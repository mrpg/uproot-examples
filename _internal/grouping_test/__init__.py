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


class WaitForEveryone(SynchronizingWait):
    synchronize = "session"

    @classmethod
    def all_here(page, session):
        # Get all players and sort alphabetically by name
        all_players = sorted(players(session), key=lambda p: p.name)

        # Split into two groups of roughly equal size
        mid = len(all_players) // 2
        group_a = all_players[:mid]
        group_b = all_players[mid:]

        # Create the groups using create_groups
        if group_a and group_b:
            create_groups(session, [group_a, group_b])
        elif group_a:
            # Only one group if odd number with 1 player
            create_groups(session, [group_a])


class ShowGroup(Page):
    @classmethod
    def context(page, player):
        if player.group:
            group_members = sorted(players(player.group), key=lambda p: p.name)
            group_name = player.group.name
        else:
            group_members = []
            group_name = None

        return dict(
            group_name=group_name,
            group_members=group_members,
        )


page_order = [
    WaitForEveryone,
    ShowGroup,
]
