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

DESCRIPTION = "Beauty contest / guessing game (Nagel, 1995)"

P = cu("0.67")  # Fraction of average (2/3)
PRIZE = cu("10")


class GroupPlease(GroupCreatingWait):
    group_size = 3


class Guess(Page):
    fields = dict(
        guess=DecimalField(
            label="Enter your guess (0-100):",
            min=0,
            max=100,
        ),
    )

    @classmethod
    def context(page, player):
        return dict(p=P, group_size=GroupPlease.group_size, prize=PRIZE)


class Sync(SynchronizingWait):
    @classmethod
    def all_here(page, group):
        guesses = [p.guess for p in players(group)]
        average = sum(guesses) / len(guesses)
        target = P * average

        # Find winner(s) - closest to target
        distances = [(p, abs(p.guess - target)) for p in players(group)]
        min_distance = min(d for _, d in distances)
        winners = [p for p, d in distances if d == min_distance]

        for player in players(group):
            player.target = target
            player.average = average
            player.winner = player in winners
            player.payoff = PRIZE / len(winners) if player.winner else cu(0)


class Results(Page):
    @classmethod
    def context(page, player):
        return dict(
            others=others_in_group(player),
            p=P,
        )


page_order = [
    GroupPlease,
    Guess,
    Sync,
    Results,
]
