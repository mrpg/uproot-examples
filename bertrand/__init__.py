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


page_order = [
    GroupPlease,
    Instructions,
    Decision,
    Sync,
    Results,
]
