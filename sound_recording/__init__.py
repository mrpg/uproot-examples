# Docs are available at https://uproot.science/
# Examples are available at https://github.com/mrpg/uproot-examples
#
# This example app is under the 0BSD license. You can use it freely and build on it
# without any limitations and without any attribution. However, these two lines must be
# preserved in any uproot app (the license file is automatically installed in projects):
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt

import base64

from uproot.fields import *
from uproot.smithereens import *
from uproot.types import Page

DESCRIPTION = "Record audio of yourself reading a sentence"


class C:
    SENTENCE = (
        "I caught this morning morning's minion, kingdom"
        " of daylight's dauphin, dapple-dawn-drawn Falcon in his riding."
    )


class Record(Page):
    fields = dict(
        audio=FileField(
            label="Your recording",
        ),
    )

    @classmethod
    async def handle_stealth_fields(page, player, data):
        audio = data["audio"]
        contents = await audio.read()

        # uproot supports storing bytes directly in the database.
        # NOTE: This will grow the database quickly with many participants!

        player.audio = contents
        player.audio_content_type = audio.content_type


class Playback(Page):
    allow_back = True

    @classmethod
    async def templatevars(page, player):
        return dict(
            audio_src=data_uri(player.audio),
        )


page_order = [Record, Playback]
