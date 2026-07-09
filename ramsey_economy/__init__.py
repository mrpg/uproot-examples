# Docs are available at https://uproot.science/
# Examples are available at https://github.com/mrpg/uproot-examples
#
# This example app is under the 0BSD license. You can use it freely and build on it
# without any limitations and without any attribution. However, these two lines must be
# preserved in any uproot app (the license file is automatically installed in projects):
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt

from decimal import ROUND_FLOOR, ROUND_HALF_UP, Decimal
from io import BytesIO

from fastapi import HTTPException
from fastapi.responses import Response
from PIL import Image, ImageDraw, ImageFont
from uproot.fields import *
from uproot.smithereens import *

DESCRIPTION = "A miniature laboratory economy (Ramsey model)"
SUGGESTED_MULTIPLE = 3


CENT = Decimal("0.01")
ONE = Decimal("1")
ZERO = Decimal("0")


def decimal_value(value: Any) -> Decimal:
    if isinstance(value, Decimal):
        return value

    return Decimal(str(value))


def cents_floor(value: Any) -> Decimal:
    """Largest cent value that does not exceed value."""

    return decimal_value(value).quantize(CENT, rounding=ROUND_FLOOR)


def cents_round(value: Any) -> Decimal:
    return decimal_value(value).quantize(CENT, rounding=ROUND_HALF_UP)


def redemption(c: Any) -> Decimal:
    """Redemption value u(c) = 2 sqrt(c)."""
    c = decimal_value(c)

    if c <= ZERO:
        return ZERO

    return cents_round(Decimal("2") * c.sqrt())


class C:
    GROUP_SIZE = 3

    # Production: Y = A K^alpha L^(1-alpha)
    A = 3.0
    ALPHA = 1 / 3

    # Continuation probability (configurable via session settings key "beta")
    DEFAULT_BETA = 0.9

    # Depreciation rate
    DELTA = Decimal("0.2")

    # Maximum labor supply (number of captchas per round)
    L_BAR = 10

    # Initial capital per player
    K_BAR = Decimal("20")

    # Default tax rates (configurable via session settings keys "tau_l", "tau_k")
    DEFAULT_TAU_L = 0.0
    DEFAULT_TAU_K = 0.0

    # Captcha settings
    CAPTCHA_LENGTH = 5
    CAPTCHA_CHARACTERS = "0123456789"
    IMAGE_WIDTH = 180
    IMAGE_HEIGHT = 70
    BACKGROUND_COLOR = "white"
    FONT_SIZE = 38
    LINE_COUNT = 12
    TEXT_COLOR = (40, 55, 75)
    LINE_COLOR_MIN = 130
    LINE_COLOR_MAX = 220
    DIGIT_VERTICAL_JITTER = 4

    # Redemption value lookup table: (consumption, u(consumption))
    REDEMPTION_TABLE = [
        (c, redemption(c)) for c in [0, 1, 2, 5, 10, 15, 20, 25, 30, 40, 50]
    ]

    __export__ = ["L_BAR", "CAPTCHA_LENGTH", "IMAGE_WIDTH", "IMAGE_HEIGHT"]


# -- Helpers ---------------------------------------------------------------


def unit_interval_setting(session: SessionType, key: str, default: float) -> float:
    try:
        value = float(session.settings.get(key, default))
    except (TypeError, ValueError):
        value = default

    return min(1.0, max(0.0, value))


def get_capital(player: PlayerType) -> Any:
    """Return the player's capital at the start of the current round."""

    if player.round == 1:
        return C.K_BAR

    prev = player.within(app=__name__, round=player.round - 1)

    return prev.get("next_capital", C.K_BAR)


def get_settings(session: SessionType) -> dict[str, float]:
    """Read configurable parameters from session settings."""

    return {
        "tau_l": unit_interval_setting(session, "tau_l", C.DEFAULT_TAU_L),
        "tau_k": unit_interval_setting(session, "tau_k", C.DEFAULT_TAU_K),
        "beta": unit_interval_setting(session, "beta", C.DEFAULT_BETA),
    }


def get_cumulative_earnings(player: PlayerType) -> Any:
    """Sum of redemption values from all completed prior rounds."""

    if player.round <= 1:
        return ZERO

    prev = player.within(app=__name__, round=player.round - 1)

    return prev.get("cumulative_earnings", ZERO)


class Context(PlayerContext):
    @property
    def capital(self) -> Any:
        return get_capital(self.player)

    @property
    def cumulative_earnings(self) -> Any:
        return get_cumulative_earnings(self.player)

    @property
    def settings(self) -> dict[str, float]:
        return get_settings(self.player.session)


# -- Captcha ---------------------------------------------------------------


def make_captcha_code() -> str:
    r = rng()

    return "".join(r.choice(C.CAPTCHA_CHARACTERS) for _ in range(C.CAPTCHA_LENGTH))


def captcha_png(code: str) -> bytes:
    from random import Random as PyRandom

    r = PyRandom(code)
    image = Image.new("RGB", (C.IMAGE_WIDTH, C.IMAGE_HEIGHT), C.BACKGROUND_COLOR)
    draw = ImageDraw.Draw(image)

    for _ in range(C.LINE_COUNT):
        start = (r.randint(0, C.IMAGE_WIDTH), r.randint(0, C.IMAGE_HEIGHT))
        end = (r.randint(0, C.IMAGE_WIDTH), r.randint(0, C.IMAGE_HEIGHT))
        color = tuple(r.randint(C.LINE_COLOR_MIN, C.LINE_COLOR_MAX) for _ in range(3))
        draw.line([start, end], fill=color, width=1)

    try:
        font = ImageFont.load_default(size=C.FONT_SIZE)
    except TypeError:
        font = ImageFont.load_default()

    left, top, right, bottom = draw.textbbox((0, 0), code, font=font)
    text_width = right - left
    x = (C.IMAGE_WIDTH - text_width) // 2
    y = (C.IMAGE_HEIGHT - (bottom - top)) // 2 - top

    for i, digit in enumerate(code):
        offset = i * (text_width // len(code))
        draw.text(
            (
                x + offset,
                y + r.randint(-C.DIGIT_VERTICAL_JITTER, C.DIGIT_VERTICAL_JITTER),
            ),
            digit,
            fill=C.TEXT_COLOR,
            font=font,
        )

    buffer = BytesIO()
    image.save(buffer, format="PNG")

    return buffer.getvalue()


# -- Pages -----------------------------------------------------------------


class GroupPlease(GroupCreatingWait):
    group_size = C.GROUP_SIZE


class Instructions(Page):
    pass


class LaborTask(Page):
    @classmethod
    def before_once(page, player: PlayerType) -> None:
        player.effort = 0
        player.captcha_code = None

    @live
    def new_captcha(page, player: PlayerType) -> Any:
        effort = player.get("effort")

        if effort is None:
            effort = 0
            player.effort = 0

        if effort >= C.L_BAR:
            return {"done": True, "effort": effort}

        player.captcha_code = make_captcha_code()

        return {"done": False, "effort": effort}

    @live
    def check_captcha(page, player: PlayerType, answer: str) -> Any:
        effort = min(max(0, player.get("effort") or 0), C.L_BAR)

        if effort >= C.L_BAR:
            player.effort = C.L_BAR
            player.captcha_code = None

            return {"correct": False, "done": True, "effort": C.L_BAR}

        if player.captcha_code is None:
            return {"correct": False, "effort": effort}

        if answer.strip() == player.captcha_code:
            effort = min(effort + 1, C.L_BAR)
            player.effort = effort

            if effort >= C.L_BAR:
                player.captcha_code = None

                return {"correct": True, "done": True, "effort": effort}

            player.captcha_code = make_captcha_code()

            return {"correct": True, "done": False, "effort": effort}

        return {"correct": False, "done": False, "effort": effort}

    @live
    def set_effort(page, player: PlayerType, effort: int) -> None:
        if not player.session._uproot_simulate:
            return

        player.effort = min(max(0, int(effort)), C.L_BAR)


class SyncLabor(SynchronizingWait):
    @classmethod
    def all_here(page, group: GroupType) -> None:
        settings = get_settings(group.session)
        tau_l = settings["tau_l"]
        tau_k = settings["tau_k"]
        n = C.GROUP_SIZE

        capitals = []
        labors = []

        for p in group.players:
            capitals.append(decimal_value(get_capital(p)))
            labors.append(p.get("effort") or 0)

        aggregate_capital = sum(capitals, ZERO)
        K = float(aggregate_capital)
        L = sum(labors)

        # Production is computed in float because exponentiation with fractional
        # alpha is natural there. The results are safe to use: every value that
        # reaches a player passes through cents_floor(), which truncates to the
        # nearest cent below, so floating-point rounding cannot inflate payoffs.
        if K <= 0 or L <= 0:
            for i, p in enumerate(group.players):
                p.wage = 0.0
                p.rental_rate = 0.0
                p.output = 0.0
                p.aggregate_capital = aggregate_capital
                p.aggregate_labor = L
                p.labor_income = ZERO
                p.capital_return = ZERO
                p.transfer = ZERO
                p.own_capital = capitals[i]
                p.resources = cents_floor(max(ZERO, (ONE - C.DELTA) * capitals[i]))
        else:
            Y = C.A * K**C.ALPHA * L ** (1 - C.ALPHA)
            w = (1 - C.ALPHA) * C.A * K**C.ALPHA * L ** (-C.ALPHA)
            r = C.ALPHA * C.A * K ** (C.ALPHA - 1) * L ** (1 - C.ALPHA)
            T = (tau_l * w * L + tau_k * r * K) / n

            for i, p in enumerate(group.players):
                k_i = capitals[i]
                l_i = labors[i]

                labor_inc = cents_floor((1 - tau_l) * w * l_i)
                capital_ret = cents_floor((1 - tau_k) * r * float(k_i))
                transfer = cents_floor(T)
                undepreciated = cents_floor((ONE - C.DELTA) * k_i)
                W_i = labor_inc + capital_ret + undepreciated + transfer

                p.wage = w
                p.rental_rate = r
                p.output = Y
                p.aggregate_capital = aggregate_capital
                p.aggregate_labor = L
                p.labor_income = labor_inc
                p.capital_return = capital_ret
                p.transfer = transfer
                p.own_capital = k_i
                p.resources = max(ZERO, W_i)


class ConsumptionChoice(Page):
    @classmethod
    def fields(page, player: PlayerType) -> dict[str, Field]:
        max_c = max(ZERO, decimal_value(player.resources))

        return dict(
            consumption=DecimalField(
                label="How much do you want to consume?",
                description="The remainder will be saved as capital for the next period.",
                min=0,
                max=max_c,
                step=CENT,
                places=2,
                addon_end=f"out of {max_c:.2f}",
            ),
        )


class SyncRound(SynchronizingWait):
    @classmethod
    def all_here(page, group: GroupType) -> None:
        settings = get_settings(group.session)
        beta = settings["beta"]
        continue_game = rng().random() < beta

        for p in group.players:
            c = decimal_value(p.consumption)
            rv = redemption(c)
            cumulative_earnings = get_cumulative_earnings(p) + rv

            p.redemption_value = rv
            p.next_capital = cents_floor(max(ZERO, p.resources - c))
            p.cumulative_earnings = cumulative_earnings
            p.payoff = cumulative_earnings
            p.add_round = continue_game


class RoundResults(Page):
    pass


# -- Captcha image API -----------------------------------------------------


async def api2(session: SessionType, request: Any) -> Response:
    uname = request.query_params.get("uname")

    if uname not in {player.name for player in session.players}:
        raise HTTPException(status_code=404, detail="Unknown player")

    with Player(session.name, uname) as player:
        code = player.captcha_code

    if not code:
        raise HTTPException(status_code=404, detail="No captcha")

    return Response(
        content=captcha_png(code),
        media_type="image/png",
        headers={"Cache-Control": "no-store"},
    )


# -- Data export ------------------------------------------------------------


def played_rounds(*players: PlayerType) -> list[int]:
    return sorted(
        {
            round_num
            for player in players
            for round_num, _ in player.within(app=__name__).along("round")
        }
    )


def digest(session: SessionType) -> list[Any]:
    data = []

    for group in session.groups(app=__name__):
        players = group.players
        rounds = played_rounds(*players)
        latest_round = rounds[-1] if rounds else 0

        history = []

        for round_num in rounds:
            round_data = []

            for p in players:
                pd = p.within.strict(app=__name__, round=round_num)
                round_data.append(
                    {
                        "effort": pd.get("effort"),
                        "own_capital": pd.get("own_capital"),
                        "consumption": pd.get("consumption"),
                        "next_capital": pd.get("next_capital"),
                        "redemption_value": pd.get("redemption_value"),
                    }
                )

            history.append((round_num, round_data))

        data.append((group.name, latest_round, history, [p.name for p in players]))

    return data


def pipeline(session: SessionType) -> list[dict[str, Any]]:
    rows = []
    settings = get_settings(session)

    for group in session.groups(app=__name__):
        players = group.players
        rounds = played_rounds(*players)

        for member_id, player in enumerate(players):
            for round_num in rounds:
                pd = player.within.strict(app=__name__, round=round_num)

                rows.append(
                    {
                        "session": session.name,
                        "group": group.name,
                        "round": round_num,
                        "uname": player.name,
                        "member_id": member_id,
                        "effort": pd.get("effort"),
                        "own_capital": pd.get("own_capital"),
                        "wage": pd.get("wage"),
                        "rental_rate": pd.get("rental_rate"),
                        "aggregate_capital": pd.get("aggregate_capital"),
                        "aggregate_labor": pd.get("aggregate_labor"),
                        "output": pd.get("output"),
                        "labor_income": pd.get("labor_income"),
                        "capital_return": pd.get("capital_return"),
                        "transfer": pd.get("transfer"),
                        "resources": pd.get("resources"),
                        "consumption": pd.get("consumption"),
                        "next_capital": pd.get("next_capital"),
                        "redemption_value": pd.get("redemption_value"),
                        "payoff": pd.get("payoff"),
                        "tau_l": settings["tau_l"],
                        "tau_k": settings["tau_k"],
                        "beta": settings["beta"],
                    }
                )

    return rows


page_order = [
    GroupPlease,
    Instructions,
    Repeat(
        LaborTask,
        SyncLabor,
        ConsumptionChoice,
        SyncRound,
        RoundResults,
    ),
]
