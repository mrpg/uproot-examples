from uproot.smithereens import *
from uproot.types import GroupCreatingWait, Page


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
