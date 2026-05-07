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

DESCRIPTION = "Repeated prisoner's dilemma"
SUGGESTED_MULTIPLE = 2
APP_NAME = __name__


class C:
    ROUNDS = 3
    GROUP_SIZE = 2


class GroupPlease(GroupCreatingWait):
    group_size = C.GROUP_SIZE


class Dilemma(Page):
    fields = dict(
        cooperate=RadioField(
            label="Do you wish to cooperate?",
            choices=[(True, "Yes"), (False, "No")],
        ),
    )


def set_payoff(player):
    other = player.other_in_group

    match player.cooperate, other.cooperate:
        case True, True:
            player.payoff = 10
        case True, False:
            player.payoff = 0
        case False, True:
            player.payoff = 15
        case False, False:
            player.payoff = 3


class Sync(SynchronizingWait):
    @classmethod
    def all_here(page, group):
        for player in group.players:
            set_payoff(player)


class Results(Page):
    pass


def digest(session):
    data = []

    for group, players in prisoners_dilemma_groups(session):
        player1, player2 = players

        rounds = played_rounds(player1, player2)
        latest_round = rounds[-1] if rounds else 0

        history = [
            (
                round_num,
                player1.within(app=APP_NAME, round=round_num).get("cooperate"),
                player2.within(app=APP_NAME, round=round_num).get("cooperate"),
            )
            for round_num in range(1, latest_round + 1)
        ]

        data.append(
            (
                group.name,
                latest_round,
                history,
            )
        )

    return data


def pipeline(session):
    rows = []

    for group, players in prisoners_dilemma_groups(session):
        rounds = played_rounds(*players)

        for member_id, player in enumerate(players):
            other = players[1 - member_id]

            for round_num in rounds:
                player_data = player.within(app=APP_NAME, round=round_num)
                other_data = other.within(app=APP_NAME, round=round_num)

                rows.append(
                    {
                        "session": session.name,
                        "group": group.name,
                        "round": round_num,
                        "uname": player.name,
                        "member_id": member_id,
                        "cooperate": player_data.get("cooperate"),
                        "other_uname": other.name,
                        "other_cooperate": other_data.get("cooperate"),
                        "payoff": player_data.get("payoff"),
                    }
                )

    return rows


def prisoners_dilemma_groups(session):
    groups = []

    for group in session.groups:
        players = list(group.players)

        if len(players) != C.GROUP_SIZE:
            continue

        if is_prisoners_dilemma_group(group, players):
            groups.append((group, players))

    return groups


def is_prisoners_dilemma_group(group, players):
    with group:
        if group.get("app") == APP_NAME:
            return True

        gid = group.gid

    return all(
        player.within(app=APP_NAME).get("_uproot_group") == gid for player in players
    )


page_order = [
    GroupPlease,
    Rounds(
        Dilemma,
        Sync,
        Results,
        n=C.ROUNDS,
    ),
]
