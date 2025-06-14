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
from uproot.types import GroupCreatingWait, Page

DESCRIPTION = "Have a player watch someone else's diary entry"


class GroupPlease(GroupCreatingWait):
    group_size = 2
    watch_values = (
        True,
        False,
    )

    @classmethod
    def after_grouping(page, group):
        for player, watched in zip(players(group), page.watch_values):
            player.watched = watched


class Watch(Page):
    @live
    async def typed(page, player, s: str):
        await send_to(
            others_in_group(player),
            s,
        )


page_order = [
    GroupPlease,
    Watch,
]
