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

DESCRIPTION = "Counter"


def new_player(player):
    player.counter = 0


class Counter(Page):
    @live
    async def increment(page, player):
        player.counter += 1
        return player.counter

    @live
    async def reset(page, player):
        player.counter = 0


page_order = [
    Counter,
]
