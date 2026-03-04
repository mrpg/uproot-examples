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

DESCRIPTION = """Wait for session, then create two groups of identical size and notify
    surplus participant that they could not be grouped. Hence, to test this app,
    run it with an odd number of participants."""


class PageWithTimeout(Page):
    @classmethod
    def timeout(page, player):
        return 20


class WaitForEveryone(SynchronizingWait):
    synchronize = "session"

    @classmethod
    def all_here(page, session):
        # Get all players and sort alphabetically by name
        all_players = sorted(session.players, key=lambda p: p.name)
        if len(all_players) == 1:
            # Only one player
            create_group(session, all_players)
        else:
            # Split into two groups of equal size
            mid = len(all_players) // 2
            group_a = all_players[:mid]
            if len(all_players) % 2 == 0:
                group_b = all_players[mid:]
            else:
                group_b = all_players[mid : len(all_players) - 1]
            create_groups(session, [group_a, group_b])


class ShowGroup(Page):
    @classmethod
    def templatevars(page, player):
        if player.group:
            group_members = sorted(player.group.players, key=lambda p: p.name)
            group_name = player.group.name
        else:
            # Surplus participant (not grouped)
            group_members = []
            group_name = None
        return dict(
            group_name=group_name,
            group_members=group_members,
        )


page_order = [
    PageWithTimeout,
    WaitForEveryone,
    ShowGroup,
]
