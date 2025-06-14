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

DESCRIPTION = "Watching for dropouts in uproot"


def new_player(player):
    player.dropout = False
    watch_for_dropout(player, handle_dropout)


async def handle_dropout(player):
    player.dropout = True
    await move_to_end(player)

    print(f"New dropout: {player}")


class Hello(Page):
    pass


page_order = [
    Hello,
]
