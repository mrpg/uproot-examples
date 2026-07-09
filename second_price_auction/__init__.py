# Docs are available at https://uproot.science/
# Examples are available at https://github.com/mrpg/uproot-examples
#
# This example app is under the 0BSD license. You can use it freely and build on it
# without any limitations and without any attribution. However, these two lines must be
# preserved in any uproot app (the license file is automatically installed in projects):
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt

from uproot.fields import *
from uproot.smithereens import *

DESCRIPTION = "Second-price sealed-bid auction (Vickrey, 1961)"
SUGGESTED_MULTIPLE = 3


class C:
    GROUP_SIZE = 3
    MAX_VALUE = 100


class GroupPlease(GroupCreatingWait):
    group_size = C.GROUP_SIZE

    @classmethod
    def after_grouping(page, group: GroupType) -> None:
        for player in group.players:
            player.value = cu(rng().randint(0, C.MAX_VALUE))


class Bid(Page):
    fields = dict(
        bid=DecimalField(
            label="Your bid:",
            addon_start="$",
            min=0,
            max=C.MAX_VALUE,
            places=2,
        ),
    )


class Sync(SynchronizingWait):
    @classmethod
    def all_here(page, group: GroupType) -> None:
        players = group.players
        bids = sorted((p.bid for p in players), reverse=True)
        high_bid, price = bids[0], bids[1]
        winner = rng().choice([p for p in players if p.bid == high_bid])

        for player in players:
            player.high_bid = high_bid
            player.price = price
            player.winner = player is winner
            player.payoff = player.value - price if player.winner else cu(0)


class Results(Page):
    pass


def pipeline(session: SessionType) -> list[dict[str, Any]]:
    rows = []

    for group in session.groups(app=__name__):
        players = group.players

        for member_id, player in enumerate(players):
            player_data = player.within(app=__name__)

            rows.append(
                {
                    "session": session.name,
                    "group": group.name,
                    "uname": player.name,
                    "member_id": member_id,
                    "value": player_data.get("value"),
                    "bid": player_data.get("bid"),
                    "high_bid": player_data.get("high_bid"),
                    "price": player_data.get("price"),
                    "winner": player_data.get("winner"),
                    "payoff": player_data.get("payoff"),
                }
            )

    return rows


page_order = [
    GroupPlease,
    Bid,
    Sync,
    Results,
]
