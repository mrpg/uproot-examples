# Docs are available at https://uproot.science/
# Examples are available at https://github.com/mrpg/uproot-examples
#
# This example app is under the 0BSD license. You can use it freely and build on it
# without any limitations and without any attribution. However, these two lines must be
# preserved in any uproot app (the license file is automatically installed in projects):
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt

"""
Conjoint Experiment

Participants compare randomly generated profiles (study abroad destinations)
and choose their preferred option. Each pair has 7 randomized attributes.
Profiles are presented one pair at a time using live WebSocket communication.
"""

import random

import uproot.models as um
from uproot.smithereens import *

DESCRIPTION = "Conjoint experiment (study abroad destinations)"
LANDING_PAGE = False


class C:
    DEFAULT_N_PAIR = 5

    HAS_BEACHES = [True, False]
    ENGLISH = [True, False]
    ACCOMMODATION = [True, False]
    PARTYING = [True, False]
    SUNNY = [True, False]
    GRADING = [1, 2, 3]
    COSTS = [-1, 0, 1]

    PROFILE_ATTRS = [
        "has_beaches",
        "english",
        "accommodation",
        "partying",
        "sunny",
        "grading",
        "costs",
    ]


class Profile(metaclass=um.Entry):
    """A single destination profile (one side of a comparison pair)."""

    pid: PlayerIdentifier
    pair_id: int
    side: int  # 0 = left (Option A), 1 = right (Option B)
    has_beaches: bool
    english: bool
    accommodation: bool
    partying: bool
    sunny: bool
    grading: int
    costs: int


class Preference(metaclass=um.Entry):
    """Records which side the player preferred for a given pair."""

    pid: PlayerIdentifier
    pair_id: int
    preferred_side: int  # 0 = left, 1 = right


def new_session(session):
    session.profiles = um.create_model(session, tag="profiles")
    session.preferences = um.create_model(session, tag="preferences")


def new_player(player):
    player.current_pair = 0


def generate_profile():
    return dict(
        has_beaches=random.choice(C.HAS_BEACHES),
        english=random.choice(C.ENGLISH),
        accommodation=random.choice(C.ACCOMMODATION),
        partying=random.choice(C.PARTYING),
        sunny=random.choice(C.SUNNY),
        grading=random.choice(C.GRADING),
        costs=random.choice(C.COSTS),
    )


class Choice(Page):
    @classmethod
    def may_proceed(page, player):
        return player.current_pair >= player.session.settings.get(
            "n_pairs",
            C.DEFAULT_N_PAIR,
        )

    @classmethod
    def before_once(page, player):
        """Generate all profile pairs for this player."""
        for pair_id in range(
            player.session.settings.get(
                "n_pairs",
                C.DEFAULT_N_PAIR,
            )
        ):
            for side in (0, 1):
                attrs = generate_profile()
                um.add_entry(
                    player.session.profiles,
                    player,
                    Profile,
                    pair_id=pair_id,
                    side=side,
                    **attrs,
                )

    @live
    async def get_pair(page, player):
        """Get the current pair of profiles, or signal done."""
        pair_id = player.current_pair
        if pair_id >= player.session.settings.get(
            "n_pairs",
            C.DEFAULT_N_PAIR,
        ):
            return {"type": "done"}

        left = None
        right = None
        for _, _, entry in um.filter_entries(
            player.session.profiles, Profile, pid=player.pid, pair_id=pair_id
        ):
            if entry.side == 0:
                left = entry
            else:
                right = entry

        def profile_dict(entry):
            return {attr: getattr(entry, attr) for attr in C.PROFILE_ATTRS}

        return {
            "type": "pair",
            "left": profile_dict(left),
            "right": profile_dict(right),
            "current": pair_id + 1,
            "total": player.session.settings.get(
                "n_pairs",
                C.DEFAULT_N_PAIR,
            ),
        }

    @live
    async def submit_choice(page, player, side: int):
        """Record the player's choice and advance to the next pair."""
        if side not in (0, 1):
            return {"type": "error"}

        pair_id = player.current_pair
        if pair_id >= player.session.settings.get(
            "n_pairs",
            C.DEFAULT_N_PAIR,
        ):
            return {"type": "done"}

        # Check for duplicate submission
        for _, _, entry in um.filter_entries(
            player.session.preferences,
            Preference,
            pid=player.pid,
            pair_id=pair_id,
        ):
            # Already recorded, skip
            break
        else:
            um.add_entry(
                player.session.preferences,
                player,
                Preference,
                pair_id=pair_id,
                preferred_side=side,
            )

        player.current_pair = pair_id + 1

        # Return next pair or done
        if player.current_pair >= player.session.settings.get(
            "n_pairs",
            C.DEFAULT_N_PAIR,
        ):
            return {"type": "done"}

        left = None
        right = None
        for _, _, entry in um.filter_entries(
            player.session.profiles,
            Profile,
            pid=player.pid,
            pair_id=player.current_pair,
        ):
            if entry.side == 0:
                left = entry
            else:
                right = entry

        def profile_dict(entry):
            return {attr: getattr(entry, attr) for attr in C.PROFILE_ATTRS}

        return {
            "type": "pair",
            "left": profile_dict(left),
            "right": profile_dict(right),
            "current": player.current_pair + 1,
            "total": player.session.settings.get(
                "n_pairs",
                C.DEFAULT_N_PAIR,
            ),
        }


page_order = [
    Choice,
]
