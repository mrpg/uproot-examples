# Docs are available at https://uproot.science/
# Examples are available at https://github.com/mrpg/uproot-examples
#
# This example app is under the 0BSD license. You can use it freely and build on it
# without any limitations and without any attribution. However, these two lines must be
# preserved in any uproot app (the license file is automatically installed in projects):
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt

import json
from string import ascii_uppercase

from uproot.fields import *
from uproot.smithereens import *

DESCRIPTION = "Generic n×n game (defaults to Rock-Paper-Scissors)"
SUGGESTED_MULTIPLE = 2
APP_NAME = __name__

ACTIONS_26 = list(ascii_uppercase)


class C:
    # Default: Rock-Paper-Scissors
    # Each cell is [row_player_payoff, col_player_payoff]
    #           A(Rock)  B(Paper) C(Scissors)
    DEFAULT_MATRIX = [
        [[0, 0], [-1, 1], [1, -1]],
        [[1, -1], [0, 0], [-1, 1]],
        [[-1, 1], [1, -1], [0, 0]],
    ]


def get_matrix(session):
    return session.settings.get("matrix", C.DEFAULT_MATRIX)


def get_n(session):
    return len(get_matrix(session))


def get_actions(session):
    return ACTIONS_26[: get_n(session)]


class Context(PlayerContext):
    @property
    def actions(self):
        return get_actions(self.player.session)

    @property
    def matrix(self):
        return get_matrix(self.player.session)

    @property
    def matrix_json(self):
        return json.dumps(get_matrix(self.player.session))

    @property
    def actions_json(self):
        return json.dumps(get_actions(self.player.session))


class GroupPlease(GroupCreatingWait):
    group_size = 2


class Instructions(Page):
    pass


class Decision(Page):
    fields = dict(
        choice=RadioField(
            label="Please select your choice:",
            choices=[(letter, f"Action {letter}") for letter in ACTIONS_26],
        ),
    )

    @classmethod
    def after_once(page, player):
        actions = get_actions(player.session)
        if player.choice not in actions:
            raise page.error(
                choice=f"Please select a valid action ({', '.join(actions)})."
            )


def set_payoff(player):
    matrix = get_matrix(player.session)
    actions = get_actions(player.session)
    other = player.other_in_group
    i = actions.index(player.choice)
    j = actions.index(other.choice)
    player.payoff = matrix[i][j][0]
    other.payoff = matrix[i][j][1]


class Sync(SynchronizingWait):
    @classmethod
    def all_here(page, group):
        player = group.players[0]
        set_payoff(player)


class Results(Page):
    pass


def pipeline(session):
    rows = []

    for group, players in app_groups(session):
        for member_id, player in enumerate(players):
            other = players[1 - member_id]
            player_data = player.within(app=APP_NAME)
            other_data = other.within(app=APP_NAME)

            rows.append(
                {
                    "session": session.name,
                    "group": group.name,
                    "uname": player.name,
                    "member_id": member_id,
                    "choice": player_data.get("choice"),
                    "other_uname": other.name,
                    "other_choice": other_data.get("choice"),
                    "payoff": player_data.get("payoff"),
                }
            )

    return rows


def app_groups(session):
    groups = []

    for group in session.groups:
        players = group.players

        if len(players) == 2 and is_app_group(group, players):
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
    Instructions,
    Decision,
    Sync,
    Results,
]
