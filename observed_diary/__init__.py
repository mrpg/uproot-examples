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
        for pid, watched in zip(group.players, page.watch_values):
            pid().watched = watched


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
