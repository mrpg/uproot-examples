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
can submit bids and asks respectively. A trade executes when a participant
accepts an opposing offer at the posted price.

The auction follows these principles:
- Each participant is either a buyer (with a value) or seller (with a cost)
- Buyers profit when purchasing below their value
- Sellers profit when selling above their cost
- Trades occur when a buyer accepts an ask or a seller accepts a bid
"""

from decimal import Decimal
from time import time
from typing import Any, Optional
from uuid import UUID

import uproot.models as um
from find_eq import find_equilibrium
from uproot.fields import *
from uproot.smithereens import *

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


def is_integer(value):
    return isinstance(value, int) and not isinstance(value, bool)


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
        proposer: Player whose standing offer was accepted
        acceptor: Player who accepted the offer
        price: Execution price
    """

    round: int
    acceptor: PlayerIdentifier
    price: int
    proposer: Optional[PlayerIdentifier] = None


def new_session(session):
    """Initialize session with offer book and transaction ledger models"""
    num_rounds = get_setting(session, "num_rounds")
    duration = get_setting(session, "duration")
    values = get_setting(session, "values")
    costs = get_setting(session, "costs")

    if (
        not isinstance(num_rounds, int)
        or isinstance(num_rounds, bool)
        or num_rounds < 1
    ):
        raise ValueError("num_rounds must be a positive integer")
    if not is_integer(duration) or duration <= 0:
        raise ValueError("duration must be a positive integer")
    if (
        not isinstance(values, list)
        or not values
        or not all(is_integer(v) for v in values)
    ):
        raise ValueError("values must be a non-empty integer list")
    if (
        not isinstance(costs, list)
        or not costs
        or not all(is_integer(c) for c in costs)
    ):
        raise ValueError("costs must be a non-empty integer list")

    for key in ("buyer_tax", "seller_tax"):
        val = get_setting(session, key)
        if isinstance(val, list):
            if len(val) != num_rounds:
                raise ValueError(
                    f"{key} has {len(val)} entries but num_rounds is {num_rounds}"
                )
            if not all(is_integer(tax) for tax in val):
                raise ValueError(f"{key} must contain only integers")
        elif not is_integer(val):
            raise ValueError(f"{key} must be an integer or a list of integers")

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

        with session:
            assignment = session.get("double_auction_assignment")

            if assignment is None:
                values = get_setting(session, "values")
                costs = get_setting(session, "costs")

                master_buyer = [True for _ in values] + [False for _ in costs]
                master_cost_or_value = values + costs

                n = len(present)
                k = n // len(master_buyer)
                e = n - k * len(master_buyer)

                assignable_buyer = master_buyer * k
                assignable_cost_or_value = master_cost_or_value * k

                for i in range(e):
                    is_buyer = i % 2 == 0
                    assignable_buyer.append(is_buyer)
                    assignable_cost_or_value.append(
                        max(values) if is_buyer else min(costs)
                    )

                assignment = [
                    [a, b] for a, b in zip(assignable_buyer, assignable_cost_or_value)
                ]
                rng().shuffle(assignment)
                session.double_auction_assignment = assignment

        my_id = present.index(player)
        player.buyer, player.cost_or_value = assignment[my_id]


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
    traded_players = players_traded_in_round(txs_model, round)

    # Map each player to their latest offer (last one wins)
    player_offers = {}
    for entry_id, _, entry in um.filter_entries(offers_model, Offer, round=round):
        player_offers[entry.pid] = (entry_id, entry.buy, entry.price)

    # Partition valid offers into market sides
    market_book = {"asks": [], "bids": []}

    for pid, (offer_id, is_buy, price) in player_offers.items():
        if pid in traded_players:
            continue
        if price is None:  # Skip cancelled offers
            continue

        offer_data = {"id": offer_id, "price": price}
        side_key = "bids" if is_buy else "asks"
        market_book[side_key].append(offer_data)

    market_book["txs"] = [
        {"price": entry.price}
        for _, _, entry in um.filter_entries(txs_model, Transaction, round=round)
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
    txs_model,
    round: int,
    offer_uuid,
) -> Optional[UUID]:
    """Return offer_uuid if it is currently the active offer, else None."""
    if offer_uuid is None:
        return None
    result = validate_offer(offers_model, txs_model, round, offer_uuid)
    return offer_uuid if result is not None else None


def transaction_players(transaction: Transaction) -> tuple[PlayerIdentifier, ...]:
    players = [transaction.acceptor]
    if transaction.proposer is not None:
        players.append(transaction.proposer)
    return tuple(players)


def players_traded_in_round(txs_model, round: int) -> set[PlayerIdentifier]:
    traded = set()
    for _, _, transaction in um.filter_entries(txs_model, Transaction, round=round):
        traded.update(transaction_players(transaction))
    return traded


def player_transaction_id(
    txs_model, round: int, pid: PlayerIdentifier
) -> Optional[UUID]:
    result = player_transaction(txs_model, round, pid)
    return result[0] if result is not None else None


def player_transaction(
    txs_model,
    round: int,
    pid: PlayerIdentifier,
) -> Optional[tuple[UUID, Transaction]]:
    for tx_id, _, transaction in um.filter_entries(txs_model, Transaction, round=round):
        if pid in transaction_players(transaction):
            return tx_id, transaction
    return None


def player_has_traded(txs_model, round: int, pid: PlayerIdentifier) -> bool:
    return player_transaction_id(txs_model, round, pid) is not None


def player_profit_from_ledger(player) -> Optional[int]:
    result = player_transaction(player.session.txs, player.round, player.pid)
    if result is None:
        return None
    _, transaction = result
    return calculate_profit(player, transaction.price, player.round)


def ensure_trading_open(player):
    """Start or verify the shared round timer, then reject stale live calls."""
    session = player.session
    now = time()

    if session.get("trade_until") is None:
        session.trade_until = now + get_setting(session, "duration")
        session.trade_round = player.round

    if session.get("trade_round") != player.round:
        raise ValueError("Trading is closed for this round")
    if now > session.trade_until:
        raise ValueError("Trading is closed for this round")


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
    txs_model,
    round: int,
    offer_id: UUID,
) -> Optional[tuple[UUID, Offer]]:
    """
    Validate that an offer exists and is active

    Returns (id, offer) tuple if valid, None if invalid/cancelled
    """
    target_offer = None
    player_latest = {}

    for entry_id, _, entry in um.filter_entries(offers_model, Offer, round=round):
        player_latest[entry.pid] = entry_id
        if entry_id == offer_id:
            target_offer = entry

    if target_offer is None or target_offer.price is None:
        return None
    if player_latest.get(target_offer.pid) != offer_id:
        return None
    if player_has_traded(txs_model, round, target_offer.pid):
        return None

    return (offer_id, target_offer)


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
        player.profit = 0
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
        if player_has_traded(player.session.txs, player.round, player.pid):
            return dict(offer_amount=None)
        if player.get("offer") is None:
            return dict(offer_amount=None)
        else:
            result = validate_offer(
                player.session.offers,
                player.session.txs,
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
        ensure_trading_open(player)

        if player.get("trade") or player_has_traded(
            player.session.txs, player.round, player.pid
        ):
            raise ValueError(f"Player {player} already traded.")

        if amount is not None:
            if not is_integer(amount):
                raise ValueError("Offer amount must be an integer")
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
            player.session.offers,
            player.session.txs,
            player.round,
            player.get("offer"),
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
    def accept_offer(page, player, offer_ids: list):
        """
        Accept an existing market offer, executing a trade

        The client sends a list of offer IDs (all at the same price);
        the server picks the first one that is still valid.
        """
        ensure_trading_open(player)

        if player.get("trade") or player_has_traded(
            player.session.txs, player.round, player.pid
        ):
            raise ValueError(f"Player {player} already traded.")

        # Try each candidate until we find one still valid
        offer_id = None
        offer = None

        for raw_id in offer_ids:
            cid = UUID(str(raw_id))
            result = validate_offer(
                player.session.offers,
                player.session.txs,
                player.round,
                cid,
            )

            if result is None:
                continue

            _, validated_offer = result

            if validated_offer.round != player.round:
                continue
            if validated_offer.buy == player.buyer:
                continue
            if validated_offer.pid == player.pid:
                continue

            offer_id = cid
            offer = validated_offer
            break

        if offer_id is None:
            raise ValueError("Offer no longer valid")

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
            player.session.offers,
            player.session.txs,
            player.round,
            player.get("offer"),
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
                acceptor=player.pid,
                price=offer.price,
                proposer=offer.pid,
            )
            proposer.trade = player.trade = tx_id

        remove_ids = [offer_id]

        if acceptor_old_offer_id is not None:
            remove_ids.append(acceptor_old_offer_id)

        broadcast_market_diff(
            player,
            player.session,
            remove=remove_ids,
            add=[],
            txs=[{"price": offer.price}],
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

        traded = players_traded_in_round(session.txs, round_num)
        player_offers = {}
        for entry_id, _, entry in um.filter_entries(
            session.offers, Offer, round=round_num
        ):
            player_offers[entry.pid] = (entry.buy, entry.price)

        actual_bids = []
        actual_asks = []
        for pid, (is_buy, price) in player_offers.items():
            if pid in traded:
                continue
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
    traded = players_traded_in_round(session.txs, round_num)

    for _, pid, offer in um.filter_entries(session.offers, Offer, round=round_num):
        offers[pid] = offer

    return {
        pid: offer
        for pid, offer in offers.items()
        if offer.price is not None and pid not in traded
    }


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
