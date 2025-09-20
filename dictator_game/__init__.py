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

DESCRIPTION = "Dictator game"


class GroupPlease(GroupCreatingWait):
    group_size = 2

    @classmethod
    def after_grouping(page, group):
        for player, is_dictator in zip(players(group), [True, False]):
            player.dictator = is_dictator


class Dictate(Page):
    fields = dict(
        give=DecimalField(label="How much do you give?", min=0, max=10),
    )

    @classmethod
    def show(page, player):
        return player.dictator


class Sync(SynchronizingWait):
    @classmethod
    def all_here(page, group):
        dictator = players(group).find_one(_.dictator, True)
        recipient = players(group).find_one(_.dictator, False)

        dictator.payoff = cu(10) - dictator.give
        recipient.payoff = dictator.give


class Results(Page):
    pass


page_order = [
    GroupPlease,
    Dictate,
    Sync,
    Results,
]
