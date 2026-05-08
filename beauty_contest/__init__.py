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
SUGGESTED_MULTIPLE = 3
APP_NAME = __name__


class C:
    P = cu("0.67")  # Fraction of average (2/3)
    GROUP_SIZE = 3
    PRIZE = cu("10")


class GroupPlease(GroupCreatingWait):
    group_size = C.GROUP_SIZE


class Guess(Page):
    fields = dict(
        guess=DecimalField(
            label="Enter your guess (0-100):",
            min=0,
            max=100,
        ),
    )


class Sync(SynchronizingWait):
    @classmethod
    def all_here(page, group):
        guesses = [p.guess for p in group.players]
        average = sum(guesses) / len(guesses)
        target = C.P * average

        # Find winner(s) - closest to target
        distances = [(p, abs(p.guess - target)) for p in group.players]
        min_distance = min(d for _, d in distances)
        winners = [p for p, d in distances if d == min_distance]

        for player in group.players:
            player.target = target
            player.average = average
            player.winner = player in winners
            player.payoff = C.PRIZE / len(winners) if player.winner else cu(0)


class Results(Page):
    pass


def pipeline(session):
    rows = []

    for group, players in beauty_contest_groups(session):
        for member_id, player in enumerate(players):
            player_data = player.within(app=APP_NAME)

            rows.append(
                {
                    "session": session.name,
                    "group": group.name,
                    "uname": player.name,
                    "member_id": member_id,
                    "guess": player_data.get("guess"),
                    "average": player_data.get("average"),
                    "target": player_data.get("target"),
                    "winner": player_data.get("winner"),
                    "payoff": player_data.get("payoff"),
                }
            )

    return rows


def beauty_contest_groups(session):
    groups = []

    for group in session.groups:
        players = group.players

        if len(players) == C.GROUP_SIZE and is_app_group(group, players):
            groups.append((group, players))

    return groups


def is_app_group(group, players):
    with group:
        if group.get("app") == APP_NAME:
            return True

        gid = group.gid

    return all(
        player.within(app=APP_NAME).get("_uproot_group") == gid for player in players
    )


page_order = [
    GroupPlease,
    Guess,
    Sync,
    Results,
]
