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

DESCRIPTION = "Minimum effort / weakest link game (Van Huyck et al., 1990)"

# Payoff = a * min(efforts) - b * own_effort + c
A = cu("2")  # Benefit from minimum effort
B = cu("1")  # Cost of own effort
C = cu("6")  # Fixed component


class GroupPlease(GroupCreatingWait):
    group_size = 3


class ChooseEffort(Page):
    fields = dict(
        effort=RadioField(
            label="Choose your effort level:",
            choices=[(i, str(i)) for i in range(1, 8)],
        ),
    )

    @classmethod
    def context(page, player):
        return dict(a=A, b=B, c=C, group_size=GroupPlease.group_size)


class Sync(SynchronizingWait):
    @classmethod
    def all_here(page, group):
        efforts = [p.effort for p in players(group)]
        minimum = min(efforts)

        for player in players(group):
            player.minimum = minimum
            player.payoff = A * minimum - B * player.effort + C


class Results(Page):
    @classmethod
    def context(page, player):
        return dict(others=others_in_group(player))


page_order = [
    GroupPlease,
    ChooseEffort,
    Sync,
    Results,
]
