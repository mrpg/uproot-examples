# Equilibrium finder for unit-demand/unit-supply double auctions.
# Adapted from https://github.com/mrpg/find-eq (0BSD license).

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class Equilibrium:
    """Result of market clearing in a double auction.

    Attributes:
        price_min: Lower bound of the clearing price interval (inclusive).
        price_max: Upper bound of the clearing price interval (inclusive).
        quantity: Number of units traded at equilibrium.

    Any price p in [price_min, price_max] clears the market at the
    equilibrium quantity.
    """

    price_min: Decimal
    price_max: Decimal
    quantity: int


def find_equilibrium(bids: list[Decimal], asks: list[Decimal]) -> Equilibrium | None:
    """Find the competitive equilibrium in a unit-demand/unit-supply double auction.

    Each bid represents a buyer's maximum willingness to pay for exactly one
    indivisible unit. Each ask represents a seller's minimum acceptable price
    for exactly one indivisible unit. The market clears at the maximum quantity
    where gains from trade are non-negative.

    Args:
        bids: Reservation prices of buyers (one per buyer).
        asks: Reservation prices of sellers (one per seller).

    Returns:
        An Equilibrium object containing the clearing price interval and
        quantity. When no trade is possible (all asks exceed all bids),
        quantity is 0 and the price interval spans [max(bids), min(asks)].
        Returns None only if bids or asks is empty (no market exists).

    Example:
        >>> from decimal import Decimal
        >>> bids = [Decimal("10"), Decimal("8"), Decimal("6")]
        >>> asks = [Decimal("5"), Decimal("7"), Decimal("9")]
        >>> eq = find_equilibrium(bids, asks)
        >>> eq.quantity
        2
        >>> eq.price_min  # Marginal seller's ask
        Decimal('7')
        >>> eq.price_max  # Marginal buyer's bid
        Decimal('8')
    """
    if not bids or not asks:
        return None

    # Sort to construct demand and supply schedules.
    # Demand: bids in descending order (highest willingness to pay first).
    # Supply: asks in ascending order (lowest reservation price first).
    bids_sorted = sorted(bids, reverse=True)
    asks_sorted = sorted(asks)

    # Find the maximum tradeable quantity.
    # Trade k units iff the k-th highest bid >= k-th lowest ask,
    # i.e., the k-th buyer's surplus from trading with the k-th seller
    # is non-negative.
    max_quantity = 0
    for k in range(1, min(len(bids_sorted), len(asks_sorted)) + 1):
        if bids_sorted[k - 1] >= asks_sorted[k - 1]:
            max_quantity = k
        else:
            # Since bids_sorted is non-increasing and asks_sorted is
            # non-decreasing, no larger k can satisfy the condition.
            break

    if max_quantity == 0:
        # No trade, but an equilibrium still exists: any price in
        # [max(bids), min(asks)] clears the market at quantity 0.
        return Equilibrium(
            price_min=bids_sorted[0],
            price_max=asks_sorted[0],
            quantity=0,
        )

    # The clearing price interval [p_min, p_max] must ensure demand == supply.
    # Start with marginal traders' values.
    price_min = asks_sorted[max_quantity - 1]
    price_max = bids_sorted[max_quantity - 1]

    # Tighten interval to exclude non-trading agents:
    # - price_min >= excluded buyer's bid (so they don't demand)
    # - price_max <= excluded seller's ask (so they don't supply)
    if max_quantity < len(bids_sorted):
        price_min = max(price_min, bids_sorted[max_quantity])
    if max_quantity < len(asks_sorted):
        price_max = min(price_max, asks_sorted[max_quantity])

    return Equilibrium(price_min=price_min, price_max=price_max, quantity=max_quantity)
