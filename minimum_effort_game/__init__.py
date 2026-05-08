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

DESCRIPTION = "Minimum effort / weakest link game (Van Huyck et al., 1990)"
SUGGESTED_MULTIPLE = 3
APP_NAME = __name__


class C:
    # Payoff = a * min(efforts) - b * own_effort + c
    A = cu("2")  # Benefit from minimum effort
    B = cu("1")  # Cost of own effort
    C = cu("6")  # Fixed component
    GROUP_SIZE = 3


class GroupPlease(GroupCreatingWait):
    group_size = C.GROUP_SIZE


class ChooseEffort(Page):
    fields = dict(
        effort=RadioField(
            label="Choose your effort level:",
            choices=[(i, str(i)) for i in range(1, 8)],
        ),
    )


class Sync(SynchronizingWait):
    @classmethod
    def all_here(page, group):
        efforts = [p.effort for p in group.players]
        minimum = min(efforts)

        for player in group.players:
            player.minimum = minimum
            player.payoff = C.A * minimum - C.B * player.effort + C.C


class Results(Page):
    pass


def pipeline(session):
    rows = []

    for group, players in minimum_effort_groups(session):
        for member_id, player in enumerate(players):
            player_data = player.within(app=APP_NAME)

            rows.append(
                {
                    "session": session.name,
                    "group": group.name,
                    "uname": player.name,
                    "member_id": member_id,
                    "effort": player_data.get("effort"),
                    "minimum": player_data.get("minimum"),
                    "payoff": player_data.get("payoff"),
                }
            )

    return rows


def minimum_effort_groups(session):
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
    ChooseEffort,
    Sync,
    Results,
]
