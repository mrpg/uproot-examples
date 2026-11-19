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
from itertools import permutations

from uproot.fields import *
from uproot.smithereens import *

DESCRIPTION = "Balanced page order randomization"


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
    def templatevars(page, player: PlayerType) -> dict[str, Any]:
        ordering = ORDERINGS[player.perm_index]
        return {
            "page_names": [p.__name__ for p in ordering],
            "num_orderings": len(ORDERINGS),
        }


def page_order(player: PlayerType) -> list[Any]:
    if player.get("perm_index") is None:
        # To count only some players, add conditions to the `if` below (see README.md).
        assigned = [
            p.get("perm_index")
            for p in player.session.players
            if p.get("perm_index") is not None
        ]
        counts = Counter(assigned)
        n = len(assigned) + 1
        total_weight = sum(WEIGHTS)

        # Assign to the most underrepresented ordering (largest deficit from target).
        # Ties go to the first such ordering (see README.md).
        player.perm_index = max(
            range(len(ORDERINGS)),
            key=lambda i: WEIGHTS[i] / total_weight * n - counts.get(i, 0),
        )

    return [Start, *ORDERINGS[player.perm_index], End]
