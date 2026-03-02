# Docs are available at https://uproot.science/
# Examples are available at https://github.com/mrpg/uproot-examples
#
# This example app is under the 0BSD license. You can use it freely and build on it
# without any limitations and without any attribution. However, these two lines must be
# preserved in any uproot app (the license file is automatically installed in projects):
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt

from uproot.smithereens import *

DESCRIPTION = "Wait for session, then create two alphabetically-sorted groups"


class Context:
    def group_name(player):
        if player.group:
            return player.group.name

        return None

    def group_members(player):
        if player.group:
            return sorted(players(player.group), key=lambda p: p.name)

        return []


class WaitForEveryone(SynchronizingWait):
    synchronize = "session"

    @classmethod
    def all_here(page, session):
        # Get all players and sort alphabetically by name
        all_players = sorted(players(session), key=lambda p: p.name)

        if len(all_players) == 1:
            # Only one player
            create_group(session, all_players)
        else:
            # Split into two groups of roughly equal size
            mid = len(all_players) // 2
            group_a = all_players[:mid]
            group_b = all_players[mid:]

            create_groups(session, [group_a, group_b])


class ShowGroup(Page):
    pass


page_order = [
    WaitForEveryone,
    ShowGroup,
]
