# Docs are available at https://uproot.science/
# Examples are available at https://github.com/mrpg/uproot-examples
#
# This example app is under the 0BSD license. You can use it freely and build on it
# without any limitations and without any attribution. However, these two lines must be
# preserved in any uproot app (the license file is automatically installed in projects):
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt

from uproot.fields import *
from uproot.smithereens import *

DESCRIPTION = "Linear public goods game with third-party punishment"
SUGGESTED_MULTIPLE = 4


class C:
    ENDOWMENT = cu("20")
    PUNISHER_ENDOWMENT = cu("20")
    MPCR = cu("0.4")
    GROUP_SIZE = 4
    NUM_CONTRIBUTORS = 3
    PUNISHMENT_RATIO = 3


class Context(PlayerContext):
    @property
    def total_contribution(self) -> Any:
        return sum(
            p.contribution for p in self.player.group.players if not p.is_punisher
        )

    @property
    def contributors(self) -> list[Any]:
        return [p for p in self.player.group.players if not p.is_punisher]

    @property
    def punishment_received(self) -> Any:
        punisher = self.player.group.players.find_one(is_punisher=True)
        key = f"punish_{self.player.member_id}"
        return getattr(punisher, key, cu("0")) * C.PUNISHMENT_RATIO

    @property
    def punishment_spent(self) -> Any:
        return sum(
            getattr(self.player, f"punish_{p.member_id}", cu("0"))
            for p in self.player.group.players
            if not p.is_punisher
        )


class GroupPlease(GroupCreatingWait):
    group_size = C.GROUP_SIZE

    @classmethod
    def after_grouping(page, group: GroupType) -> None:
        players = list(group.players)
        for i, player in enumerate(players):
            player.is_punisher = i == C.NUM_CONTRIBUTORS


class Contribute(Page):
    fields = dict(
        contribution=DecimalField(
            label="How much do you contribute to the group account?",
            min=0,
            max=C.ENDOWMENT,
        ),
    )

    @classmethod
    def show(page, player: PlayerType) -> bool:
        return bool(not player.is_punisher)


class WaitForContributions(SynchronizingWait):
    pass


class Punish(Page):
    @classmethod
    def show(page, player: PlayerType) -> bool:
        return bool(player.is_punisher)

    @classmethod
    def fields(page, player: PlayerType) -> dict[str, Field]:
        contributors = [p for p in player.group.players if not p.is_punisher]
        result = {}
        for i, contributor in enumerate(contributors):
            result[f"punish_{contributor.member_id}"] = DecimalField(
                label=f"Punishment for Contributor {i + 1} (contributed {contributor.contribution})",
                min=0,
                max=C.PUNISHER_ENDOWMENT,
            )
        return result

    @classmethod
    def validate(page, player: PlayerType, data: dict[str, Any]) -> str | None:
        total = sum(data.values())
        if total > C.PUNISHER_ENDOWMENT:
            return f"Total punishment cost cannot exceed your endowment of {C.PUNISHER_ENDOWMENT}. You allocated {total}."
        return None


class WaitForPunisher(SynchronizingWait):
    @classmethod
    def all_here(page, group: GroupType) -> None:
        contributors = [p for p in group.players if not p.is_punisher]
        punisher = group.players.find_one(is_punisher=True)

        total_contribution = sum(p.contribution for p in contributors)

        for contributor in contributors:
            punishment_received = (
                getattr(punisher, f"punish_{contributor.member_id}", cu("0"))
                * C.PUNISHMENT_RATIO
            )
            contributor.payoff = (
                C.ENDOWMENT
                - contributor.contribution
                + C.MPCR * total_contribution
                - punishment_received
            )

        total_spent = sum(
            getattr(punisher, f"punish_{p.member_id}", cu("0")) for p in contributors
        )
        punisher.payoff = C.PUNISHER_ENDOWMENT - total_spent


class Results(Page):
    pass


def digest(session: SessionType) -> list[Any]:
    data = []

    for group in session.groups:
        players = group.players
        if len(players) != C.GROUP_SIZE:
            continue
        if not any(
            p.within(app=__name__).get("is_punisher") is not None for p in players
        ):
            continue

        contributors = []
        punisher_data = None

        for player in players:
            pd = player.within(app=__name__)
            if pd.get("is_punisher"):
                punisher_data = pd
            else:
                contributors.append((player, pd))

        contribution_details = []
        total_punishment = cu("0")

        for player, pd in contributors:
            contribution = pd.get("contribution")
            punishment = (
                punisher_data.get(f"punish_{player.member_id}")
                if punisher_data
                else None
            )
            if punishment is not None:
                total_punishment += punishment
            contribution_details.append((contribution, punishment))

        total_contribution = (
            sum(c for c, _ in contribution_details if c is not None)
            if all(c is not None for c, _ in contribution_details)
            else None
        )

        data.append(
            (group.name, total_contribution, contribution_details, total_punishment)
        )

    return data


def pipeline(session: SessionType) -> list[dict[str, Any]]:
    rows = []

    for group in session.groups:
        players = group.players
        if len(players) != C.GROUP_SIZE:
            continue
        if not any(
            p.within(app=__name__).get("is_punisher") is not None for p in players
        ):
            continue

        for player in players:
            pd = player.within(app=__name__)
            is_punisher = pd.get("is_punisher")

            row = {
                "session": session.name,
                "group": group.name,
                "uname": player.name,
                "member": player.member_id,
                "role": "punisher" if is_punisher else "contributor",
                "contribution": pd.get("contribution"),
                "payoff": pd.get("payoff"),
            }

            if is_punisher:
                row["punishment"] = {}

                for other in players:
                    if not other.within(app=__name__).get("is_punisher"):
                        row["punishment"][str(other.member_id)] = str(
                            pd.get(f"punish_{other.member_id}")
                        )

            rows.append(row)

    return rows


page_order = [
    GroupPlease,
    Contribute,
    WaitForContributions,
    Punish,
    WaitForPunisher,
    Results,
]
