# Docs are available at https://uproot.science/
# Examples are available at https://github.com/mrpg/uproot-examples
#
# This example app is under the 0BSD license. You can use it freely and build on it
# without any limitations and without any attribution. However, these two lines must be
# preserved in any uproot app (the license file is automatically installed in projects):
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt

from collections import Counter

from uproot.fields import *
from uproot.smithereens import *

DESCRIPTION = "Die-roll honesty task (Fischbacher & Föllmi-Heusi, 2013)"
LANDING_PAGE = False


class C:
    # Reporting a 6 pays nothing, all other numbers pay their face value
    PAYOFFS = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 0}


class Roll(Page):
    fields = dict(
        report=RadioField(
            label="Which number did your first roll show?",
            choices=[(i, str(i)) for i in range(1, 7)],
            layout="horizontal",
        ),
    )

    @classmethod
    def after_once(page, player: PlayerType) -> None:
        player.payoff = cu(C.PAYOFFS[player.report])


class Results(Page):
    pass


def digest(session: SessionType) -> dict[str, Any]:
    counts: Counter[int] = Counter()

    for player in session.players:
        report = player.within(app=__name__).get("report")

        if report is not None:
            counts[report] += 1

    total = sum(counts.values())
    distribution = [
        (face, counts.get(face, 0), counts.get(face, 0) / total if total else 0.0)
        for face in range(1, 7)
    ]

    return {"distribution": distribution, "total": total}


def pipeline(session: SessionType) -> list[dict[str, Any]]:
    rows = []

    for player in session.players:
        player_data = player.within(app=__name__)
        report = player_data.get("report")

        if report is not None:
            rows.append(
                {
                    "session": session.name,
                    "uname": player.name,
                    "report": report,
                    "payoff": player_data.get("payoff"),
                }
            )

    return rows


page_order = [
    Roll,
    Results,
]
