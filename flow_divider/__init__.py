# Docs are available at https://uproot.science/
# Examples are available at https://github.com/mrpg/uproot-examples
#
# This example app is under the 0BSD license. You can use it freely and build on it
# without any limitations and without any attribution. However, these two lines must be
# preserved in any uproot app (the license file is automatically installed in projects):
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt

from collections.abc import Mapping

import uproot.deployment as d
from uproot.constraints import valid_token
from uproot.fields import *
from uproot.smithereens import *

DESCRIPTION = "Send players to rooms in round-robin order"
LANDING_PAGE = False


class C:
    pass


def get_room_names(settings: Mapping[str, Any]) -> list[str]:
    room_names = settings.get("room_names")

    if not isinstance(room_names, list) or not room_names:
        raise ValueError("room_names must be a non-empty list of strings")

    if not all(
        isinstance(room_name, str) and room_name and valid_token(room_name)
        for room_name in room_names
    ):
        raise ValueError("room_names must contain only valid room-name strings")

    return cast(list[str], room_names)


def admin_settings_context(
    admin: AdminType,
    config: str,
    settings: dict[str, Any],
) -> dict[str, Any]:
    return {
        "available_room_names": [] if d.PUBLIC_DEMO else sorted(admin.rooms),
        "room_names_hidden": d.PUBLIC_DEMO,
    }


def validate_session_settings(
    admin: AdminType,
    config: str,
    settings: dict[str, Any],
) -> None:
    room_names = get_room_names(settings)
    missing = [room_name for room_name in room_names if room_name not in admin.rooms]

    if missing:
        raise ValueError(
            "Destination rooms do not exist: " + ", ".join(sorted(set(missing)))
        )


def new_player(player: PlayerType) -> None:
    room_names = get_room_names(player.session.settings)
    player.room_name = room_names[player.id % len(room_names)]


class Redirect(Page):
    pass


page_order = [
    Redirect,
]
