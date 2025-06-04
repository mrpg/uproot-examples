from uproot.smithereens import *
from uproot.types import Page


class Ping(Page):
    @live
    async def ping(page, player, jstime: int, direct: bool):
        if direct:
            return jstime
        else:
            await send_to(player, jstime)


page_order = [
    Ping,
]
