# Docs are available at https://uproot.science/
# Examples are available at https://github.com/mrpg/uproot-examples
#
# This example app is under the 0BSD license. You can use it freely and build on it
# without any limitations and without any attribution. However, these two lines must be
# preserved in any uproot app (the license file is automatically installed in projects):
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt

from time import time

from uproot.smithereens import *

DESCRIPTION = "Session-wide timeout followed by code run by the first arrival"
LANDING_PAGE = False


class C:
    WAIT_SECONDS = 30.0


class SharedDeadline(Page):
    @classmethod
    def ensure_deadline(page, player: PlayerType) -> None:
        session = player.session

        if session.get("sessionwide_timeout_until") is None:
            session.sessionwide_timeout_until = time() + C.WAIT_SECONDS

    @classmethod
    def timeout(page, player: PlayerType) -> float:
        page.ensure_deadline(player)

        return float(max(0, player.session.sessionwide_timeout_until - time()))

    @classmethod
    def may_proceed(page, player: PlayerType) -> bool:
        page.ensure_deadline(player)

        return bool(time() >= player.session.sessionwide_timeout_until)


class FirstArrivalRunsCode(Page):
    @classmethod
    def run_for_session(page, session: SessionType) -> None:
        players = list(session.players)

        for position, player in enumerate(players, start=1):
            player.sessionwide_position = position

        session.sessionwide_timeout_player_count = len(players)

    @classmethod
    def before_always_once(page, player: PlayerType) -> None:
        session = player.session

        if session.get("sessionwide_timeout_code_ran", False):
            return

        page.run_for_session(session)
        session.sessionwide_timeout_first_arrival = player.name
        session.sessionwide_timeout_code_ran = True


page_order = [
    SharedDeadline,
    FirstArrivalRunsCode,
]
