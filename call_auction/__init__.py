# Docs are available at https://uproot.science/
# Examples are available at https://github.com/mrpg/uproot-examples
#
# This example app is under the 0BSD license. You can use it freely and build on it
# without any limitations and without any attribution. However, these two lines must be
# preserved in any uproot app (the license file is automatically installed in projects):
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt

from decimal import Decimal
from time import time

from find_eq import find_equilibrium
from uproot.fields import *
from uproot.smithereens import *

DESCRIPTION = "Call auction"
LANDING_PAGE = False
APP_NAME = __name__


class C:
    DEFAULT_DURATION = 5 * 60
    DEFAULT_NUM_ROUNDS = 3
    DEFAULT_VALUES = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    DEFAULT_COSTS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def get_setting(session, key):
    return session.settings.get(key, getattr(C, "DEFAULT_" + key.upper()))


class Assignment(NoshowPage):
    @classmethod
    def after_always_once(page, player):
        session = player.session
        values = get_setting(session, "values")
        costs = get_setting(session, "costs")

        master_buyer = [True] * len(values) + [False] * len(costs)
        master_cv = values + costs

        n = len(session.players)
        k = n // len(master_buyer)
        e = n - k * len(master_buyer)

        assignable_buyer = master_buyer * k
        assignable_cv = master_cv * k

        for i in range(e):
            is_buyer = i % 2 == 0
            assignable_buyer.append(is_buyer)
            assignable_cv.append(max(values) if is_buyer else min(costs))

        my_id = list(session.players).index(player)
        player.buyer = assignable_buyer[my_id]
        player.cost_or_value = assignable_cv[my_id]


class Instructions(Page):
    pass


class Submit(Page):
    @classmethod
    def before_once(page, player):
        player.bid = None
        player.traded = False
        player.profit = 0

    @classmethod
    def timeout(page, player):
        session = player.session
        if (
            session.get("submit_until") is None
            or session.get("submit_round") != player.round
        ):
            session.submit_until = time() + get_setting(session, "duration")
            session.submit_round = player.round
        return session.submit_until - time()

    @live
    def place_bid(page, player, amount: int):
        if amount < 0:
            raise ValueError("Price cannot be negative")
        if player.buyer and amount > player.cost_or_value:
            raise ValueError("Bid cannot exceed your valuation")
        if not player.buyer and amount < player.cost_or_value:
            raise ValueError("Ask cannot be below your cost")
        player.bid = amount
        setattr(player, f"bid_r{player.round}", amount)
        return amount


class Results(Page):
    @classmethod
    def before_once(page, player):
        session = player.session
        round_num = player.round
        num_rounds = get_setting(session, "num_rounds")
        player.add_round = round_num < num_rounds

        # Collect bids and asks (using persisted per-round values)
        bids = []
        asks = []
        for p in session.players:
            bid = p.get(f"bid_r{round_num}")
            if bid is not None:
                (bids if p.buyer else asks).append(bid)

        clearing_price = None
        quantity = 0

        if bids and asks:
            eq = find_equilibrium(
                [Decimal(str(b)) for b in bids],
                [Decimal(str(a)) for a in asks],
            )
            if eq and eq.quantity > 0:
                clearing_price = round((float(eq.price_min) + float(eq.price_max)) / 2)
                quantity = eq.quantity

        player.clearing_price = clearing_price
        player.market_quantity = quantity

        # Determine if this player traded
        my_bid = player.get(f"bid_r{round_num}")
        if clearing_price is not None and my_bid is not None:
            if player.buyer and my_bid >= clearing_price:
                player.traded = True
                player.profit = player.cost_or_value - clearing_price
            elif not player.buyer and my_bid <= clearing_price:
                player.traded = True
                player.profit = clearing_price - player.cost_or_value

        # Store for digest
        setattr(session, f"clearing_r{round_num}", clearing_price)
        setattr(session, f"quantity_r{round_num}", quantity)


def digest(session):
    if not any(p.get("buyer") is not None for p in session.players):
        return {"rounds_data": []}

    demand_values = sorted(
        [p.cost_or_value for p in session.players if p.get("buyer")],
        reverse=True,
    )
    supply_costs = sorted(
        [
            p.cost_or_value
            for p in session.players
            if p.get("buyer") is not None and not p.buyer
        ],
    )

    def eq_to_dict(eq):
        if eq is None or eq.quantity == 0:
            return None
        return {
            "price_min": int(eq.price_min),
            "price_max": int(eq.price_max),
            "quantity": eq.quantity,
        }

    num_rounds = get_setting(session, "num_rounds")
    rounds_data = []

    for round_num in range(1, num_rounds + 1):
        expected_eq = eq_to_dict(
            find_equilibrium(
                [Decimal(str(v)) for v in demand_values],
                [Decimal(str(c)) for c in supply_costs],
            )
        )

        submitted_bids = sorted(
            [
                p.get(f"bid_r{round_num}")
                for p in session.players
                if p.get("buyer") and p.get(f"bid_r{round_num}") is not None
            ],
            reverse=True,
        )
        submitted_asks = sorted(
            [
                p.get(f"bid_r{round_num}")
                for p in session.players
                if p.get("buyer") is not None
                and not p.buyer
                and p.get(f"bid_r{round_num}") is not None
            ],
        )

        rounds_data.append(
            {
                "round": round_num,
                "demand_values": demand_values,
                "supply_costs": supply_costs,
                "expected_eq": expected_eq,
                "submitted_bids": submitted_bids,
                "submitted_asks": submitted_asks,
                "clearing_price": session.get(f"clearing_r{round_num}"),
                "quantity": session.get(f"quantity_r{round_num}", 0),
            }
        )

    return {"rounds_data": rounds_data}


def pipeline(session):
    rows = []
    num_rounds = get_setting(session, "num_rounds")

    for round_num in range(1, num_rounds + 1):
        clearing_price = session.get(f"clearing_r{round_num}")

        for player in session.players:
            app_data = player.within(app=APP_NAME)

            if app_data.get("buyer") is None:
                continue

            round_data = player.within(app=APP_NAME, round=round_num)
            bid = round_data.get(f"bid_r{round_num}")

            rows.append(
                {
                    "session": session.name,
                    "round": round_num,
                    "uname": player.name,
                    "role": "buyer" if app_data.get("buyer") else "seller",
                    "cost_or_value": app_data.get("cost_or_value"),
                    "bid_or_ask": bid,
                    "clearing_price": clearing_price,
                    "market_quantity": session.get(f"quantity_r{round_num}", 0),
                    "traded": round_data.get("traded"),
                    "profit": round_data.get("profit"),
                }
            )

    return rows


page_order = [
    Assignment,
    Instructions,
    Repeat(
        Submit,
        Results,
    ),
]
