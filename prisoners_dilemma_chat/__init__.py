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

DESCRIPTION = "Prisoner's dilemma with continuous chat"
SUGGESTED_MULTIPLE = 2
APP_NAME = __name__


class C:
    PAYOFF_MATRIX = {
        (True, True): 10,
        (True, False): 0,
        (False, True): 15,
        (False, False): 3,
    }


class Context(PlayerContext):
    @property
    def payoff(self):
        return C.PAYOFF_MATRIX[
            self.player.cooperate,
            self.player.other_in_group.cooperate,
        ]


class GroupPlease(GroupCreatingWait):
    group_size = 2

    @classmethod
    def after_grouping(page, group):
        group.chat = chat.create(group.session)

        for i, p in enumerate(group.players, 1):
            chat.add_player(group.chat, p, pseudonym=f"Player {i}")


class Dilemma(Page):
    fields = dict(
        cooperate=RadioField(
            label="Do you wish to cooperate?",
            choices=[(True, "Yes"), (False, "No")],
        ),
    )


class Sync(SynchronizingWait):
    pass


class Results(Page):
    pass


def pipeline(session):
    rows = []

    for group, players in prisoner_groups(session):
        player1, player2 = players

        for member_id, player in enumerate(players):
            other = player2 if member_id == 0 else player1
            player_data = player.within(app=APP_NAME)
            other_data = other.within(app=APP_NAME)
            cooperate = player_data.get("cooperate")
            other_cooperate = other_data.get("cooperate")

            rows.append(
                {
                    "session": session.name,
                    "group": group.name,
                    "uname": player.name,
                    "member_id": member_id,
                    "cooperate": cooperate,
                    "other_uname": other.name,
                    "other_cooperate": other_cooperate,
                    "payoff": player_data.get("payoff"),
                }
            )

    return rows


def prisoner_groups(session):
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
    Dilemma,
    Sync,
    Results,
]
