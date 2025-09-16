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
from enum import Enum
from itertools import cycle
from random import randint
from typing import Any, Dict, List, Optional, Tuple

import uproot.model as mod
from uproot.fields import *
from uproot.smithereens import *

DESCRIPTION = "Double auction"
LANDING_PAGE = True


class Offer(metaclass=mod.Entry):
    """
    Represents a market offer (bid or ask)

    Attributes:
        id: Unique offer identifier
        pid: Player who created the offer
        round: Trading round number
        buy: True for bid, False for ask
        price: Offer price (None indicates cancellation)
    """

    id: str
    pid: t.PlayerIdentifier
    round: int
    buy: bool
    price: Optional[float]  # None signifies offer withdrawal/invalidation


class Transaction(metaclass=mod.Entry):
    """
    Represents an executed trade

    Attributes:
        id: Unique transaction identifier
        round: Trading round number
        offer_id: ID of the accepted offer
        acceptor: Player who accepted the offer
        price: Execution price
    """

    id: str
    round: int
    offer_id: str
    acceptor: t.PlayerIdentifier
    price: float


def new_session(session):
    """Initialize session with offer book and transaction ledger models"""
    session.offers = mod.create_model(session, tag="offers")
    session.txs = mod.create_model(session, tag="transactions")


def market_data(
    offers_model,
    txs_model,
    round: int,
) -> Dict[str, List[Dict[str, Any]]]:
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
    for entry in mod.filter_entries(offers_model, Offer, round=round):
        player_offers[entry.pid] = (entry.id, entry.buy, entry.price)

    # Partition valid offers into market sides
    market_book = {"asks": [], "bids": []}

    for offer_id, is_buy, price in player_offers.values():
        if price is None:  # Skip cancelled offers
            continue

        offer_data = {"id": offer_id, "price": price}
        side_key = "bids" if is_buy else "asks"
        market_book[side_key].append(offer_data)

    # Append executed transactions
    market_book["txs"] = mod.filter_entries(txs_model, Transaction, round=round)

    return market_book


def calculate_profit(
    player,
    price: float,
) -> float:
    """
    Calculate trading profit based on player type

    Buyers: profit = value - price (positive when buying below value)
    Sellers: profit = price - cost (positive when selling above cost)
    """
    if player.buyer:
        return player.cost_or_value - price
    else:
        return price - player.cost_or_value


def broadcast_market_update(
    session,
    round: int,
):
    """Send updated market state to all participants"""
    send_to(
        players(session),
        market_data(session.offers, session.txs, round),
        "OffersAndTxs",
    )


def create_offer_entry(
    session,
    player,
    offer_id: str,
    round: int,
    is_buy: bool,
    price: Optional[float],
):
    """Helper to create and store an offer"""
    mod.add_entry(
        session.offers,
        player,
        Offer,
        id=offer_id,
        round=round,
        buy=is_buy,
        price=price,
    )


def validate_offer(
    offers_model,
    offer_id: str,
    round: int,
) -> Optional[Offer]:
    """
    Validate that an offer exists and is active

    Returns the offer if valid, None if invalid/cancelled
    """
    candidates = mod.filter_entries(
        offers_model,
        Offer,
        id=offer_id,
        round=round,
    )

    if not candidates or candidates[0].price is None:
        return None

    target_offer = candidates[0]
    latest_offer = None

    # Verify this is the player's current active offer
    for entry in mod.filter_entries(offers_model, Offer, round=round):
        if entry.pid == target_offer.pid:
            latest_offer = entry

    if latest_offer.id != target_offer.id:
        return None  # Player has a newer offer

    return target_offer


class Trade(Page):
    """
    Trading interface page where participants submit and accept offers

    Each player receives a private value (buyers) or cost (sellers) and
    can profit by trading at favorable prices. The market operates as
    a continuous double auction with immediate execution.
    """

    timeout = 25 * 60

    @classmethod
    def before_once(page, player):
        """
        Initialize player with role and private value/cost

        Buyers (even IDs) receive values they're willing to pay
        Sellers (odd IDs) receive costs they must cover
        """
        player.buyer = player.id % 2 == 0
        player.cost_or_value = randint(1, 10)
        player.offer = None  # Current offer ID
        player.trade = None  # Executed trade ID
        player.profit = None  # Realized profit/loss

    @classmethod
    async def jsvars(page, player):
        if player.offer is None:
            return dict(offer_amount=None)
        else:
            offer = validate_offer(
                player.session.offers,
                player.offer,
                player.round,
            )

            if offer is None:
                return dict(offer_amount=None)
            else:
                return dict(offer_amount=offer.price)

    @live
    async def get_market(page, player):
        return market_data(player.session.offers, player.session.txs, player.round)

    @live
    async def make_offer(page, player, amount: Optional[float]):
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

        if amount is not None and amount < 0:
            raise ValueError(f"Bad amount: {amount}")

        offer_id = uuid()
        create_offer_entry(
            player.session,
            player,
            offer_id,
            player.round,
            player.buyer,
            amount,
        )
        player.offer = offer_id

        broadcast_market_update(player.session, player.round)
        return amount

    @live
    async def accept_offer(page, player, offer_id: str):
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
        offer = validate_offer(player.session.offers, offer_id, player.round)

        if offer.buy == player.buyer:
            raise ValueError("Buyer cannot sell, seller cannot buy")

        if not offer:
            raise ValueError("Offer no longer valid")

        # Cancel proposer's offer to prevent double-trading
        create_offer_entry(
            player.session,
            offer.pid,
            uuid(),
            player.round,
            not player.buyer,  # Opposite side (double auction mechanics)
            None,  # Null price cancels
        )

        # Execute trade
        tx_id = uuid()

        # Update proposer
        proposer = offer.pid()
        proposer.trade = tx_id
        proposer.profit = calculate_profit(proposer, offer.price)
        send_to(proposer, [True, proposer.profit], "OfferAccepted")

        # Update acceptor
        player.trade = tx_id
        player.profit = calculate_profit(player, offer.price)

        # Record transaction
        mod.add_entry(
            player.session.txs,
            player,
            Transaction,
            id=tx_id,
            round=player.round,
            offer_id=offer.id,
            price=offer.price,
        )

        broadcast_market_update(player.session, player.round)
        return player.profit


page_order = [
    Rounds(
        Trade,
        n=1,
    )
]
