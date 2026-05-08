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

DESCRIPTION = "Public goods game"
SUGGESTED_MULTIPLE = 3
APP_NAME = __name__


class C:
    ENDOWMENT = cu("10")
    MPCR = cu("0.5")  # Marginal Per Capita Return
    GROUP_SIZE = 3
    MULTIPLIER = MPCR * GROUP_SIZE


class Context(PlayerContext):
    @property
    def total(self):
        return sum(p.contribution for p in self.player.group.players)


class GroupPlease(GroupCreatingWait):
    group_size = C.GROUP_SIZE


class Contribute(Page):
    fields = dict(
        contribution=DecimalField(
            label="How much do you contribute to the group account?",
            min=0,
            max=C.ENDOWMENT,
        ),
    )


class Sync(SynchronizingWait):
    @classmethod
    def all_here(page, group):
        total = sum(p.contribution for p in group.players)

        for player in group.players:
            player.payoff = C.ENDOWMENT - player.contribution + C.MPCR * total


class Results(Page):
    pass


def pipeline(session):
    rows = []

    for group, players in public_goods_groups(session):
        contributions = [
            player.within(app=APP_NAME).get("contribution") for player in players
        ]
        total = (
            sum(contributions) if all(c is not None for c in contributions) else None
        )

        for member_id, player in enumerate(players):
            player_data = player.within(app=APP_NAME)

            rows.append(
                {
                    "session": session.name,
                    "group": group.name,
                    "uname": player.name,
                    "member_id": member_id,
                    "contribution": player_data.get("contribution"),
                    "total_contribution": total,
                    "mpcr": C.MPCR,
                    "payoff": player_data.get("payoff"),
                }
            )

    return rows


def public_goods_groups(session):
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
    Contribute,
    Sync,
    Results,
]
