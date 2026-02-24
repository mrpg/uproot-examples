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

DESCRIPTION = """Wait for session, then create groups of identical size C.GROUP_SIZE and
    notify surplus participants that they could not be grouped. Hence, to test this app,
    run it with a number of participants that is not a multiple of C.GROUP_SIZE."""


# CONSTANTS


class C:

    GROUP_SIZE = 3


# FUNCTIONS


def new_player(player):
    """Initialize variables."""

    player.grouped = False
    player.timed_out = False


# PAGES


class PageWithTimeout(Page):

    @classmethod
    def timeout(page, player):
        return 60

    @classmethod
    def timeout_reached(page, player):
        player.timed_out = True

    @classmethod
    def fields(page, player):
        return {
            "abort": BooleanField(label="Abort after this page."),
        }

    @classmethod
    def validate(page, player, data):
        if data.get("abort"):
            player.timed_out = True
        return (
            None  # Do not return an error message so participants proceed in any case
        )


class WaitForEveryone(SynchronizingWait):

    synchronize = "session"

    @classmethod
    def show(page, player):
        return not player.timed_out

    @classmethod
    def all_here(page, session):
        # Get all players and sort alphabetically by name
        # all_players = sorted(players(session), key=lambda p: p.name)
        players_not_timed_out = [p for p in players(session) if not p.timed_out]
        all_players = sorted(players_not_timed_out, key=lambda p: p.name)

        # Split into groups of size C.GROUP_SIZE
        groups = [
            all_players[i : i + C.GROUP_SIZE]
            for i in range(
                0, (len(all_players) // C.GROUP_SIZE) * C.GROUP_SIZE, C.GROUP_SIZE
            )
        ]
        create_groups(session, groups)
        players_grouped = [p for p in players(session) if p.group]
        for p in players_grouped:
            p.grouped = True
            p.group.dropped_out = False


class TimedOutBeforeGrouping(Page):

    @classmethod
    def show(page, player):
        return player.timed_out

    @classmethod
    def after_once(page, player):
        move_to_end(player)


class NoGroupAssigned(Page):

    @classmethod
    def show(page, player):
        return not player.grouped

    @classmethod
    def after_once(page, player):
        move_to_end(player)


class ShowGroup(Page):

    @classmethod
    def show(page, player):
        return player.grouped and not player.timed_out and not player.group.dropped_out

    @classmethod
    def timeout(page, player):
        return 45

    @classmethod
    def timeout_reached(page, player):
        player.timed_out = True
        player.group.dropped_out = True

    @classmethod
    def context(page, player):
        num_groups = 0
        if player.group:
            group_members = sorted(players(player.group), key=lambda p: p.name)
            group_name = player.group.name
            num_groups = len(players(player.session)) // C.GROUP_SIZE
        else:
            # Set values for the surplus participants
            group_members = []
            group_name = None
        return dict(
            group_name=group_name,
            group_members=group_members,
            num_groups=num_groups,
        )

    @classmethod
    def fields(page, player):
        return {
            "abort": BooleanField(label="Abort after this page."),
        }

    @classmethod
    def validate(page, player, data):
        if data.get("abort"):
            player.timed_out = True
            player.group.dropped_out = True
        return (
            None  # Do not return an error message so participants proceed in any case
        )


class KeepGroupInSync(SynchronizingWait):

    @classmethod
    def show(page, player):
        return player.grouped


class TimedOutGroupPhase(Page):

    @classmethod
    def show(page, player):
        return player.grouped and (player.timed_out or player.group.dropped_out)

    @classmethod
    def after_once(page, player):
        move_to_end(player)


class AllGood(Page):

    @classmethod
    def show(page, player):
        return player.grouped and not player.timed_out and not player.group.dropped_out


# PAGE ORDER


page_order = [
    PageWithTimeout,
    WaitForEveryone,
    TimedOutBeforeGrouping,
    NoGroupAssigned,
    Rounds(ShowGroup, KeepGroupInSync, n=3),
    TimedOutGroupPhase,
    AllGood,
]
