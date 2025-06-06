from uproot.smithereens import *
from uproot.types import Page


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
