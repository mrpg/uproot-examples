# Docs are available at https://uproot.science/
# Examples are available at https://github.com/mrpg/uproot-examples
#
# This example app is under the 0BSD license. You can use it freely and build on it
# without any limitations and without any attribution. However, these two lines must be
# preserved in any uproot app (the license file is automatically installed in projects):
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt

"""
Double Auction Market Experiment

This module implements a continuous double auction where buyers and sellers
can submit bids and asks respectively. When compatible offers meet (bid ≥ ask),
trades execute automatically at the offered price.

The auction follows these principles:
- Each participant is either a buyer (with a value) or seller (with a cost)
- Buyers profit when purchasing below their value
- Sellers profit when selling above their cost
- Trades occur when a buyer accepts an ask or a seller accepts a bid
"""

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from itertools import cycle
from time import time
from typing import Any, Optional
from uuid import UUID

import uproot.models as um
from uproot.fields import *
from uproot.smithereens import *

from .find_eq import find_equilibrium

DESCRIPTION = "Double auction"
LANDING_PAGE = False
APP_NAME = __name__


class C:
    DETECTION_PERIOD = 30.0
    DEFAULT_BUYER_TAX = 0
    DEFAULT_SELLER_TAX = 0
    DEFAULT_DURATION = 25 * 60
    DEFAULT_NUM_ROUNDS = 3
    DEFAULT_VALUES = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    DEFAULT_COSTS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def get_setting(session, key):
    return session.settings.get(key, getattr(C, "DEFAULT_" + key.upper()))


def get_tax(session, key, round_num):
    """Get tax for a specific round. key is 'buyer_tax' or 'seller_tax'."""
    val = get_setting(session, key)
    if isinstance(val, list):
        return val[round_num - 1]
    return val


class Offer(metaclass=um.Entry):
    """
    Represents a market offer (bid or ask)

    Attributes:
        pid: Player who created the offer
        round: Trading round number
        buy: True for bid, False for ask
        price: Offer price (None indicates cancellation)
    """

    pid: PlayerIdentifier
    round: int
    buy: bool
    price: Optional[int]  # None signifies offer withdrawal/invalidation


class Transaction(metaclass=um.Entry):
    """
    Represents an executed trade

    Attributes:
        round: Trading round number
        acceptor: Player who accepted the offer
        price: Execution price
    """

    round: int
    acceptor: PlayerIdentifier
    price: int


def new_session(session):
    """Initialize session with offer book and transaction ledger models"""
    num_rounds = get_setting(session, "num_rounds")
    for key in ("buyer_tax", "seller_tax"):
        val = get_setting(session, key)
        if isinstance(val, list):
            if len(val) != num_rounds:
                raise ValueError(
                    f"{key} has {len(val)} entries but num_rounds is {num_rounds}"
                )

    session.offers = um.create_model(session, tag="offers")
    session.txs = um.create_model(session, tag="transactions")


class Context(PlayerContext):
    @property
    def present(self):
        return [p for p in self.player.session.players if p.present]


class RaiseHands(Page):
    @classmethod
    def reset_session(page, player):
        for p in player.session.players:
            p.present = False

    @classmethod
    def ensure_detection(page, player):
        if player.session.get("detection_period_until") is None:
            player.session.detection_period_until = time() + C.DETECTION_PERIOD
            page.reset_session(player)

    @classmethod
    def timeout(page, player):
        page.ensure_detection(player)
        return player.session.detection_period_until - time()

    @classmethod
    def before_once(page, player):
        page.ensure_detection(player)

    @classmethod
    def may_proceed(page, player):
        return time() >= player.session.detection_period_until

    @live
    def set_presence(page, player, new_value: bool):
        player.present = new_value
        return new_value


class Assignment(NoshowPage):
    @classmethod
    def after_always_once(page, player):
        if not player.present:
            return

        session = player.session
        present = player.context.present

        master_buyer = [True for _ in get_setting(session, "values")] + [
            False for _ in get_setting(session, "costs")
        ]
        master_cost_or_value = get_setting(session, "values") + get_setting(
            session, "costs"
        )

        n = len(present)
        k = n // len(master_buyer)
        e = n - k * len(master_buyer)

        assignable_buyer = master_buyer * k
        assignable_cost_or_value = master_cost_or_value * k

        for i in range(e):
            is_buyer = i % 2 == 0
            assignable_buyer.append(is_buyer)
            assignable_cost_or_value.append(
                max(get_setting(session, "values"))
                if is_buyer
                else min(get_setting(session, "costs"))
            )

        my_id = present.index(player)  # This is guaranteed to work
        player.buyer = assignable_buyer[my_id]
        player.cost_or_value = assignable_cost_or_value[my_id]


def market_data(
    offers_model,
    txs_model,
    round: int,
) -> dict[str, list[dict[str, Any]]]:
    """
    Extract current market state: active bids, asks, and executed trades

    The market book separates buy and sell orders, showing only
    the most recent valid offer from each participant.

    Args:
        offers_model: Model containing all offers
        txs_model: Model containing all transactions
        round: Current trading round

    Returns:
        Dictionary with 'asks', 'bids', and 'txs' lists
    """
    # Map each player to their latest offer (last one wins)
    player_offers = {}
    for entry_id, _, entry in um.filter_entries(offers_model, Offer, round=round):
        player_offers[entry.pid] = (entry_id, entry.buy, entry.price)

    # Partition valid offers into market sides
    market_book = {"asks": [], "bids": []}

    for offer_id, is_buy, price in player_offers.values():
        if price is None:  # Skip cancelled offers
            continue

        offer_data = {"id": offer_id, "price": price}
        side_key = "bids" if is_buy else "asks"
        market_book[side_key].append(offer_data)

    # Append executed transactions
    market_book["txs"] = [
        entry for _, _, entry in um.filter_entries(txs_model, Transaction, round=round)
    ]

    return market_book


def calculate_profit(
    player,
    price: int,
    round_num: int,
) -> int:
    """
    Calculate trading profit based on player type

    Buyers: profit = value - price - buyer_tax
    Sellers: profit = price - cost - seller_tax
    """
    session = player.session
    if player.buyer:
        return player.cost_or_value - price - get_tax(session, "buyer_tax", round_num)
    else:
        return price - player.cost_or_value - get_tax(session, "seller_tax", round_num)


def get_player_active_offer_id(
    offers_model,
    round: int,
    offer_uuid,
) -> Optional[UUID]:
    """Return offer_uuid if it is currently the active offer, else None."""
    if offer_uuid is None:
        return None
    result = validate_offer(offers_model, round, offer_uuid)
    return offer_uuid if result is not None else None


def broadcast_market_diff(
    sender,
    session,
    remove: list,
    add: list,
    txs: list,
):
    """Send a minimal market diff to all participants."""
    notify(
        sender,
        session.players,
        {"remove": remove, "add": add, "txs": txs},
        event="MarketDiff",
    )


def create_offer_entry(
    session,
    player,
    round: int,
    is_buy: bool,
    price: Optional[int],
) -> UUID:
    """Helper to create and store an offer, returns the entry UUID"""
    return um.add_entry(
        session.offers,
        player,
        Offer,
        round=round,
        buy=is_buy,
        price=price,
    )


def validate_offer(
    offers_model,
    round: int,
    offer_id: UUID,
) -> Optional[tuple[UUID, Offer]]:
    """
    Validate that an offer exists and is active

    Returns (id, offer) tuple if valid, None if invalid/cancelled
    """
    candidates = um.filter_entries(
        offers_model,
        Offer,
        id=offer_id,
        round=round,
    )

    if not candidates:
        return None

    target_id, _, target_offer = candidates[0]
    if target_offer.price is None:
        return None

    latest_id = None

    # Verify this is the player's current active offer
    for entry_id, _, entry in um.filter_entries(offers_model, Offer, round=round):
        if entry.pid == target_offer.pid:
            latest_id = entry_id

    if latest_id != target_id:
        return None  # Player has a newer offer

    return (target_id, target_offer)


class Instructions(Page):
    """
    Instructions page shown before trading begins

    Explains the double auction mechanism, player roles, and how to trade.
    """

    @classmethod
    def show(page, player):
        return player.present


class RoundInfo(Page):
    """Round-specific information shown at the start of each trading round."""

    @classmethod
    def show(page, player):
        return player.present


class Trade(Page):
    """
    Trading interface page where participants submit and accept offers

    Each player receives a private value (buyers) or cost (sellers) and
    can profit by trading at favorable prices. The market operates as
    a continuous double auction with immediate execution.
    """

    @classmethod
    def show(page, player):
        return player.present

    @classmethod
    def before_once(page, player):
        player.offer = None
        player.trade = None
        player.profit = None
        num_rounds = get_setting(player.session, "num_rounds")
        player.add_round = player.round < num_rounds

    @classmethod
    def timeout(page, player):
        session = player.session
        if (
            session.get("trade_until") is None
            or session.get("trade_round") != player.round
        ):
            session.trade_until = time() + get_setting(session, "duration")
            session.trade_round = player.round

        return session.trade_until - time()

    @classmethod
    async def jsvars(page, player):
        if player.get("offer") is None:
            return dict(offer_amount=None)
        else:
            result = validate_offer(
                player.session.offers,
                player.round,
                player.offer,
            )

            if result is None:
                return dict(offer_amount=None)
            else:
                _, offer = result
                return dict(offer_amount=offer.price)

    @live
    def get_market(page, player):
        return market_data(player.session.offers, player.session.txs, player.round)

    @live
    def make_offer(page, player, amount: Optional[int]):
        """
        Submit a new bid (buyers) or ask (sellers) to the market

        Args:
            amount: Offer price (None to cancel existing offer)

        Returns:
            The submitted price

        Raises:
            ValueError: If amount is negative or player already traded
        """
        if player.trade:
            raise ValueError(f"Player {player} already traded.")

        if amount is not None:
            if amount < 0:
                raise ValueError(f"Bad amount: {amount}")
            session = player.session
            if player.buyer:
                max_bid = player.cost_or_value - get_tax(
                    session, "buyer_tax", player.round
                )
                if amount > max_bid:
                    raise ValueError("Bid cannot exceed your valuation minus tax")
            else:
                min_ask = player.cost_or_value + get_tax(
                    session, "seller_tax", player.round
                )
                if amount < min_ask:
                    raise ValueError("Ask cannot be below your cost plus tax")

        old_offer_id = get_player_active_offer_id(
            player.session.offers, player.round, player.get("offer")
        )

        player.offer = create_offer_entry(
            player.session,
            player,
            player.round,
            player.buyer,
            amount,
        )

        broadcast_market_diff(
            player,
            player.session,
            remove=[old_offer_id] if old_offer_id is not None else [],
            add=(
                [{"id": player.offer, "price": amount, "buy": player.buyer}]
                if amount is not None
                else []
            ),
            txs=[],
        )
        return amount

    @live
    def accept_offer(page, player, offer_id: UUID):
        """
        Accept an existing market offer, executing a trade

        The acceptor takes the proposer's price. Both parties'
        profits are calculated and distributed immediately.

        Args:
            offer_id: ID of offer to accept

        Returns:
            Acceptor's realized profit

        Raises:
            ValueError: If player already traded or offer invalid
        """
        if player.trade:
            raise ValueError(f"Player {player} already traded.")

        # Validate and retrieve the target offer
        result = validate_offer(
            player.session.offers,
            player.round,
            offer_id,
        )

        if result is None:
            raise ValueError("Offer no longer valid")

        validated_id, offer = result
        if validated_id != offer_id:
            raise ValueError("Offer no longer valid")

        if offer.buy == player.buyer:
            raise ValueError("Buyer cannot sell, seller cannot buy")

        # Ensure accepting this offer wouldn't yield negative profit
        session = player.session
        if player.buyer:
            tax = get_tax(session, "buyer_tax", player.round)
            if offer.price > player.cost_or_value - tax:
                raise ValueError("Accepting this offer would result in negative profit")
        else:
            tax = get_tax(session, "seller_tax", player.round)
            if offer.price < player.cost_or_value + tax:
                raise ValueError("Accepting this offer would result in negative profit")

        # Capture acceptor's active offer ID before cancellation
        acceptor_old_offer_id = get_player_active_offer_id(
            player.session.offers, player.round, player.get("offer")
        )

        # Cancel proposer's offer to prevent double-trading
        create_offer_entry(
            player.session,
            offer.pid,
            player.round,
            not player.buyer,  # Opposite side (double auction mechanics)
            None,  # Null price cancels
        )

        # Update proposer
        with Player(offer.pid.sname, offer.pid.uname) as proposer:
            proposer.offer = None
            proposer.profit = calculate_profit(proposer, offer.price, player.round)
            notify(player, proposer, [True, proposer.profit], event="OfferAccepted")

            # Update acceptor
            player.offer = None
            player.profit = calculate_profit(player, offer.price, player.round)

            # Cancel any outstanding offer by acceptor
            create_offer_entry(
                player.session,
                player,
                player.round,
                player.buyer,
                None,  # Null price cancels
            )

            # Record transaction
            tx_id = um.add_entry(
                player.session.txs,
                player,
                Transaction,
                round=player.round,
                price=offer.price,
            )
            proposer.trade = player.trade = tx_id

        # Fetch the newly recorded transaction entry for the diff
        new_tx_entries = um.filter_entries(player.session.txs, Transaction, id=tx_id)
        new_tx = new_tx_entries[0][2] if new_tx_entries else None

        remove_ids = [offer_id]
        if acceptor_old_offer_id is not None:
            remove_ids.append(acceptor_old_offer_id)

        broadcast_market_diff(
            player,
            player.session,
            remove=remove_ids,
            add=[],
            txs=[new_tx] if new_tx is not None else [],
        )
        return player.profit


def digest(session):
    if session.get("offers") is None:
        return {"rounds_data": []}

    demand_values = []
    supply_costs = []

    for player in session.players:
        if player.get("buyer") is None:
            continue
        if player.buyer:
            demand_values.append(player.cost_or_value)
        else:
            supply_costs.append(player.cost_or_value)

    demand_values.sort(reverse=True)
    supply_costs.sort()

    def eq_to_dict(eq):
        if eq is None or eq.quantity == 0:
            return None
        return {
            "price_min": int(eq.price_min),
            "price_max": int(eq.price_max),
            "quantity": eq.quantity,
        }

    rounds_data = []
    num_rounds = get_setting(session, "num_rounds")
    for round_num in range(1, num_rounds + 1):
        # Tax-adjusted curves (micro 101: demand shifts down, supply shifts up)
        buyer_tax = get_tax(session, "buyer_tax", round_num)
        seller_tax = get_tax(session, "seller_tax", round_num)
        eff_demand = [v - buyer_tax for v in demand_values]
        eff_supply = [c + seller_tax for c in supply_costs]

        expected_eq = eq_to_dict(
            find_equilibrium(
                [Decimal(str(v)) for v in eff_demand],
                [Decimal(str(c)) for c in eff_supply],
            )
        )

        player_offers = {}
        for entry_id, _, entry in um.filter_entries(
            session.offers, Offer, round=round_num
        ):
            player_offers[entry.pid] = (entry.buy, entry.price)

        actual_bids = []
        actual_asks = []
        for is_buy, price in player_offers.values():
            if price is None:
                continue
            if is_buy:
                actual_bids.append(price)
            else:
                actual_asks.append(price)

        actual_bids.sort(reverse=True)
        actual_asks.sort()

        tx_prices = [
            entry.price
            for _, _, entry in um.filter_entries(
                session.txs, Transaction, round=round_num
            )
        ]

        rounds_data.append(
            {
                "round": round_num,
                "demand_values": eff_demand,
                "supply_costs": eff_supply,
                "expected_eq": expected_eq,
                "actual_bids": actual_bids,
                "actual_asks": actual_asks,
                "transactions": tx_prices,
            }
        )

    return {
        "rounds_data": rounds_data,
    }


def pipeline(session):
    if session.get("offers") is None:
        return []

    rows = []
    num_rounds = get_setting(session, "num_rounds")

    for round_num in range(1, num_rounds + 1):
        latest_offers = latest_offer_by_player(session, round_num)
        transactions = transactions_by_id(session, round_num)

        for player in session.players:
            app_data = player.within(app=APP_NAME)

            if app_data.get("buyer") is None:
                continue

            round_data = player.within(app=APP_NAME, round=round_num)
            trade_id = round_data.get("trade")
            transaction = transactions.get(trade_id)
            active_offer = latest_offers.get(player.pid)

            rows.append(
                {
                    "session": session.name,
                    "round": round_num,
                    "uname": player.name,
                    "role": "buyer" if app_data.get("buyer") else "seller",
                    "cost_or_value": app_data.get("cost_or_value"),
                    "buyer_tax": get_tax(session, "buyer_tax", round_num),
                    "seller_tax": get_tax(session, "seller_tax", round_num),
                    "active_offer": active_offer.price if active_offer else None,
                    "trade_price": transaction.price if transaction else None,
                    "profit": round_data.get("profit"),
                }
            )

    return rows


def latest_offer_by_player(session, round_num):
    offers = {}

    for _, pid, offer in um.filter_entries(session.offers, Offer, round=round_num):
        offers[pid] = offer

    return {pid: offer for pid, offer in offers.items() if offer.price is not None}


def transactions_by_id(session, round_num):
    return {
        entry_id: transaction
        for entry_id, _, transaction in um.filter_entries(
            session.txs,
            Transaction,
            round=round_num,
        )
    }


page_order = [
    RaiseHands,
    Assignment,
    Instructions,
    Repeat(
        RoundInfo,
        Trade,
    ),
]
