# Docs are available at https://uproot.science/
# Examples are available at https://github.com/mrpg/uproot-examples
#
# This example app is under the 0BSD license. You can use it freely and build on it
# without any limitations and without any attribution. However, these two lines must be
# preserved in any uproot app (the license file is automatically installed in projects):
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt

import math

import uproot.models as um
from uproot.fields import *
from uproot.smithereens import *

DESCRIPTION = "Prediction market (LMSR)"
LANDING_PAGE = False


class C:
    ENDOWMENT = 100
    LIQUIDITY = 100
    EVENT_QUESTION = "Will the drawn number be greater than 50?"


# --- Logarithmic Market Scoring Rule (Hanson, 2003) ---


def lmsr_cost(q_yes, q_no, b):
    x, y = q_yes / b, q_no / b
    m = max(x, y)

    return b * (m + math.log(math.exp(x - m) + math.exp(y - m)))


def lmsr_prices(q_yes, q_no, b):
    x, y = q_yes / b, q_no / b
    m = max(x, y)
    ex = math.exp(x - m)
    ey = math.exp(y - m)
    s = ex + ey

    return ex / s, ey / s


def compute_buy_cost(q_yes, q_no, b, is_yes, shares):
    if is_yes:
        return lmsr_cost(q_yes + shares, q_no, b) - lmsr_cost(q_yes, q_no, b)

    return lmsr_cost(q_yes, q_no + shares, b) - lmsr_cost(q_yes, q_no, b)


def compute_sell_revenue(q_yes, q_no, b, is_yes, shares):
    if is_yes:
        return lmsr_cost(q_yes, q_no, b) - lmsr_cost(q_yes - shares, q_no, b)

    return lmsr_cost(q_yes, q_no, b) - lmsr_cost(q_yes, q_no - shares, b)


# --- Data Model ---


class TradeEntry(metaclass=um.Entry):
    outcome: str
    action: str
    shares: int
    total_cost: float
    price_yes_after: float
    price_no_after: float


def new_session(session):
    session.q_yes = 0
    session.q_no = 0
    session.trade_log = um.create_model(session, tag="trades")


# --- Pages ---


class Instructions(Page):
    pass


class Trading(Page):
    @classmethod
    def before_once(page, player):
        if player.get("cash") is None:
            player.cash = float(C.ENDOWMENT)

        if player.get("yes_shares") is None:
            player.yes_shares = 0

        if player.get("no_shares") is None:
            player.no_shares = 0

    @classmethod
    def may_proceed(page, player):
        return player.session.get("event_resolved") is True

    @live
    def get_state(page, player):
        session = player.session
        q_yes = session.get("q_yes") or 0
        q_no = session.get("q_no") or 0
        p_yes, p_no = lmsr_prices(q_yes, q_no, C.LIQUIDITY)

        trades = []

        if session.get("trade_log") is not None:
            for _, _, entry in um.get_entries(session.trade_log, TradeEntry):
                trades.append(
                    {
                        "outcome": entry.outcome,
                        "action": entry.action,
                        "shares": entry.shares,
                        "total_cost": round(entry.total_cost, 2),
                        "price_yes": round(entry.price_yes_after, 4),
                    }
                )

        return {
            "price_yes": round(p_yes, 4),
            "price_no": round(p_no, 4),
            "q_yes": q_yes,
            "q_no": q_no,
            "cash": round(float(player.get("cash") or 0), 2),
            "yes_shares": player.get("yes_shares") or 0,
            "no_shares": player.get("no_shares") or 0,
            "trades": trades[-50:],
            "resolved": session.get("event_resolved") is True,
        }

    @live
    def trade(page, player, outcome: str, action: str, shares: int):
        if outcome not in ("yes", "no"):
            raise ValueError("Invalid outcome")

        if action not in ("buy", "sell"):
            raise ValueError("Invalid action")

        if shares <= 0:
            raise ValueError("Shares must be at least 1")

        if player.session.get("event_resolved"):
            raise ValueError("Market is closed")

        session = player.session
        b = C.LIQUIDITY
        is_yes = outcome == "yes"
        q_yes = session.get("q_yes") or 0
        q_no = session.get("q_no") or 0

        if action == "buy":
            cost = round(compute_buy_cost(q_yes, q_no, b, is_yes, shares), 2)
            cash = float(player.get("cash") or 0)

            if cost > cash + 0.005:
                raise ValueError("Insufficient funds")

            player.cash = round(cash - cost, 2)

            if is_yes:
                player.yes_shares = (player.get("yes_shares") or 0) + shares
                session.q_yes = q_yes + shares
            else:
                player.no_shares = (player.get("no_shares") or 0) + shares
                session.q_no = q_no + shares

            total_cost = cost
        else:
            held = (
                player.get("yes_shares") if is_yes else player.get("no_shares")
            ) or 0

            if shares > held:
                raise ValueError(
                    f"You only hold {held} {outcome.capitalize()} contracts"
                )

            revenue = round(compute_sell_revenue(q_yes, q_no, b, is_yes, shares), 2)
            player.cash = round(float(player.get("cash") or 0) + revenue, 2)

            if is_yes:
                player.yes_shares = held - shares
                session.q_yes = q_yes - shares
            else:
                player.no_shares = held - shares
                session.q_no = q_no - shares

            total_cost = -revenue

        new_q_yes = session.get("q_yes") or 0
        new_q_no = session.get("q_no") or 0
        p_yes, p_no = lmsr_prices(new_q_yes, new_q_no, b)

        if session.get("trade_log") is None:
            session.trade_log = um.create_model(session, tag="trades")

        um.add_entry(
            session.trade_log,
            player,
            TradeEntry,
            outcome=outcome,
            action=action,
            shares=shares,
            total_cost=total_cost,
            price_yes_after=p_yes,
            price_no_after=p_no,
        )

        notify(
            player,
            session.players,
            {
                "price_yes": round(p_yes, 4),
                "price_no": round(p_no, 4),
                "q_yes": new_q_yes,
                "q_no": new_q_no,
                "trade": {
                    "outcome": outcome,
                    "action": action,
                    "shares": shares,
                    "total_cost": round(total_cost, 2),
                    "price_yes": round(p_yes, 4),
                },
            },
            event="PriceUpdate",
        )

        return {
            "price_yes": round(p_yes, 4),
            "price_no": round(p_no, 4),
            "cash": round(float(player.cash), 2),
            "yes_shares": player.yes_shares,
            "no_shares": player.no_shares,
        }


def settle_player(player):
    player.app = __name__  # HACK

    session = player.session
    yes_payout = 1 if session.event_occurred else 0
    no_payout = 1 - yes_payout
    yes_shares = player.get("yes_shares") or 0
    no_shares = player.get("no_shares") or 0
    cash_val = player.get("cash")
    cash = float(cash_val) if cash_val is not None else float(C.ENDOWMENT)
    contract_payout = yes_shares * yes_payout + no_shares * no_payout
    payoff = round(cash + contract_payout, 2)

    player.contract_payout = contract_payout
    player.payoff = cu(f"{payoff:.2f}")


class Results(Page):
    pass


# --- Digest ---


def digest(session):
    q_yes = session.get("q_yes") or 0
    q_no = session.get("q_no") or 0
    p_yes, p_no = lmsr_prices(q_yes, q_no, C.LIQUIDITY)

    price_history = [0.5]
    trades = []

    if session.get("trade_log") is not None:
        for _, _, entry in um.get_entries(session.trade_log, TradeEntry):
            price_history.append(round(entry.price_yes_after, 4))
            trades.append(
                {
                    "outcome": entry.outcome,
                    "action": entry.action,
                    "shares": entry.shares,
                    "total_cost": round(entry.total_cost, 2),
                    "price_yes": round(entry.price_yes_after, 4),
                }
            )

    positions = []

    for player in session.players:
        player_data = player.within(app=__name__)
        cash = player_data.get("cash")

        if cash is None:
            continue

        positions.append(
            {
                "name": player.name,
                "cash": round(float(cash), 2),
                "yes_shares": player_data.get("yes_shares") or 0,
                "no_shares": player_data.get("no_shares") or 0,
                "payoff": player_data.get("payoff"),
            }
        )

    return {
        "event_question": C.EVENT_QUESTION,
        "price_yes": round(p_yes, 4),
        "price_no": round(p_no, 4),
        "q_yes": q_yes,
        "q_no": q_no,
        "price_history": price_history,
        "num_trades": len(trades),
        "trades": trades,
        "positions": positions,
        "resolved": session.get("event_resolved") is True,
        "event_occurred": session.get("event_occurred"),
    }


# --- Pipeline ---


def resolve_event(session, event_value):
    """Resolve the event, move players to Results."""
    if session.get("event_resolved"):
        return True

    session.event_occurred = bool(int(event_value))
    session.event_resolved = True

    for player in session.players:
        settle_player(player)
        move_to_page(player, Results)

    return True


def pipeline(session, data=None):
    if data and "event" in data:
        resolve_event(session, data["event"])

    rows = []

    for player in session.players:
        player_data = player.within(app=__name__)
        cash = player_data.get("cash")

        if cash is None:
            continue

        rows.append(
            {
                "session": session.name,
                "uname": player.name,
                "endowment": C.ENDOWMENT,
                "final_cash": round(float(cash), 2),
                "yes_shares": player_data.get("yes_shares") or 0,
                "no_shares": player_data.get("no_shares") or 0,
                "event_occurred": session.get("event_occurred"),
                "contract_payout": player_data.get("contract_payout"),
                "payoff": player_data.get("payoff"),
            }
        )

    return rows


page_order = [
    Instructions,
    Trading,
    Results,
]
