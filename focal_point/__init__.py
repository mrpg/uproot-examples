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

DESCRIPTION = "Coordination through focal points"


def new_player(player):
    player.payoff = 0  # initialize this field on player entry


class Context(PlayerContext):
    @property
    def other(self):
        return self.player.other_in_group


class GroupPlease(GroupCreatingWait):
    group_size = 2


class Claim(Page):
    fields = dict(
        claim=DecimalField(label="How much do you claim?"),
    )


class Sync(SynchronizingWait):
    @classmethod
    def set_payoff(page, player):
        other = player.other_in_group

        if player.claim + other.claim <= 100:
            player.payoff = player.claim

    @classmethod
    def all_here(page, group):
        group.players.apply(page.set_payoff)


class Results(Page):
    pass


page_order = [
    GroupPlease,
    Claim,
    Sync,
    Results,
]
