# SPDX-License-Identifier: 0BSD
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt
#
# Docs are available at https://uproot.science/
# Examples are available at https://github.com/mrpg/uproot-examples

from uproot.fields import *
from uproot.smithereens import *

from .euclidean_rerandomization import assign as assign_euclidean

DESCRIPTION = "Rerandomization/stratification on the fly"
LANDING_PAGE = False

LABELS = dict(
    age="What is your current age?",
    econ="Have you ever taken a class in economics at the university level?",
)


class C:
    TREATMENTS = ["A", "B"]


class Survey(Page):
    fields = dict(
        age=IntegerField(
            label=LABELS["age"],
            description="Full years only, please.",
            addon_end="years",
            class_wrapper="col-12 col-md-3",  # Scale down on desktop
            min=0,
            max=120,
        ),
        econ=RadioField(
            label=LABELS["econ"],
            choices=[(True, "Yes"), (False, "No")],
        ),
    )


class Wait(SynchronizingWait):
    synchronize = "session"

    @classmethod
    def all_here(page, session):
        players = list(session.players)
        n = len(players)

        covariates = [[float(p.age), 1.0 if p.econ else 0.0] for p in players]

        treatments = list(C.TREATMENTS)
        k = len(treatments)
        base = n // k
        remainder = n % k
        sizes = {
            t: base + (1 if i < remainder else 0) for i, t in enumerate(treatments)
        }
        sizes_nonzero = {t: s for t, s in sizes.items() if s > 0}

        try:
            assignments = assign_euclidean(
                covariates,
                sizes_nonzero,
                alpha=0.001,
                max_iterations=100000,
            )
            assignment_method = "euclidean"
        except Exception:
            pool = [t for t, s in sizes_nonzero.items() for _ in range(s)]
            rng().shuffle(pool)
            assignments = pool
            assignment_method = "shuffle"

        session.rerandomization_assignment_method = assignment_method

        for player, treatment in zip(players, assignments):
            player.treatment = treatment


class Results(Page):
    pass


def digest(session):
    by_treatment: dict[str, dict[str, list[float]]] = {
        t: {"ages": [], "econs": []} for t in C.TREATMENTS
    }

    for player in session.players:
        d = player.within(app=__name__)
        treatment = d.get("treatment")

        if treatment is None:
            continue

        age = d.get("age")
        econ = d.get("econ")

        if age is not None:
            by_treatment[treatment]["ages"].append(age)

        if econ is not None:
            by_treatment[treatment]["econs"].append(1 if econ else 0)

    summary = []
    for t in C.TREATMENTS:
        ages = by_treatment[t]["ages"]
        econs = by_treatment[t]["econs"]
        summary.append(
            (
                t,
                len(ages),
                sum(ages) / len(ages) if ages else None,
                sum(econs) / len(econs) if econs else None,
            )
        )

    return {
        "assignment_method": session.get("rerandomization_assignment_method"),
        "summary": summary,
    }


page_order = [
    Survey,
    Wait,
    Results,
]
