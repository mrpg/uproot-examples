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
SUGGESTED_MULTIPLE = 2
APP_NAME = __name__


def new_player(player):
    player.payoff = 0  # initialize this field on player entry


class GroupPlease(GroupCreatingWait):
    group_size = 2


class Claim(Page):
    fields = dict(
        claim=DecimalField(
            label="How much do you claim?",
            addon_start="$",
        ),
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


def pipeline(session):
    rows = []

    for group, players in focal_point_groups(session):
        claims = [player.within(app=APP_NAME).get("claim") for player in players]
        total_claim = (
            sum(claims) if all(claim is not None for claim in claims) else None
        )

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
                    "claim": player_data.get("claim"),
                    "other_uname": other.name,
                    "other_claim": other_data.get("claim"),
                    "total_claim": total_claim,
                    "payoff": player_data.get("payoff"),
                }
            )

    return rows


def focal_point_groups(session):
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
    Claim,
    Sync,
    Results,
]
