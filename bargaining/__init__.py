# Docs are available at https://uproot.science/
# Examples are available at https://github.com/mrpg/uproot-examples
#
# This example app is under the 0BSD license. You can use it freely and build on it
# without any limitations and without any attribution. However, these two lines must be
# preserved in any uproot app (the license file is automatically installed in projects):
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt

from time import time

from uproot.fields import *
from uproot.smithereens import *

DESCRIPTION = "Unstructured real-time bargaining with a deadline"
SUGGESTED_MULTIPLE = 2
APP_NAME = __name__


class C:
    PIE = 10
    DURATION = 120.0  # Seconds until the deadline


class GroupPlease(GroupCreatingWait):
    group_size = 2

    @classmethod
    def after_grouping(page, group):
        group.agreed = False
        group.deadline = time() + C.DURATION

        for player in group.players:
            player.proposal = None


class Bargain(Page):
    @classmethod
    def timeout(page, player):
        return max(0.0, player.group.deadline - time())

    @classmethod
    def timeout_reached(page, player):
        if not player.group.agreed:
            player.payoff = cu(0)

    @classmethod
    def may_proceed(page, player):
        return player.group.agreed or time() >= player.group.deadline

    @classmethod
    def jsvars(page, player):
        return {
            "pie": C.PIE,
            "agreed": player.group.agreed,
            "my_proposal": player.proposal,
            "their_proposal": player.other_in_group.proposal,
        }

    @live
    def propose(page, player, amount: float):
        if player.group.agreed or not 0 <= amount <= C.PIE:
            return

        player.proposal = round(amount, 2)
        notify(player, player.others_in_group, player.proposal, event="Proposal")

    @live
    def accept(page, player):
        group = player.group

        with group:
            other = player.other_in_group
            their_proposal = other.proposal

            if group.agreed or their_proposal is None:
                return

            group.agreed = True

        player.payoff = cu(C.PIE) - cu(str(their_proposal))
        other.payoff = cu(str(their_proposal))
        notify(player, group.players, None, event="Agreed")


class Results(Page):
    pass


def pipeline(session):
    rows = []

    for group, players in bargaining_groups(session):
        with group:
            agreed = group.get("agreed")

        for member_id, player in enumerate(players):
            player_data = player.within(app=APP_NAME)

            rows.append(
                {
                    "session": session.name,
                    "group": group.name,
                    "uname": player.name,
                    "member_id": member_id,
                    "proposal": player_data.get("proposal"),
                    "agreed": agreed,
                    "payoff": player_data.get("payoff"),
                }
            )

    return rows


def bargaining_groups(session):
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
    Bargain,
    Results,
]
