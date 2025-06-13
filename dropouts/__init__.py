from uproot.smithereens import *
from uproot.types import Page


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
