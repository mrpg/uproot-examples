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

DESCRIPTION = "Typed, append-only data with uproot.models"


class Rating(metaclass=um.Entry):
    """One entry in the custom model."""

    player: PlayerIdentifier
    item: str
    score: int


def new_session(session: SessionType) -> None:
    """Create one model shared by all players in the session."""
    session.ratings = um.create_model(session, tag="ratings")


def rating_data(player: PlayerType) -> dict[str, Any]:
    """Return this player's entries plus the size of the shared model."""
    model = player.session.ratings
    player_ratings = um.filter_entries(model, Rating, player=player.pid)
    ratings = [
        {
            "id": str(entry_id),
            "created_at": timestamp,
            "item": rating.item,
            "score": rating.score,
        }
        for entry_id, timestamp, rating in player_ratings
    ]

    return {
        "ratings": ratings,
        "session_count": len(um.get_entries(model, Rating)),
    }


class Ratings(Page):
    @classmethod
    def jsvars(page, player: PlayerType) -> dict[str, Any]:
        return {"rating_data": rating_data(player)}

    @live
    def get_rating_data(page, player: PlayerType) -> dict[str, Any]:
        return rating_data(player)

    @live
    def add_rating(
        page,
        player: PlayerType,
        item: str,
        score: int,
    ) -> dict[str, Any]:
        item = item.strip()

        if not item or len(item) > 80:
            return {**rating_data(player), "error": "Enter an item of 1–80 characters."}

        if not 1 <= score <= 10:
            return {**rating_data(player), "error": "Score must be between 1 and 10."}

        # Identifier fields such as Rating.player are filled automatically.
        entry_id = um.add_entry(
            player.session.ratings,
            player.pid,
            Rating,
            item=item,
            score=score,
        )
        notify(
            player,
            player.session.players,
            {"id": str(entry_id)},
            event="RatingAdded",
            where=...,
        )

        return rating_data(player)


page_order = [
    Ratings,
]
