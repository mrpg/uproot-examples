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

DESCRIPTION = "Public goods game"

ENDOWMENT = cu("10")
MPCR = cu("0.5")  # Marginal Per Capita Return


class GroupPlease(GroupCreatingWait):
    group_size = 3


class Contribute(Page):
    fields = dict(
        contribution=DecimalField(
            label="How much do you contribute to the group account?",
            min=0,
            max=ENDOWMENT,
        ),
    )

    @classmethod
    def context(page, player):
        group_size = GroupPlease.group_size
        multiplier = MPCR * group_size

        return dict(
            endowment=ENDOWMENT,
            group_size=group_size,
            multiplier=multiplier,
        )


class Sync(SynchronizingWait):
    @classmethod
    def all_here(page, group):
        total = sum(p.contribution for p in players(group))

        for player in players(group):
            player.payoff = ENDOWMENT - player.contribution + MPCR * total


class Results(Page):
    @classmethod
    def context(page, player):
        total = sum(p.contribution for p in players(player.group))

        return dict(total=total)


page_order = [
    GroupPlease,
    Contribute,
    Sync,
    Results,
]
