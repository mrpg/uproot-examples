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

DESCRIPTION = "Trust game (Berg et al., 1995)"
SUGGESTED_MULTIPLE = 2


class C:
    ENDOWMENT = cu("10")
    MULTIPLIER = 3


class Context(PlayerContext):
    @property
    def sent(self) -> Any:
        return self.player.group.players.find_one(trustor=True).sent

    @property
    def received(self) -> Any:
        return self.player.group.players.find_one(trustor=True).sent * C.MULTIPLIER

    @property
    def returned(self) -> Any:
        return self.player.group.players.find_one(trustor=False).returned


class GroupPlease(GroupCreatingWait):
    group_size = 2

    @classmethod
    def after_grouping(page, group: GroupType) -> None:
        for player, is_trustor in zip(group.players, [True, False]):
            player.trustor = is_trustor


class Send(Page):
    fields = dict(
        sent=DecimalField(
            label="How much do you send to the other player?",
            min=0,
            max=C.ENDOWMENT,
        ),
    )

    @classmethod
    def show(page, player: PlayerType) -> bool:
        return bool(player.trustor)


class WaitForSend(SynchronizingWait):
    pass


class Return(Page):
    @classmethod
    def show(page, player: PlayerType) -> bool:
        return not player.trustor

    @classmethod
    def fields(page, player: PlayerType) -> dict[str, Field]:
        trustor = player.group.players.find_one(trustor=True)
        received = trustor.sent * C.MULTIPLIER
        return dict(
            returned=DecimalField(
                label="How much do you return to the other player?",
                min=0,
                max=received,
            ),
        )


class Sync(SynchronizingWait):
    @classmethod
    def all_here(page, group: GroupType) -> None:
        trustor = group.players.find_one(trustor=True)
        trustee = group.players.find_one(trustor=False)

        received = trustor.sent * C.MULTIPLIER

        trustor.payoff = C.ENDOWMENT - trustor.sent + trustee.returned
        trustee.payoff = C.ENDOWMENT + received - trustee.returned


class Results(Page):
    pass


def pipeline(session: SessionType) -> list[dict[str, Any]]:
    rows = []

    for group in session.groups(app=__name__):
        players = group.players
        player_rows = [(player, player.within(app=__name__)) for player in players]
        trustor, trustor_data = next(
            (player, data) for player, data in player_rows if data.get("trustor")
        )
        trustee, trustee_data = next(
            (player, data) for player, data in player_rows if not data.get("trustor")
        )
        sent = trustor_data.get("sent")
        received = sent * C.MULTIPLIER if sent is not None else None

        for player, player_data in player_rows:
            rows.append(
                {
                    "session": session.name,
                    "group": group.name,
                    "uname": player.name,
                    "role": "trustor" if player_data.get("trustor") else "trustee",
                    "trustor_uname": trustor.name,
                    "trustee_uname": trustee.name,
                    "sent": sent,
                    "received": received,
                    "returned": trustee_data.get("returned"),
                    "payoff": player_data.get("payoff"),
                }
            )

    return rows


page_order = [
    GroupPlease,
    Send,
    WaitForSend,
    Return,
    Sync,
    Results,
]
