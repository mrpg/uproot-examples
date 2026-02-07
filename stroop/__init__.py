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
Stroop Task

A classic cognitive psychology task where participants identify the ink color
of color words. In congruent trials, word and color match (e.g., "RED" in red).
In incongruent trials, they differ (e.g., "RED" in blue).

Each trial measurement is stored in a separate model entry.
Time is measured on the client side to avoid network latency effects.
"""

from random import Random as Random_

import uproot.models as um
from uproot.fields import *
from uproot.smithereens import *

DESCRIPTION = "Stroop task"
LANDING_PAGE = False

# Configuration
NUM_TRIALS = 12
COLORS = ["red", "green", "blue", "yellow"]


class Trial(metaclass=um.Entry):
    """
    Represents a single Stroop trial measurement.

    Attributes:
        pid: Player who completed this trial
        trial_number: Sequential trial number (1-indexed)
        word: The color word displayed (e.g., "RED")
        ink_color: The actual color of the text (e.g., "blue")
        congruent: True if word matches ink_color
        response: The participant's response (color they chose)
        correct: Whether the response matched the ink color
        reaction_time_ms: Time from stimulus onset to response (client-measured)
    """

    pid: PlayerIdentifier
    trial_number: int
    word: str
    ink_color: str
    congruent: bool
    response: str
    correct: bool
    reaction_time_ms: float


def new_session(session):
    """Initialize session with trial data model."""
    session.trials = um.create_model(session, tag="trials")


def new_player(player):
    """Initialize player state."""
    player.current_trial = 0
    player.rng = Random_()


def generate_trial_sequence(rng: Random_, n_trials: int) -> list[dict]:
    """
    Generate a balanced sequence of congruent and incongruent trials.

    Returns a list of trial specifications with word, ink_color, and congruent flag.
    """
    trials = []

    # Create equal numbers of congruent and incongruent trials
    n_congruent = n_trials // 2
    n_incongruent = n_trials - n_congruent

    # Generate congruent trials (word matches color)
    for _ in range(n_congruent):
        color = rng.choice(COLORS)
        trials.append(
            {
                "word": color.upper(),
                "ink_color": color,
                "congruent": True,
            }
        )

    # Generate incongruent trials (word differs from color)
    for _ in range(n_incongruent):
        word_color = rng.choice(COLORS)
        ink_color = rng.choice([c for c in COLORS if c != word_color])
        trials.append(
            {
                "word": word_color.upper(),
                "ink_color": ink_color,
                "congruent": False,
            }
        )

    rng.shuffle(trials)
    return trials


class Instructions(Page):
    """Instructions page explaining the Stroop task."""

    pass


class Stroop(Page):
    """
    Main Stroop task page.

    Trials are presented one at a time. The participant sees a color word
    displayed in a (possibly different) ink color and must identify the
    ink color as quickly and accurately as possible.

    Time is measured on the client side using performance.now() for accuracy.
    """

    @classmethod
    def may_proceed(page, player):
        """Only allow proceeding after all trials are completed."""
        return player.current_trial >= NUM_TRIALS

    @classmethod
    def before_once(page, player):
        """Generate the trial sequence for this player."""
        player.trial_sequence = generate_trial_sequence(player.rng, NUM_TRIALS)

    @live
    async def get_state(page, player):
        """Get current trial state (called on page load)."""
        # Count completed trials from model
        completed_count = 0
        for _, _, entry in um.filter_entries(
            player.session.trials,
            Trial,
            pid=player.pid,
        ):
            completed_count += 1

        # Sync player.current_trial
        player.current_trial = completed_count

        return {
            "trials": player.trial_sequence,
            "colors": COLORS,
            "num_trials": NUM_TRIALS,
            "completed_trials": completed_count,
        }

    @live
    async def submit_response(
        page,
        player,
        trial_number: int,
        response: str,
        reaction_time_ms: float,
    ):
        """
        Record a trial response.

        Args:
            trial_number: Which trial this response is for (1-indexed)
            response: The color the participant selected
            reaction_time_ms: Client-measured reaction time in milliseconds

        Returns:
            dict with 'correct' boolean and 'done' boolean
        """
        if trial_number < 1 or trial_number > NUM_TRIALS:
            raise ValueError(f"Invalid trial number: {trial_number}")

        # Check if this trial was already submitted (prevent duplicates on reload)
        existing = None
        for _, _, entry in um.filter_entries(
            player.session.trials,
            Trial,
            pid=player.pid,
            trial_number=trial_number,
        ):
            existing = entry
            break

        if existing:
            # Trial already recorded, return existing result
            done = trial_number >= NUM_TRIALS
            return {"correct": existing.correct, "done": done}

        trial_spec = player.trial_sequence[trial_number - 1]
        correct = response == trial_spec["ink_color"]

        # Store the trial data
        um.add_entry(
            player.session.trials,
            player,
            Trial,
            trial_number=trial_number,
            word=trial_spec["word"],
            ink_color=trial_spec["ink_color"],
            congruent=trial_spec["congruent"],
            response=response,
            correct=correct,
            reaction_time_ms=reaction_time_ms,
        )

        player.current_trial = trial_number
        done = trial_number >= NUM_TRIALS

        return {"correct": correct, "done": done}


class Results(Page):
    """Display results summary."""

    @classmethod
    async def jsvars(page, player):
        """Calculate and pass results to the template."""
        trials = [
            entry
            for _, _, entry in um.filter_entries(
                player.session.trials,
                Trial,
                pid=player.pid,
            )
        ]

        if not trials:
            return {
                "total_trials": 0,
                "correct_count": 0,
                "accuracy": 0,
                "mean_rt": 0,
                "congruent_rt": 0,
                "incongruent_rt": 0,
                "stroop_effect": 0,
            }

        correct_count = sum(1 for t in trials if t.correct)
        accuracy = (correct_count / len(trials)) * 100

        # Calculate mean reaction times
        all_rts = [t.reaction_time_ms for t in trials if t.correct]
        congruent_rts = [
            t.reaction_time_ms for t in trials if t.correct and t.congruent
        ]
        incongruent_rts = [
            t.reaction_time_ms for t in trials if t.correct and not t.congruent
        ]

        mean_rt = sum(all_rts) / len(all_rts) if all_rts else 0
        congruent_rt = sum(congruent_rts) / len(congruent_rts) if congruent_rts else 0
        incongruent_rt = (
            sum(incongruent_rts) / len(incongruent_rts) if incongruent_rts else 0
        )
        stroop_effect = incongruent_rt - congruent_rt

        return {
            "total_trials": len(trials),
            "correct_count": correct_count,
            "accuracy": round(accuracy, 1),
            "mean_rt": round(mean_rt, 1),
            "congruent_rt": round(congruent_rt, 1),
            "incongruent_rt": round(incongruent_rt, 1),
            "stroop_effect": round(stroop_effect, 1),
        }


page_order = [
    Instructions,
    Stroop,
    Results,
]
