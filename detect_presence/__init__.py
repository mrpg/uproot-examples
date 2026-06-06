# Docs are available at https://uproot.science/
# Examples are available at https://github.com/mrpg/uproot-examples
#
# This example app is under the 0BSD license. You can use it freely and build on it
# without any limitations and without any attribution. However, these two lines must be
# preserved in any uproot app (the license file is automatically installed in projects):
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt

from time import time as now

from uproot.fields import *
from uproot.smithereens import *

DESCRIPTION = "Detect who is actually present (useful for classroom experiments)"
LANDING_PAGE = False


class C:
    DETECTION_PERIOD = 60.0


class Context(PlayerContext):
    @property
    def present(self):
        return [p for p in self.player.session.players if p.get("present", False)]


class RaiseHands(Page):
    # IMPORTANT: If you have multiple rounds, or otherwise reuse this pattern, you
    # must ensure that player.session.detection_period_until gets reset to None.
    # You do not need to manually invoke RaiseHands.reset_session, however.

    @classmethod
    def reset_session(page, player):
        for p in player.session.players:
            p.present = False

    @classmethod
    def ensure_detection(page, player):
        if player.session.get("detection_period_until") is None:
            # This player was here first
            player.session.detection_period_until = now() + C.DETECTION_PERIOD
            page.reset_session(player)

    @classmethod
    def show(page, player):
        return player.session.get(
            "detection_period_until"
        ) is None or not page.may_proceed(player)

    @classmethod
    def timeout(page, player):
        page.ensure_detection(player)

        return player.session.detection_period_until - now()

    @classmethod
    def before_once(page, player):
        page.ensure_detection(player)

    @classmethod
    def may_proceed(page, player):
        return now() >= player.session.detection_period_until

    @live
    def set_presence(page, player, new_value: bool):
        if player.get("present", False):
            return True

        player.present = new_value

        if new_value and all(p.get("present", False) for p in player.session.players):
            player.session.detection_period_until = now()
            notify(player, player.session.players)

        return new_value


# Other pages can now use player.present to check whether a player actually is
# present, e.g., in show(). Note: The use of player.get("present", False) is
# recommended, as it falls back to a sensible default instead of raising an
# Exception, should player.present be unset.


class Info(Page):
    @classmethod
    def before_once(page, player):
        # Optional: Create a group of all present players. Players who arrive a bit
        # later are added to the pre-existing group. Remove this method (and the
        # corresponding template block) if grouping is not needed.

        # IMPORTANT: The group that is created may be "incomplete" when checked on this
        # page. Make sure to wait for a sufficient amount of time if your logic needs
        # to ensure that the group really consists of all present players.

        if not player.get("present", False):
            return

        session = player.session
        group = session.get("presence_group")

        if group is None:
            # First present player: create the group
            session.presence_group = create_group(session, [player])
        else:
            # Group already exists: add this player to it
            add_to_group(session.group(group), player)


page_order = [
    RaiseHands,
    Info,
]
