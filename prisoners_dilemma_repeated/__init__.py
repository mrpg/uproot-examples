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

DESCRIPTION = "Repeated prisoner's dilemma"


class C:
    ROUNDS = 3


class GroupPlease(GroupCreatingWait):
    group_size = 2


class Dilemma(Page):
    fields = dict(
        cooperate=RadioField(
            label="Do you wish to cooperate?",
            choices=[(True, "Yes"), (False, "No")],
        ),
    )

    @classmethod
    def context(page, player):
        return dict(
            other=other_in_group(player),
            rounds_so_far=range(1, player.round),
        )


def set_payoff(player):
    other = other_in_group(player)

    match player.cooperate, other.cooperate:
        case True, True:
            player.payoff = 10
        case True, False:
            player.payoff = 0
        case False, True:
            player.payoff = 15
        case False, False:
            player.payoff = 3


class Sync(SynchronizingWait):
    @classmethod
    def all_here(page, group):
        for player in players(group):
            set_payoff(player)


class Results(Page):
    @classmethod
    def context(page, player):
        return dict(
            other=other_in_group(player),
        )


def digest(session):
    data = []

    for gname in session.groups:
        with session.group(gname) as group:
            player1 = players(group).find_one(_.member_id, 0)
            player2 = players(group).find_one(_.member_id, 1)

            latest_round = max(player1.round, player2.round)
            history = []

            for round in range(1, latest_round + 1):
                history.append(
                    (
                        round,
                        player1.within(round=round).cooperate,
                        player2.within(round=round).cooperate,
                    ),
                )

            data.append((gname, latest_round, history))

    return data


page_order = [
    GroupPlease,
    Rounds(
        Dilemma,
        Sync,
        Results,
        n=C.ROUNDS,
    ),
]
