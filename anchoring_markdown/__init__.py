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
from statistics import median

from uproot.fields import *
from uproot.smithereens import *

DESCRIPTION = "Anchoring effect (Tversky & Kahneman, 1974), implemented in Markdown"
LANDING_PAGE = False


class C:
    TREATMENTS = ["SHORT", "LONG"]
    ANCHORS = {"SHORT": 1, "LONG": 1000}


class AssignTreatment(NoshowPage):
    @classmethod
    def after_always_once(page, player):
        counts = Counter(
            player.session.players.apply(
                lambda p: p.get("treatment"),
            ),
        )
        player.treatment = min(
            C.TREATMENTS,
            key=lambda x: counts.get(x, 0),
        )


class Estimate(Page):
    @classmethod
    def fields(page, player):
        anchor = fmtnum(C.ANCHORS[player.treatment], post="\xa0km", places=0)

        return {
            "comparison": RadioField(
                label=f"Do you think the answer is more or less than {anchor}?",
                choices=[
                    ("less", f"Less than {anchor}"),
                    ("more", f"More than {anchor}"),
                ],
                class_wrapper="mb-5",
            ),
            "estimate": DecimalField(
                label="Your estimate:",
                min=0,
                addon_end="km",
                class_wrapper="short-field",
            ),
        }


class Results(Page):
    pass


def digest(session):
    data = []
    estimates_by_treatment = {treatment: [] for treatment in C.TREATMENTS}

    for player in session.players:
        d = player.within(app=__name__)
        treatment = d.get("treatment")
        comparison = d.get("comparison")
        estimate = d.get("estimate")

        if treatment is not None:
            data.append(
                (
                    player.name,
                    treatment,
                    C.ANCHORS.get(treatment),
                    comparison,
                    estimate,
                )
            )
            if estimate is not None:
                estimates_by_treatment[treatment].append(estimate)

    medians = [
        (
            treatment,
            C.ANCHORS[treatment],
            median(estimates),
            len(estimates),
        )
        for treatment, estimates in estimates_by_treatment.items()
        if estimates
    ]

    return {"data": data, "medians": medians}


def pipeline(session):
    rows = []

    for player in session.players:
        d = player.within(app=__name__)
        treatment = d.get("treatment")
        comparison = d.get("comparison")
        estimate = d.get("estimate")

        if treatment is not None:
            rows.append(
                {
                    "session": session.name,
                    "uname": player.name,
                    "treatment": treatment,
                    "anchor": C.ANCHORS.get(treatment),
                    "comparison": comparison,
                    "estimate": estimate,
                }
            )

    return rows


page_order = [
    AssignTreatment,
    Estimate,
    Results,
]
