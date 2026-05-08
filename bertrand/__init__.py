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

DESCRIPTION = "Bertrand price competition"
SUGGESTED_MULTIPLE = 2
APP_NAME = __name__


class C:
    MAX_PRICE = 100
    # Demand at price P: Q = 100 - P, zero costs
    # Lower price captures all demand; tie splits demand equally


class Context(PlayerContext):
    @property
    def other_price(self):
        return self.player.other_in_group.price

    @property
    def market_price(self):
        return min(self.player.price, self.other_price)

    @property
    def my_demand(self):
        p, o = self.player.price, self.other_price
        if p < o:
            return max(0, 100 - p)
        if p > o:
            return 0
        return max(0, 100 - p) / 2


class GroupPlease(GroupCreatingWait):
    group_size = 2


class Instructions(Page):
    pass


class Decision(Page):
    fields = dict(
        price=IntegerField(
            label="What price do you set?",
            addon_start="$",
            min=0,
            max=C.MAX_PRICE,
            render_kw={"style": "flex: unset !important; width: 6rem !important;"},
        ),
    )


class Sync(SynchronizingWait):
    @classmethod
    def all_here(page, group):
        p1, p2 = group.players

        if p1.price < p2.price:
            d1, d2 = max(0, 100 - p1.price), 0
        elif p2.price < p1.price:
            d1, d2 = 0, max(0, 100 - p2.price)
        else:
            d1 = d2 = max(0, 100 - p1.price) / 2

        p1.payoff = p1.price * d1
        p2.payoff = p2.price * d2


class Results(Page):
    pass


def pipeline(session):
    rows = []

    for group, players in duopoly_groups(session):
        p1, p2 = players
        p1_data = p1.within(app=APP_NAME)
        p2_data = p2.within(app=APP_NAME)
        p1_price = p1_data.get("price")
        p2_price = p2_data.get("price")

        if p1_price is None or p2_price is None:
            d1 = d2 = None
            market_price = None
        elif p1_price < p2_price:
            d1, d2 = max(0, 100 - p1_price), 0
            market_price = p1_price
        elif p2_price < p1_price:
            d1, d2 = 0, max(0, 100 - p2_price)
            market_price = p2_price
        else:
            d1 = d2 = max(0, 100 - p1_price) / 2
            market_price = p1_price

        demands = [d1, d2]

        for member_id, player in enumerate(players):
            other = players[1 - member_id]
            player_data = player.within(app=APP_NAME)
            other_data = other.within(app=APP_NAME)

            rows.append(
                {
                    "session": session.name,
                    "group": group.name,
                    "uname": player.name,
                    "member_id": member_id,
                    "price": player_data.get("price"),
                    "other_uname": other.name,
                    "other_price": other_data.get("price"),
                    "market_price": market_price,
                    "demand": demands[member_id],
                    "payoff": player_data.get("payoff"),
                }
            )

    return rows


def duopoly_groups(session):
    groups = []

    for group in session.groups:
        players = group.players

        if len(players) == 2 and is_app_group(group, players):
            groups.append((group, players))

    return groups


def is_app_group(group, players):
    with group:
        if group.get("app") == APP_NAME:
            return True

        gid = group.gid

    return all(
        player.within(app=APP_NAME).get("_uproot_group") == gid for player in players
    )


page_order = [
    GroupPlease,
    Instructions,
    Decision,
    Sync,
    Results,
]
