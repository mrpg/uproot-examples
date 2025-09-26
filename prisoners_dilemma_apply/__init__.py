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

DESCRIPTION = "Prisoner's dilemma (using apply)"


class GroupPlease(GroupCreatingWait):
    group_size = 2


class Dilemma(Page):
    fields = dict(
        cooperate=RadioField(
            label="Do you wish to cooperate?",
            choices=[(True, "Yes"), (False, "No")],
        ),
    )


class Sync(SynchronizingWait):
    @classmethod
    def set_payoff(page, player):
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

    @classmethod
    def all_here(page, group):
        players(group).apply(page.set_payoff)


class Results(Page):
    @classmethod
    def context(page, player):
        return dict(
            other=other_in_group(player),
        )


page_order = [
    GroupPlease,
    Dilemma,
    Sync,
    Results,
]
