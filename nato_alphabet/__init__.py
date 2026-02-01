# Docs are available at https://uproot.science/
# Examples are available at https://github.com/mrpg/uproot-examples
#
# This example app is under the 0BSD license. You can use it freely and build on it
# without any limitations and without any attribution. However, these two lines must be
# preserved in any uproot app (the license file is automatically installed in projects):
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt

import json
import random
import string
import sys
from io import BytesIO

from fastapi.responses import Response
from uproot.fields import *
from uproot.smithereens import *

DESCRIPTION = "NATO alphabet transcription task (Gibson, 2025)"
LANDING_PAGE = False

with open("nato_alphabet/_static/lengths.json") as f:
    WAVLENGTHS = json.load(f)


class C:
    WORD_LENGTH = 4
    SECONDS = 6.0  # Audio length per word
    SEED = 0x1337

    __export__ = ["WORD_LENGTH"]


def new_session(session):
    try:
        import audioop

        import pydub
    except ImportError:
        raise RuntimeError(
            "This app requires 'pydub' and 'audioop-lts'. Install via pip/uv."
        )


def new_player(player):
    player.rng = random.Random(C.SEED)
    player.current_word = None
    player.solved = 0


def generate_wav(letters: str):
    from pydub import AudioSegment

    intermediate = AudioSegment.silent(
        duration=1000
        * (C.SECONDS - 0.6 - 0.1 - sum(WAVLENGTHS[ch] for ch in letters))
        / (len(letters) - 1)
    )

    combined = AudioSegment.empty()
    combined += AudioSegment.silent(duration=500)

    for i, ch in enumerate(letters):
        if i > 0:
            combined += intermediate

        combined += AudioSegment.from_wav(f"nato_alphabet/_static/{ch}.wav")

    combined += AudioSegment.silent(duration=100)

    return combined


def generate_word(rng: random.Random) -> str:
    return "".join(rng.choice(string.ascii_uppercase) for _ in range(C.WORD_LENGTH))


class Transcribe(Page):
    @live
    async def ensure_word(page, player):
        if player.get("current_word") is None:
            player.current_word = generate_word(player.rng)

    @live
    async def get_audio(page, player):
        buffer = BytesIO()

        result = generate_wav(player.current_word)
        result.export(buffer, format="wav")

        return data_uri(buffer.getvalue())

    @live
    async def submit_answer(page, player, answer: str):
        """Check the answer and return result."""
        if player.current_word is None:
            return {
                "correct": False,
                "message": "No word loaded",
            }

        # Normalize: uppercase and strip whitespace
        answer = answer.strip().upper()

        # Validate: must be exactly WORD_LENGTH uppercase letters A-Z
        if len(answer) != C.WORD_LENGTH:
            return {
                "correct": False,
                "message": f"Answer must be {C.WORD_LENGTH} letters",
            }

        if not answer.isalpha():
            return {
                "correct": False,
                "message": "Answer must contain only letters A-Z",
            }

        if answer == player.current_word:
            player.solved += 1
            player.current_word = generate_word(player.rng)

            return {
                "correct": True,
                "new_word": True,
            }

        return {
            "correct": False,
            "message": "Incorrect. Try again.",
        }


class Results(Page):
    pass


page_order = [
    Transcribe,
    Results,
]
