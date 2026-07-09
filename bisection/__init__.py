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

DESCRIPTION = "Certainty-equivalent elicitation over mean-preserving spreads"
LANDING_PAGE = False


class C:
    MEAN = 50
    LOTTERIES = [
        (47, 53),
        (40, 60),
        (25, 75),
        (0, 100),
    ]
    BISECTION_STEPS = 5
    TOTAL_ROUNDS = len(LOTTERIES) * BISECTION_STEPS


def bisection_state(player, lottery_index, up_to_step):
    low, high = C.LOTTERIES[lottery_index]
    first_round = lottery_index * C.BISECTION_STEPS + 1

    for s in range(up_to_step):
        mid = (low + high) / 2
        chose_certain = player.within(app=__name__, round=first_round + s).get(
            "prefer_certain"
        )

        if chose_certain is None:
            break

        if chose_certain:
            high = mid
        else:
            low = mid

    return low, high


def certainty_equivalent(player: PlayerType, lottery_index: int) -> float:
    low, high = bisection_state(player, lottery_index, C.BISECTION_STEPS)

    return (low + high) / 2


# PAGES


class Instructions(Page):
    pass


class Choice(Page):
    @classmethod
    def before_once(page, player: PlayerType) -> None:
        lottery_index = (player.round - 1) // C.BISECTION_STEPS
        step = (player.round - 1) % C.BISECTION_STEPS
        low, high = bisection_state(player, lottery_index, step)

        player.lottery_index = lottery_index
        player.lottery_low = C.LOTTERIES[lottery_index][0]
        player.lottery_high = C.LOTTERIES[lottery_index][1]
        player.offer = round((low + high) / 2, 2)
        player.step = step

    @classmethod
    def fields(page, player: PlayerType) -> dict[str, Field]:
        offer = player.offer
        lo = player.lottery_low
        hi = player.lottery_high

        return dict(
            prefer_certain=RadioField(
                label="Which do you prefer?",
                choices=[
                    (True, f"€{offer:.2f} for certain"),
                    (False, f"A 50–50 chance of €{lo} or €{hi}"),
                ],
            ),
        )

    @classmethod
    def templatevars(page, player: PlayerType) -> dict[str, Any]:
        return dict(
            lottery_num=player.lottery_index + 1,
            step_num=player.step + 1,
            total_lotteries=len(C.LOTTERIES),
            total_steps=C.BISECTION_STEPS,
            total_decisions=C.TOTAL_ROUNDS,
        )


class Results(Page):
    @classmethod
    def templatevars(page, player: PlayerType) -> dict[str, Any]:
        premiums_exact = [0.0]
        results = [
            dict(
                lottery_num=0,
                low=C.MEAN,
                high=C.MEAN,
                spread=0,
                ce=float(C.MEAN),
                risk_premium=0.0,
            ),
        ]

        for i, (lo, hi) in enumerate(C.LOTTERIES):
            ce = certainty_equivalent(player, i)
            pi = C.MEAN - ce
            premiums_exact.append(pi)

            results.append(
                dict(
                    lottery_num=i + 1,
                    low=lo,
                    high=hi,
                    spread=hi - lo,
                    ce=round(ce, 2),
                    risk_premium=round(pi, 2),
                )
            )

        all_nonneg = all(p >= 0 for p in premiums_exact)
        weakly_increasing = all(
            premiums_exact[i] <= premiums_exact[i + 1]
            for i in range(len(premiums_exact) - 1)
        )

        return dict(
            results=results,
            consistent=all_nonneg and weakly_increasing,
        )


def pipeline(session: SessionType) -> list[dict[str, Any]]:
    rows = []

    for player in session.players:
        for i, (lo, hi) in enumerate(C.LOTTERIES):
            last_round = (i + 1) * C.BISECTION_STEPS

            if (
                player.within(app=__name__, round=last_round).get("prefer_certain")
                is None
            ):
                continue

            ce = certainty_equivalent(player, i)
            first_round = i * C.BISECTION_STEPS + 1
            choices = {}

            for s in range(C.BISECTION_STEPS):
                rd = player.within(app=__name__, round=first_round + s)
                choices[f"step_{s + 1}_certain"] = rd.get("prefer_certain")

            rows.append(
                {
                    "session": session.name,
                    "uname": player.name,
                    "lottery": i + 1,
                    "low_outcome": lo,
                    "high_outcome": hi,
                    "ce": round(ce, 2),
                    "risk_premium": round(C.MEAN - ce, 2),
                    **choices,
                }
            )

    return rows


def digest(session: SessionType) -> dict[str, Any]:
    data = []

    for player in session.players:
        if player.within(app=__name__, round=1).get("prefer_certain") is None:
            continue

        player_data = dict(name=player.name, results=[])

        for i, (lo, hi) in enumerate(C.LOTTERIES):
            last_round = (i + 1) * C.BISECTION_STEPS

            if (
                player.within(app=__name__, round=last_round).get("prefer_certain")
                is None
            ):
                player_data["results"].append(
                    dict(
                        lottery=f"L{i + 1}",
                        outcomes=f"{lo}–{hi}",
                        ce=None,
                        risk_premium=None,
                    )
                )
                continue

            ce = certainty_equivalent(player, i)

            player_data["results"].append(
                dict(
                    lottery=f"L{i + 1}",
                    outcomes=f"{lo}–{hi}",
                    ce=round(ce, 2),
                    risk_premium=round(C.MEAN - ce, 2),
                )
            )

        data.append(player_data)

    return data


page_order = [
    Instructions,
    Rounds(Choice, n=C.TOTAL_ROUNDS),
    Results,
]
