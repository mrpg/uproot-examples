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

DESCRIPTION = "Generic 2×2 game"


class C:
    """Payoff matrix configuration.

    Payoffs are defined as (row_player, column_player) for each cell.
    Row player chooses A or B (rows), column player chooses A or B (columns).

              | Other: A | Other: B |
    ----------|----------|----------|
    You: A    |  AA      |  AB      |
    You: B    |  BA      |  BB      |
    """

    AA = (10, 10)  # Both choose A
    AB = (0, 15)  # You choose A, other chooses B
    BA = (15, 0)  # You choose B, other chooses A
    BB = (3, 3)  # Both choose B


class GroupPlease(GroupCreatingWait):
    group_size = 2


class Instructions(Page):
    @classmethod
    def context(page, player):
        return dict(payoffs=C)


class Decision(Page):
    fields = dict(
        choice=RadioField(
            label="Please select your choice:",
            choices=[("A", "Action A"), ("B", "Action B")],
        ),
    )

    @classmethod
    def context(page, player):
        return dict(payoffs=C)


def set_payoff(player):
    other = other_in_group(player)
    cell = getattr(C, player.choice + other.choice)
    player.payoff = cell[0]
    other.payoff = cell[1]


class Sync(SynchronizingWait):
    @classmethod
    def all_here(page, group):
        player = players(group)[0]
        set_payoff(player)


class Results(Page):
    @classmethod
    def context(page, player):
        return dict(other=other_in_group(player))


page_order = [
    GroupPlease,
    Instructions,
    Decision,
    Sync,
    Results,
]
