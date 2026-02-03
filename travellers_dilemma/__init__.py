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

DESCRIPTION = "Traveller's dilemma (Basu, 1994)"

# Game parameters
MIN_CLAIM = 2
MAX_CLAIM = 100
BONUS = 2  # Reward for lower claim / penalty for higher claim


class GroupPlease(GroupCreatingWait):
    group_size = 2


class Claim(Page):
    fields = dict(
        claim=IntegerField(
            label=f"Enter your claim ({MIN_CLAIM}-{MAX_CLAIM}):",
            min=MIN_CLAIM,
            max=MAX_CLAIM,
        ),
    )

    @classmethod
    def context(page, player):
        return dict(
            min_claim=MIN_CLAIM,
            max_claim=MAX_CLAIM,
            bonus=BONUS,
        )


class Sync(SynchronizingWait):
    @classmethod
    def all_here(page, group):
        player1, player2 = players(group)

        if player1.claim < player2.claim:
            player1.payoff = player1.claim + BONUS
            player2.payoff = player1.claim - BONUS
        elif player2.claim < player1.claim:
            player2.payoff = player2.claim + BONUS
            player1.payoff = player2.claim - BONUS
        else:
            # Equal claims: both get their claim amount
            player1.payoff = player1.claim
            player2.payoff = player2.claim


class Results(Page):
    @classmethod
    def context(page, player):
        return dict(
            other=other_in_group(player),
            bonus=BONUS,
        )


page_order = [
    GroupPlease,
    Claim,
    Sync,
    Results,
]
