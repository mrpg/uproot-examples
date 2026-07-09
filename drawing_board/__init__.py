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
from typing import Any

import uproot.models as um
from uproot.smithereens import *
from uproot.types import Page

DESCRIPTION = "An interactive drawing board"


class Stroke(metaclass=um.Entry):
    """
    Represents a drawing stroke on the board

    Attributes:
        pid: Player who created the stroke
        points: List of coordinate points making up the stroke
        color: Hex color code for the stroke
        lineWidth: Width of the stroke line
    """

    pid: PlayerIdentifier
    points: list[dict[str, Any]]
    color: str
    lineWidth: int


def new_session(session: SessionType) -> None:
    """Initialize session with strokes model"""
    session.strokes = um.create_model(session, tag="strokes")


def get_all_strokes(strokes_model: ModelIdentifier) -> list[dict[str, Any]]:
    """
    Retrieve all strokes from the model

    Args:
        strokes_model: Model containing all strokes

    Returns:
        List of stroke dictionaries with points, color, and lineWidth
    """
    strokes = []
    for _, _, entry in um.filter_entries(strokes_model, Stroke):
        strokes.append(
            {
                "points": entry.points,
                "color": entry.color,
                "lineWidth": entry.lineWidth,
            }
        )
    return strokes


def generate_visible_hex() -> str:
    color_rng = rng()
    hue = color_rng.random()
    saturation = color_rng.random()
    lightness = 0.6 * color_rng.random()

    rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
    return "#{:02x}{:02x}{:02x}".format(
        int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
    )


def new_player(player: PlayerType) -> None:
    player.color = generate_visible_hex()


class Draw(Page):
    @classmethod
    async def jsvars(page, player: PlayerType) -> dict[str, Any]:
        return dict(
            color=player.color,
            strokes=get_all_strokes(player.session.strokes),
        )

    @live
    def stroke(
        page, player: PlayerType, points: list[dict[str, Any]], lineWidth: int
    ) -> None:
        # Save stroke to the model
        um.auto_add_entry(
            player.session.strokes,
            player,
            Stroke,
            points=points,
            color=player.color,
            lineWidth=lineWidth,
        )

        # Broadcast to other players
        notify(
            player,
            player.others_in_session,
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
