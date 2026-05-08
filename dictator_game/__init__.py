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

DESCRIPTION = "Dictator game"
SUGGESTED_MULTIPLE = 2
APP_NAME = __name__


class GroupPlease(GroupCreatingWait):
    group_size = 2

    @classmethod
    def after_grouping(page, group):
        for player, is_dictator in zip(group.players, [True, False]):
            player.dictator = is_dictator


class Dictate(Page):
    fields = dict(
        give=DecimalField(label="How much do you give?", min=0, max=10),
    )

    @classmethod
    def show(page, player):
        return player.dictator


class Sync(SynchronizingWait):
    @classmethod
    def all_here(page, group):
        dictator = group.players.find_one(dictator=True)
        recipient = group.players.find_one(dictator=False)

        dictator.payoff = cu(10) - dictator.give
        recipient.payoff = dictator.give


class Results(Page):
    pass


def pipeline(session):
    rows = []

    for group, players in dictator_groups(session):
        player_rows = [(player, player.within(app=APP_NAME)) for player in players]
        dictator, dictator_data = next(
            (player, data) for player, data in player_rows if data.get("dictator")
        )
        recipient, _ = next(
            (player, data) for player, data in player_rows if not data.get("dictator")
        )

        for player, player_data in player_rows:
            rows.append(
                {
                    "session": session.name,
                    "group": group.name,
                    "uname": player.name,
                    "role": (
                        "dictator" if player_data.get("dictator") else "recipient"
                    ),
                    "dictator_uname": dictator.name,
                    "recipient_uname": recipient.name,
                    "give": dictator_data.get("give"),
                    "payoff": player_data.get("payoff"),
                }
            )

    return rows


def dictator_groups(session):
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
    Dictate,
    Sync,
    Results,
]
