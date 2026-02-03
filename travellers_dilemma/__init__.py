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

DESCRIPTION = "Traveller’s dilemma (Basu, 1994)"


class C:
    MIN_CLAIM = 2
    MAX_CLAIM = 100
    BONUS = 2  # Reward for lower claim / penalty for higher claim


class GroupPlease(GroupCreatingWait):
    group_size = 2


class Claim(Page):
    fields = dict(
        claim=IntegerField(
            label=f"Enter your claim (between {C.MIN_CLAIM} and {C.MAX_CLAIM}):",
            min=C.MIN_CLAIM,
            max=C.MAX_CLAIM,
        ),
    )


class Sync(SynchronizingWait):
    @classmethod
    def all_here(page, group):
        player1, player2 = players(group)

        if player1.claim < player2.claim:
            player1.payoff = player1.claim + C.BONUS
            player2.payoff = player1.claim - C.BONUS
        elif player2.claim < player1.claim:
            player2.payoff = player2.claim + C.BONUS
            player1.payoff = player2.claim - C.BONUS
        else:
            # Equal claims: both get their claim amount
            player1.payoff = player1.claim
            player2.payoff = player2.claim


class Results(Page):
    @classmethod
    def context(page, player):
        return dict(
            other=other_in_group(player),
        )


page_order = [
    GroupPlease,
    Claim,
    Sync,
    Results,
]
