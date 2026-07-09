# Docs are available at https://uproot.science/
# Examples are available at https://github.com/mrpg/uproot-examples
#
# This example app is under the 0BSD license. You can use it freely and build on it
# without any limitations and without any attribution. However, these two lines must be
# preserved in any uproot app (the license file is automatically installed in projects):
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt

from random import random

from uproot.fields import *
from uproot.smithereens import *

DESCRIPTION = "Indefinitely repeated prisoner's dilemma"
SUGGESTED_MULTIPLE = 2


class C:
    GROUP_SIZE = 2
    DEFAULT_CONTINUATION_PROB = 0.75
    PAYOFF_MATRIX = {
        (True, True): 10,
        (True, False): 0,
        (False, True): 15,
        (False, False): 3,
    }


class GroupPlease(GroupCreatingWait):
    group_size = C.GROUP_SIZE


class Dilemma(Page):
    fields = dict(
        cooperate=RadioField(
            label="Do you wish to cooperate?",
            choices=[(True, "Yes"), (False, "No")],
        ),
    )


class Sync(SynchronizingWait):
    @classmethod
    def all_here(page, group: GroupType) -> None:
        prob = group.session.settings.get(
            "continuation_prob", C.DEFAULT_CONTINUATION_PROB
        )
        continue_game = random() < prob

        for player in group.players:
            other = player.other_in_group
            player.payoff = C.PAYOFF_MATRIX[player.cooperate, other.cooperate]
            player.add_round = continue_game


class Results(Page):
    pass


def digest(session: SessionType) -> dict[str, Any]:
    data = []

    for group in session.groups(app=__name__):
        players = group.players
        player1, player2 = players

        rounds = played_rounds(player1, player2)
        latest_round = rounds[-1] if rounds else 0

        history = [
            (
                round_num,
                player1.within.strict(app=__name__, round=round_num).get("cooperate"),
                player2.within.strict(app=__name__, round=round_num).get("cooperate"),
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


def pipeline(session: SessionType) -> list[dict[str, Any]]:
    rows = []

    for group in session.groups(app=__name__):
        players = group.players
        rounds = played_rounds(*players)

        for member_id, player in enumerate(players):
            other = players[1 - member_id]

            for round_num in rounds:
                player_data = player.within.strict(app=__name__, round=round_num)
                other_data = other.within.strict(app=__name__, round=round_num)

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


def played_rounds(*players):
    return sorted(
        {
            round_num
            for player in players
            for round_num, _ in player.within(app=__name__).along("round")
        }
    )


page_order = [
    GroupPlease,
    Repeat(
        Dilemma,
        Sync,
        Results,
    ),
]
