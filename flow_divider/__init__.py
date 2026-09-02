# Docs are available at https://uproot.science/
# Examples are available at https://github.com/mrpg/uproot-examples
#
# This example app is under the 0BSD license. You can use it freely and build on it
# without any limitations and without any attribution. However, these two lines must be
# preserved in any uproot app (the license file is automatically installed in projects):
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt

from uproot.constraints import valid_token
from uproot.fields import *
from uproot.smithereens import *

DESCRIPTION = "Send players to rooms in round-robin order"
LANDING_PAGE = False


class C:
    pass


def get_room_names(session: SessionType) -> list[str]:
    room_names = session.settings.get("room_names")

    if not isinstance(room_names, list) or not room_names:
        raise TypeError("room_names must be a non-empty list of strings")

    if not all(
        isinstance(room_name, str) and room_name and valid_token(room_name)
        for room_name in room_names
    ):
        raise TypeError("room_names must contain only valid room-name strings")

    return cast(list[str], room_names)


def new_player(player: PlayerType) -> None:
    room_names = get_room_names(player.session)
    player.room_name = room_names[player.id % len(room_names)]


class Redirect(Page):
    pass


page_order = [
    Redirect,
]
