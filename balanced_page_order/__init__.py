# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt

from collections import Counter
from itertools import permutations

from uproot.fields import *
from uproot.smithereens import *

DESCRIPTION = "Balanced page order randomization"

# See below (lines 31-34).


class Start(Page):
    pass


class Page1(Page):
    pass


class Page2(Page):
    pass


class Page3(Page):
    pass


# Adapt PAGES, ORDERINGS, and WEIGHTS to your experiment.
PAGES = [Page1, Page2, Page3]
ORDERINGS = list(permutations(PAGES))
WEIGHTS = [1] * len(ORDERINGS)  # Default: equal weights


class End(Page):
    @classmethod
    def templatevars(page, player):
        ordering = ORDERINGS[player.perm_index]
        return {
            "page_names": [p.__name__ for p in ordering],
            "num_orderings": len(ORDERINGS),
        }


def page_order(player):
    if player.get("perm_index") is None:
        assigned = [
            x
            for x in player.session.players.apply(lambda p: p.get("perm_index"))
            if x is not None
        ]
        counts = Counter(assigned)
        n = len(assigned) + 1
        total_weight = sum(WEIGHTS)

        # Assign to the most underrepresented ordering (largest deficit from target)
        player.perm_index = max(
            range(len(ORDERINGS)),
            key=lambda i: WEIGHTS[i] / total_weight * n - counts.get(i, 0),
        )

    return [Start, *ORDERINGS[player.perm_index], End]
