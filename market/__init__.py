# Docs are available at https://uproot.science/
# Examples are available at https://github.com/mrpg/uproot-examples
#
# This example app is under the 0BSD license. You can use it freely and build on it
# without any limitations and without any attribution. However, these two lines must be
# preserved in any uproot app (the license file is automatically installed in projects):
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt

from dataclasses import replace
from decimal import Decimal
from typing import Any, Optional

import uproot.models as um
from mini_exchange import Exchange, Order
from mini_exchange import Trade as METrade
from uproot.fields import *
from uproot.smithereens import *

DESCRIPTION = "Continuous market (limit order book)"
LANDING_PAGE = False


class BookEvent(metaclass=um.Entry):
    action: str
    order_id: str
    price: str
    quantity: str
    buy: bool
    user: str
    time: float


class TradeEvent(metaclass=um.Entry):
    buyer: str
    seller: str
    price: str
    quantity: str
    timestamp: float


_exchanges: dict[str, Exchange] = {}


def _exchange_key(session):
    return str(session.book_model)


def reconstruct_exchange(session) -> Exchange:
    exchange = Exchange()

    if session.get("book_model") is None:
        return exchange

    resting: dict[str, Order] = {}
    for _, _, book_event in um.get_entries(session.book_model, BookEvent):
        if book_event.action == "add":
            order = Order(
                id=book_event.order_id,
                price=Decimal(book_event.price),
                quantity=Decimal(book_event.quantity),
                buy=book_event.buy,
                user=book_event.user,
                time=book_event.time,
            )
            resting[book_event.order_id] = order
        elif book_event.action == "remove":
            resting.pop(book_event.order_id, None)
        elif book_event.action == "update":
            if book_event.order_id in resting:
                old = resting[book_event.order_id]
                resting[book_event.order_id] = replace(
                    old, quantity=Decimal(book_event.quantity)
                )

    for order in resting.values():
        side = exchange.bids if order.buy else exchange.asks
        side.add(order)
        exchange.orders[order.id] = order

    if session.get("trade_model") is not None:
        for _, _, trade_event in um.get_entries(session.trade_model, TradeEvent):
            exchange.trades.append(
                METrade(
                    buyer=trade_event.buyer,
                    seller=trade_event.seller,
                    price=Decimal(trade_event.price),
                    quantity=Decimal(trade_event.quantity),
                    timestamp=trade_event.timestamp,
                )
            )

    return exchange


def get_exchange(session) -> Exchange:
    key = _exchange_key(session)
    if key not in _exchanges:
        _exchanges[key] = reconstruct_exchange(session)
    return _exchanges[key]


def new_session(session: SessionType) -> None:
    session.book_model = um.create_model(session, tag="book_events")
    session.trade_model = um.create_model(session, tag="trade_events")


def store_book_changes(session, player, before_orders, after_orders, trades):
    for oid in set(before_orders) - set(after_orders):
        o = before_orders[oid]
        um.add_entry(
            session.book_model,
            player,
            BookEvent,
            action="remove",
            order_id=o.id,
            price=str(o.price),
            quantity="0",
            buy=o.buy,
            user=o.user,
            time=o.time,
        )

    for oid in set(before_orders) & set(after_orders):
        if after_orders[oid].quantity != before_orders[oid].quantity:
            o = after_orders[oid]
            um.add_entry(
                session.book_model,
                player,
                BookEvent,
                action="update",
                order_id=o.id,
                price=str(o.price),
                quantity=str(o.quantity),
                buy=o.buy,
                user=o.user,
                time=o.time,
            )

    for oid in set(after_orders) - set(before_orders):
        o = after_orders[oid]
        um.add_entry(
            session.book_model,
            player,
            BookEvent,
            action="add",
            order_id=o.id,
            price=str(o.price),
            quantity=str(o.quantity),
            buy=o.buy,
            user=o.user,
            time=o.time,
        )

    for trade in trades:
        um.add_entry(
            session.trade_model,
            player,
            TradeEvent,
            buyer=trade.buyer,
            seller=trade.seller,
            price=str(trade.price),
            quantity=str(trade.quantity),
            timestamp=trade.timestamp,
        )


def update_portfolios(session, trades):
    players_by_name = {p.name: p for p in session.players}
    for trade in trades:
        amount = trade.price * trade.quantity
        buyer = players_by_name.get(trade.buyer)
        if buyer is not None:
            buyer.cash = str(Decimal(buyer.get("cash") or "0") - amount)
            buyer.stock = int(buyer.get("stock") or 0) + int(trade.quantity)
        seller = players_by_name.get(trade.seller)
        if seller is not None:
            seller.cash = str(Decimal(seller.get("cash") or "0") + amount)
            seller.stock = int(seller.get("stock") or 0) - int(trade.quantity)


def get_book_snapshot(exchange):
    asks: dict[str, dict[str, Any]] = {}
    for order in exchange.asks:
        p = str(order.price)
        if p not in asks:
            asks[p] = {"price": str(order.price), "quantity": 0, "orders": []}
        asks[p]["quantity"] += int(order.quantity)
        asks[p]["orders"].append({"id": order.id, "quantity": int(order.quantity)})

    bids: dict[str, dict[str, Any]] = {}
    for order in exchange.bids:
        p = str(order.price)
        if p not in bids:
            bids[p] = {"price": str(order.price), "quantity": 0, "orders": []}
        bids[p]["quantity"] += int(order.quantity)
        bids[p]["orders"].append({"id": order.id, "quantity": int(order.quantity)})

    return {
        "asks": sorted(asks.values(), key=lambda x: Decimal(x["price"])),
        "bids": sorted(bids.values(), key=lambda x: Decimal(x["price"]), reverse=True),
    }


def get_player_orders(exchange, player_name):
    orders = []
    for oid, order in exchange.orders.items():
        if order.user == player_name:
            orders.append(
                {
                    "id": order.id,
                    "price": str(order.price),
                    "quantity": int(order.quantity),
                    "side": "buy" if order.buy else "sell",
                }
            )
    return orders


def get_recent_trades(exchange, limit=50):
    trades = []
    for trade in exchange.trades[-limit:]:
        trades.append(
            {
                "price": str(trade.price),
                "quantity": int(trade.quantity),
            }
        )
    return trades


def broadcast_update(player, session, exchange):
    book = get_book_snapshot(exchange)
    trades = get_recent_trades(exchange)
    notify(
        player,
        session.players,
        {"book": book, "trades": trades},
        event="MarketUpdate",
    )


class Trading(Page):
    @classmethod
    def before_once(page, player: PlayerType) -> None:
        if player.get("cash") is None:
            player.cash = "0"
        if player.get("stock") is None:
            player.stock = 0

    @live
    def get_state(page, player):
        exchange = get_exchange(player.session)
        book = get_book_snapshot(exchange)
        trades = get_recent_trades(exchange)
        my_orders = get_player_orders(exchange, player.name)
        return {
            "book": book,
            "trades": trades,
            "my_orders": my_orders,
            "cash": player.get("cash") or "0",
            "stock": int(player.get("stock") or 0),
        }

    @live
    def submit_order(
        page,
        player,
        order_type: str,
        side: str,
        price: Optional[str],
        quantity: int,
    ):
        if order_type not in ("limit", "market"):
            raise ValueError("order_type must be 'limit' or 'market'")
        if side not in ("buy", "sell"):
            raise ValueError("side must be 'buy' or 'sell'")
        if quantity <= 0:
            raise ValueError("quantity must be positive")

        session = player.session
        exchange = get_exchange(session)
        is_buy = side == "buy"

        if order_type == "limit":
            if price is None:
                raise ValueError("Price required for limit orders")
            dec_price = Decimal(price)
            if dec_price <= 0:
                raise ValueError("Price must be positive")
        else:
            if is_buy:
                if not exchange.asks:
                    raise ValueError("No sell orders available")
                dec_price = max(order.price for order in exchange.asks)
            else:
                if not exchange.bids:
                    raise ValueError("No buy orders available")
                dec_price = min(order.price for order in exchange.bids)

        before_orders = dict(exchange.orders)

        try:
            order, trades = exchange.place(
                dec_price, Decimal(quantity), player.name, is_buy
            )
        except ValueError as e:
            raise ValueError(str(e))

        # For market orders, cancel any resting remainder
        if order_type == "market" and order.quantity > 0:
            exchange.cancel(order.id)

        after_orders = dict(exchange.orders)
        store_book_changes(session, player, before_orders, after_orders, trades)
        update_portfolios(session, trades)
        broadcast_update(player, session, exchange)

        return {
            "cash": player.get("cash") or "0",
            "stock": int(player.get("stock") or 0),
        }

    @live
    def cancel_order(page, player, order_id: str):
        session = player.session
        exchange = get_exchange(session)

        if order_id not in exchange.orders:
            raise ValueError("Order not found")
        if exchange.orders[order_id].user != player.name:
            raise ValueError("Cannot cancel another player's order")

        before_orders = dict(exchange.orders)
        exchange.cancel(order_id)
        after_orders = dict(exchange.orders)

        store_book_changes(session, player, before_orders, after_orders, [])
        broadcast_update(player, session, exchange)

        return {
            "cash": player.get("cash") or "0",
            "stock": int(player.get("stock") or 0),
        }


page_order = [Trading]
