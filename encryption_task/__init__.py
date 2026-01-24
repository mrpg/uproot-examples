# Docs are available at https://uproot.science/
# Examples are available at https://github.com/mrpg/uproot-examples
#
# This example app is under the 0BSD license. You can use it freely and build on it
# without any limitations and without any attribution. However, these two lines must be
# preserved in any uproot app (the license file is automatically installed in projects):
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt

import random
import string

from uproot.fields import *
from uproot.smithereens import *

DESCRIPTION = "Encryption task (Erkal et al., 2011)"
LANDING_PAGE = False


class C:
    # All 26 letters are shown in the table
    CHARSET = tuple(string.ascii_uppercase)
    # Only the first N letters (after shuffling) are used for puzzles
    # This makes it easier to scan the table
    ACTIVE_LETTERS = 13
    # Length of strings to decrypt
    WORD_LENGTH = 6
    # Duration in seconds
    DURATION = 120
    # Table mode: "fixed" = same table throughout, "random" = new table each puzzle
    TABLE_MODE = "fixed"
    # Random seed (set to None for different puzzles per player)
    SEED = 0x1337

    __export__ = ["WORD_LENGTH", "DURATION", "TABLE_MODE"]


def new_player(player):
    player.table_letters = None  # Shuffled alphabet
    player.table_digits = None  # Corresponding digits
    player.puzzle = None  # Current word to decode
    player.solution = None  # Correct answer
    player.solved = 0
    player.rng = random.Random(C.SEED)


def generate_table(rng: random.Random) -> tuple[str, str]:
    """Generate a random letter-to-digit mapping for all 26 letters.

    Returns:
        (letters, digits) - e.g., ("QWERTY...", "3829...")
    """
    # Shuffle the alphabet
    letters = list(C.CHARSET)
    rng.shuffle(letters)
    # Each letter maps to a random digit (0-9)
    digits = [str(rng.randint(0, 9)) for _ in range(len(C.CHARSET))]

    return "".join(letters), "".join(digits)


def generate_word(rng: random.Random, table_letters: str) -> str:
    """Generate a puzzle word using only the first ACTIVE_LETTERS of the table."""
    active = table_letters[: C.ACTIVE_LETTERS]
    return "".join(rng.choices(active, k=C.WORD_LENGTH))


def decrypt(word: str, table_letters: str, table_digits: str) -> str:
    """Decrypt a word using the table mapping."""
    mapping = dict(zip(table_letters, table_digits))
    return "".join(mapping[c] for c in word)


class Encryption(Page):
    timeout = C.DURATION

    @live
    async def get_puzzle(page, player):
        """Get the current puzzle (generates new table/word if needed)."""
        if player.table_letters is None or C.TABLE_MODE == "random":
            # Generate new table
            player.table_letters, player.table_digits = generate_table(player.rng)

        # Always generate a new word
        player.puzzle = generate_word(player.rng, player.table_letters)
        player.solution = decrypt(
            player.puzzle, player.table_letters, player.table_digits
        )

        # Split table into two rows for display (first 13 and last 13 letters)
        return {
            "table_letters_1": player.table_letters[: C.ACTIVE_LETTERS],
            "table_digits_1": player.table_digits[: C.ACTIVE_LETTERS],
            "table_letters_2": player.table_letters[C.ACTIVE_LETTERS :],
            "table_digits_2": player.table_digits[C.ACTIVE_LETTERS :],
            "puzzle": player.puzzle,
        }

    @live
    async def submit_answer(page, player, answer: str):
        """Check the answer and return result."""
        if player.solution is None:
            return {"correct": False, "message": "No puzzle loaded"}

        if answer == player.solution:
            player.solved += 1
            return {"correct": True}

        return {"correct": False, "message": "Incorrect. Try again."}


class Results(Page):
    pass


page_order = [
    Encryption,
    Results,
]
