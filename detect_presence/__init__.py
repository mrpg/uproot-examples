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
    DETECTION_PERIOD = 30.0


class Context(PlayerContext):
    @property
    def present(self):
        return [p for p in self.player.session.players if p.present]


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
        player.present = new_value

        return new_value


# Other pages can now use player.present to check whether a player actually is
# present, e.g., in show().


class Info(Page):
    pass


page_order = [
    RaiseHands,
    Info,
]
