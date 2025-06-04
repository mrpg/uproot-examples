import colorsys
import random

from uproot.smithereens import *
from uproot.types import Page


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
        await send_to(
            others_in_session(player),
            [
                dict(
                    points=points,
                    color=player.color,
                    lineWidth=lineWidth,
                ),
            ],
            "Strokes",
        )


page_order = [
    Draw,
]
