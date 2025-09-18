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
from uproot.types import Page

DESCRIPTION = "Ping the server (a simple WebSocket benchmark)"


class Ping(Page):
    @live
    async def ping(page, player, jstime: int, direct: bool):
        if direct:
            return jstime
        else:
            notify(player, player, jstime)


page_order = [
    Ping,
]
