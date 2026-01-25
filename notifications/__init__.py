# Docs are available at https://uproot.science/
# Examples are available at https://github.com/mrpg/uproot-examples
#
# This example app is under the 0BSD license. You can use it freely and build on it
# without any limitations and without any attribution. However, these two lines must be
# preserved in any uproot app (the license file is automatically installed in projects):
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt

from uproot.smithereens import *

DESCRIPTION = "Test smithereens.notify"


class SendAndReceive(Page):
    allow_back = True

    @live
    async def notify_(page, player, data: str, where_: str | None):
        if where_ is None:
            where = None
        elif where_ == "...":
            where = ...
        else:
            where = int(where_)

        notify(
            player,
            players(player.session),
            data,
            event="Notified",
            where=where,
        )


page_order = [
    SendAndReceive,
    SendAndReceive,
    SendAndReceive,
]
