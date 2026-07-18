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

DESCRIPTION = "Mind game (Jiang, 2013; Kajackaite & Gneezy, 2017)"
LANDING_PAGE = False


class C:
    BONUS = cu(100)


class Instructions(Page):
    pass


class Think(Page):
    pass


class Roll(Page):
    fields = dict(
        reported_diceroll=RadioField(
            label="Which number did the die show?",
            choices=[(i, str(i)) for i in range(1, 7)],
            layout="horizontal",
        ),
        correct_guess=RadioField(
            label="Was this the number you had in mind?",
            choices=[(True, "Yes"), (False, "No")],
            layout="horizontal",
        ),
    )

    @classmethod
    def after_once(page, player: PlayerType) -> None:
        if player.correct_guess == 1:
            player.payoff = C.BONUS


class Results(Page):
    pass


def digest(session: SessionType) -> dict[str, Any]:
    n_total = 0
    n_correct = 0

    for player in session.players:
        data = player.within(app=__name__)
        guess = data.get("correct_guess")

        if guess is not None:
            n_total += 1
            if guess == 1:
                n_correct += 1

    rate = n_correct / n_total if n_total else 0.0

    return {
        "n_total": n_total,
        "n_correct": n_correct,
        "rate": rate,
    }


def pipeline(session: SessionType) -> list[dict[str, Any]]:
    rows = []

    for player in session.players:
        data = player.within(app=__name__)
        guess = data.get("correct_guess")

        if guess is not None:
            rows.append(
                {
                    "session": session.name,
                    "uname": player.name,
                    "reported_diceroll": data.get("reported_diceroll"),
                    "correct_guess": guess,
                    "payoff": data.get("payoff"),
                }
            )

    return rows


page_order = [
    Instructions,
    Think,
    Roll,
    Results,
]
