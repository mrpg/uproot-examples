# Docs are available at https://uproot.science/
# Examples are available at https://github.com/mrpg/uproot-examples
#
# This example app is under the 0BSD license. You can use it freely and build on it
# without any limitations and without any attribution. However, these two lines must be
# preserved in any uproot app (the license file is automatically installed in projects):
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt

from decimal import Decimal

from uproot.fields import *
from uproot.smithereens import *

DESCRIPTION = "Ultimatum game"
SUGGESTED_MULTIPLE = 2


class Context(PlayerContext):
    @property
    def offer(self):
        return self.player.group.players.find_one(proposer=True).offer

    @property
    def accepted(self):
        return self.player.group.players.find_one(proposer=False).accept


class GroupPlease(GroupCreatingWait):
    group_size = 2

    @classmethod
    def after_grouping(page, group: GroupType) -> None:
        for player, is_proposer in zip(group.players, [True, False]):
            player.proposer = is_proposer


class Propose(Page):
    fields = dict(
        offer=DecimalField(
            label="How much do you offer to the other player?",
            min=0,
            max=10,
        ),
    )

    @classmethod
    def show(page, player: PlayerType) -> bool:
        return player.proposer


class WaitForProposal(SynchronizingWait):
    pass


class Respond(Page):
    fields = dict(
        accept=RadioField(
            label="Do you accept the offer?",
            choices=[(True, "Yes"), (False, "No")],
        ),
    )

    @classmethod
    def show(page, player: PlayerType) -> bool:
        return not player.proposer


class Sync(SynchronizingWait):
    @classmethod
    def all_here(page, group: GroupType) -> None:
        proposer = group.players.find_one(proposer=True)
        responder = group.players.find_one(proposer=False)

        if responder.accept:
            proposer.payoff = cu(10) - proposer.offer
            responder.payoff = proposer.offer
        else:
            proposer.payoff = cu(0)
            responder.payoff = cu(0)


class Results(Page):
    pass


def digest(session: SessionType) -> dict[str, Any]:
    data = []
    summary_by_offer: dict[Decimal, dict[str, int]] = {}

    for group in session.groups(app=__name__):
        players = group.players
        proposer = next(p for p in players if p.within(app=__name__).get("proposer"))
        responder = next(
            p for p in players if not p.within(app=__name__).get("proposer")
        )

        offer = proposer.within(app=__name__).get("offer")
        accepted = responder.within(app=__name__).get("accept")

        data.append((group.name, offer, accepted))

        if offer is not None:
            counts = summary_by_offer.setdefault(
                offer,
                {"accepted": 0, "rejected": 0, "pending": 0},
            )

            if accepted is True:
                counts["accepted"] += 1
            elif accepted is False:
                counts["rejected"] += 1
            else:
                counts["pending"] += 1

    summary = []

    for offer, counts in sorted(summary_by_offer.items()):
        accepted = counts["accepted"]
        rejected = counts["rejected"]
        pending = counts["pending"]

        summary.append(
            (
                offer,
                cu(10) - offer,
                accepted,
                rejected,
                pending,
                accepted + rejected + pending,
            )
        )

    return {"data": data, "summary": summary}


def pipeline(session: SessionType) -> list[dict[str, Any]]:
    rows = []

    for group in session.groups(app=__name__):
        players = group.players
        player_rows = [(player, player.within(app=__name__)) for player in players]
        proposer, proposer_data = next(
            (player, data) for player, data in player_rows if data.get("proposer")
        )
        responder, responder_data = next(
            (player, data) for player, data in player_rows if not data.get("proposer")
        )

        for player, player_data in player_rows:
            rows.append(
                {
                    "session": session.name,
                    "group": group.name,
                    "uname": player.name,
                    "role": "proposer" if player_data.get("proposer") else "responder",
                    "proposer_uname": proposer.name,
                    "responder_uname": responder.name,
                    "offer": proposer_data.get("offer"),
                    "accepted": responder_data.get("accept"),
                    "payoff": player_data.get("payoff"),
                }
            )

    return rows


page_order = [
    GroupPlease,
    Propose,
    WaitForProposal,
    Respond,
    Sync,
    Results,
]
