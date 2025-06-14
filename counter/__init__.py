"""
Docs are available at https://uproot.science/
Examples are available at https://github.com/mrpg/uproot-examples

This example app is under the 0BSD license. You can use it freely and build on it
without any limitations and without any attribution. However, these two lines must be
preserved in any uproot app (the license file is automatically installed in a project):

Third-party dependencies:
- uproot: LGPL v3+, see ../uproot_license.txt
"""

from uproot.smithereens import *
from uproot.types import Page

DESCRIPTION = "Count up"


def new_player(player):
    player.counter = 0


class Counter(Page):
    @live
    async def increment(page, player):
        if hasattr(player, "counter"):
            player.counter += 1
        else:
            player.counter = 0

        return player.counter

    @live
    async def delete(page, player):
        if hasattr(player, "counter"):
            del player.counter


page_order = [
    Counter,
]
