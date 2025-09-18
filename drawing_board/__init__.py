# Docs are available at https://uproot.science/
# Examples are available at https://github.com/mrpg/uproot-examples
#
# This example app is under the 0BSD license. You can use it freely and build on it
# without any limitations and without any attribution. However, these two lines must be
# preserved in any uproot app (the license file is automatically installed in projects):
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt

import colorsys
import random

from uproot.smithereens import *
from uproot.types import Page

DESCRIPTION = "An interactive drawing board"


def generate_visible_hex():
    hue = random.random()
    saturation = random.random()
    lightness = 0.6 * random.random()

    rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
    return "#{:02x}{:02x}{:02x}".format(
        int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
    )


def new_player(player):
    player.color = generate_visible_hex()


class Draw(Page):
    @classmethod
    async def jsvars(page, player):
        return dict(color=player.color)

    @live
    async def stroke(page, player, points: list[dict], lineWidth: int, **kwargs):
        notify(
            player,
            others_in_session(player),
            [
                dict(
                    points=points,
                    color=player.color,
                    lineWidth=lineWidth,
                ),
            ],
            event="Strokes",
        )


page_order = [
    Draw,
]
