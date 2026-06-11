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

DESCRIPTION = "Bomb Risk Elicitation Task (Crosetto & Filippin, 2013)"
LANDING_PAGE = False


class C:
    ROWS = 5
    COLS = 5
    NUM_BOXES = ROWS * COLS
    BOX_VALUE = 1  # $ per collected box


class Choose(Page):
    fields = dict(
        collected=IntegerField(
            default=0,
            min=0,
            max=C.NUM_BOXES,
            class_wrapper="d-none",
        ),
    )

    @classmethod
    def after_once(page, player):
        player.bomb_position = rng().randint(1, C.NUM_BOXES)
        player.exploded = player.bomb_position <= player.collected
        player.payoff = cu(0) if player.exploded else cu(C.BOX_VALUE * player.collected)


class Results(Page):
    pass


def pipeline(session):
    rows = []

    for player in session.players:
        player_data = player.within(app=__name__)
        collected = player_data.get("collected")

        if collected is not None:
            rows.append(
                {
                    "session": session.name,
                    "uname": player.name,
                    "collected": collected,
                    "bomb_position": player_data.get("bomb_position"),
                    "exploded": player_data.get("exploded"),
                    "payoff": player_data.get("payoff"),
                }
            )

    return rows


page_order = [
    Choose,
    Results,
]
