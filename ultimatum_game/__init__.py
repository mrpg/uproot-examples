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

DESCRIPTION = "Ultimatum game"
SUGGESTED_MULTIPLE = 2
APP_NAME = __name__


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
    def after_grouping(page, group):
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
    def show(page, player):
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
    def show(page, player):
        return not player.proposer


class Sync(SynchronizingWait):
    @classmethod
    def all_here(page, group):
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


def digest(session):
    data = []

    for group, players in ultimatum_groups(session):
        proposer = next(p for p in players if p.within(app=APP_NAME).get("proposer"))
        responder = next(
            p for p in players if not p.within(app=APP_NAME).get("proposer")
        )

        offer = proposer.within(app=APP_NAME).get("offer")
        accepted = responder.within(app=APP_NAME).get("accept")

        data.append((group.name, offer, accepted))

    return data


def pipeline(session):
    rows = []

    for group, players in ultimatum_groups(session):
        player_rows = [(player, player.within(app=APP_NAME)) for player in players]
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


def ultimatum_groups(session):
    groups = []

    for group in session.groups:
        players = group.players

        if len(players) == 2 and is_app_group(group, players):
            groups.append((group, players))

    return groups


def is_app_group(group, players):
    with group:
        if group.get("app") == APP_NAME:
            return True

        gid = group.gid

    return all(
        player.within(app=APP_NAME).get("_uproot_group") == gid for player in players
    )


page_order = [
    GroupPlease,
    Propose,
    WaitForProposal,
    Respond,
    Sync,
    Results,
]
