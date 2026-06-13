# Docs are available at https://uproot.science/
# Examples are available at https://github.com/mrpg/uproot-examples
#
# This example app is under the 0BSD license. You can use it freely and build on it
# without any limitations and without any attribution. However, these two lines must be
# preserved in any uproot app (the license file is automatically installed in projects):
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt

import asyncio

from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from uproot.smithereens import *

DESCRIPTION = "StreamingResponse through api2()"
LANDING_PAGE = False


def new_player(player):
    player.streaming_counter = 0


class Stream(Page):
    pass


async def counter_stream(sname, uname):
    for _ in range(10):
        await asyncio.sleep(1)

        with Player(sname, uname) as player:
            player.streaming_counter = player.get("streaming_counter", 0) + 1
            value = player.streaming_counter

        yield f"data: {value}\n\n"

    yield "event: done\ndata: done\n\n"


async def api2(session, request):
    uname = request.query_params.get("uname")

    if uname not in {player.name for player in session.players}:
        raise HTTPException(status_code=404, detail="Unknown player")

    return StreamingResponse(
        counter_stream(session.name, uname),
        # This demo uses server-sent events so browsers and middleware flush each
        # tick immediately; ordinary streaming responses do not always need this.
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


page_order = [
    Stream,
]
