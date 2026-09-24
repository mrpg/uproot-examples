# Docs are available at https://uproot.science/
# Examples are available at https://github.com/mrpg/uproot-examples
#
# This example app is under the 0BSD license. You can use it freely and build on it
# without any limitations and without any attribution. However, these two lines must be
# preserved in any uproot app (the license file is automatically installed in projects):
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt

from typing import Any

import uproot.models as um
from uproot.smithereens import *

DESCRIPTION = "Live message board with admin projection view"


class C:
    MAX_LENGTH = 280


class Post(metaclass=um.Entry):
    """One entry in the message board."""

    player: PlayerIdentifier
    body: str


def new_session(session: SessionType) -> None:
    session.board = um.create_model(session, tag="board")


def show_to_others(session: SessionType) -> bool:
    return bool(session.settings.get("show_to_others", False))


def all_posts(session: SessionType) -> list[dict[str, Any]]:
    entries = um.get_entries(session.board, Post)
    result = []

    for entry_id, timestamp, post in entries:
        with materialize(post.player) as p:
            player_id = p.id

        result.append(
            {
                "id": str(entry_id),
                "created_at": timestamp,
                "body": post.body,
                "player": player_id,
            }
        )

    result.reverse()

    return result


def player_posts(player: PlayerType) -> list[dict[str, Any]]:
    entries = um.filter_entries(player.session.board, Post, player=player.pid)

    return [
        {
            "id": str(entry_id),
            "created_at": timestamp,
            "body": post.body,
        }
        for entry_id, timestamp, post in entries
    ][::-1]


def board_data(player: PlayerType) -> dict[str, Any]:
    session = player.session
    own = player_posts(player)
    visible = show_to_others(session)

    return {
        "own": own,
        "all": all_posts(session) if visible else [],
        "show_to_others": visible,
        "total": len(um.get_entries(session.board, Post)),
    }


class Board(Page):
    @classmethod
    def jsvars(page, player: PlayerType) -> dict[str, Any]:
        return {"board_data": board_data(player)}

    @live
    def get_board_data(page, player: PlayerType) -> dict[str, Any]:
        return board_data(player)

    @live
    def add_post(page, player: PlayerType, body: str) -> dict[str, Any]:
        body = body.strip()

        if not body or len(body) > C.MAX_LENGTH:
            return {
                **board_data(player),
                "error": f"Enter a message of 1–{C.MAX_LENGTH} characters.",
            }

        entry_id = um.add_entry(
            player.session.board,
            player.pid,
            Post,
            body=body,
        )

        if show_to_others(player.session):
            notify(
                player,
                player.session.players,
                {"id": str(entry_id)},
                event="PostAdded",
                where=...,
            )

        return board_data(player)


def digest(session: SessionType) -> dict[str, Any]:
    posts = all_posts(session)

    return {"posts": posts, "total": len(posts)}


page_order = [
    Board,
]
