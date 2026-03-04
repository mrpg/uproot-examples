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


class C:
    ENDOWMENT = cu("10")
    MPCR = cu("0.5")  # Marginal Per Capita Return


class Context(PlayerContext):
    @property
    def group_size(self):
        return GroupPlease.group_size

    @property
    def multiplier(self):
        return C.MPCR * GroupPlease.group_size

    @property
    def total(self):
        return sum(p.contribution for p in self.player.group.players)


class GroupPlease(GroupCreatingWait):
    group_size = 3


class Contribute(Page):
    fields = dict(
        contribution=DecimalField(
            label="How much do you contribute to the group account?",
            min=0,
            max=C.ENDOWMENT,
        ),
    )


class Sync(SynchronizingWait):
    @classmethod
    def all_here(page, group):
        total = sum(p.contribution for p in group.players)

        for player in group.players:
            player.payoff = C.ENDOWMENT - player.contribution + C.MPCR * total


class Results(Page):
    pass


page_order = [
    GroupPlease,
    Contribute,
    Sync,
    Results,
]
