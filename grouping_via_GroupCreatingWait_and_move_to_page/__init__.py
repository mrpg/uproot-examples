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

DESCRIPTION = """Wait for all participants in the session, then create groups of identical size C.GROUP_SIZE and notify surplus participants that they could not be grouped. Hence, to test this app, run it with a number of participants that is not a multiple of C.GROUP_SIZE."""


# CONSTANTS


class C:
    """Constants"""

    GROUP_SIZE = 3


# FUNCTIONS


def new_player(player):
    """Initialize variables."""

    player.could_not_be_grouped = False
    player.timed_out = False
    player.timed_out_before_grouping = False
    player.withdrew_consent = False


# PAGES


class PageWithTimeLimit(Page):
    """A page with a time limit, like you would use it in an online study with interaction between participants, so that active participants do not have to wait indefinitely for slow/inattentive/inactive participants"""

    @classmethod
    def timeout(page, player):
        return 30

    @classmethod
    def timeout_reached(page, player):
        player.timed_out_before_grouping = True
        move_to_page(player, DropoutInfo)

    @classmethod
    def fields(page, player):
        return {
            "refuse": BooleanField(label="Refuse to participate."),
        }

    @classmethod
    def validate(page, player, data):
        if data.get("refuse"):
            player.withdrew_consent = True
            move_to_page(player, DropoutInfo)


class WaitForEveryone(SynchronizingWait):
    """Wait for everyone, so group formation is independent of participants’ speed of progress"""

    synchronize = "session"


class CreateGroups(GroupCreatingWait):
    """Create groups for everyone who has not withdrawn consent and who has not timed out"""

    group_size = C.GROUP_SIZE

    @classmethod
    def timeout(page, player):
        return 120  # Make sure this is long enough – in particular, if not using WaitForEveryone!

    @classmethod
    def timeout_reached(page, player):
        player.could_not_be_grouped = True
        move_to_page(player, DropoutInfo)

    @classmethod
    def after_grouping(page, group):
        group.dropped_out = False


class ShowGroup(Page):
    """Page shown only to grouped participants"""

    @classmethod
    def before_once(page, player):
        if player.could_not_be_grouped or player.group.dropped_out:
            move_to_page(player, DropoutInfo)

    @classmethod
    def timeout(page, player):
        return 60

    @classmethod
    def timeout_reached(page, player):
        player.timed_out = True
        player.group.dropped_out = True

    @classmethod
    def templatevars(page, player):
        group_members = sorted(players(player.group), key=lambda p: p.name)
        num_groups = (
            len(
                [
                    p
                    for p in players(player.session)
                    if not p.withdrew_consent and not p.timed_out_before_grouping
                ]
            )
            // C.GROUP_SIZE
        )
        return dict(
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

    @classmethod
    def after_once(page, player):
        if player.timed_out:
            move_to_page(player, DropoutInfo)
            for p in players(player.group):
                with p as pp:
                    move_to_page(pp, DropoutInfo)


class KeepGroupInSync(SynchronizingWait):
    """Let all players in a group proceed to the next round simultaneously"""

    pass


class AllGood(Page):
    """Page shown after group phase has finished without any issues"""

    @classmethod
    def after_once(page, player):
        move_to_end(player)


class DropoutInfo(Page):
    """Page shown to participants who dropped out for various reasons"""

    @classmethod
    def after_once(page, player):
        move_to_end(player)


# PAGE ORDER


page_order = [
    PageWithTimeLimit,
    # WaitForEveryone,  # Use if you want group formation to be independent of participants’ speed of progress
    CreateGroups,
    Rounds(
        ShowGroup,
        KeepGroupInSync,
        n=3,
    ),
    AllGood,
    DropoutInfo,
]
