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

DESCRIPTION = "More balanced treatment assignment"
LANDING_PAGE = False
TREATMENTS = [1, 2]  # These can have any supported type and there may be more than 2


class C:
    pass


class AssignTreatment(NoshowPage):
    @classmethod
    def after_always_once(page, player):
        # Note: You can refine the group to which the count is applied by filtering.
        # For example, instead of players(player.session).apply(...), just do
        # players(player.session).filter(_.contribution > 10).apply(...), or
        # players(player.session).filter(_.dropout == False).apply(...). Needless to
        # say, these examples require the existence of `contribution` and `dropout`
        # fields, respectively. See the examples "dropouts" and "public_goods_game".

        counts = Counter(
            players(player.session).apply(
                lambda p: p.get("treatment"),
            ),
        )
        player.treatment = min(
            TREATMENTS,
            key=lambda x: counts.get(x, 0),
        )


class Info(Page):
    pass


page_order = [
    AssignTreatment,
    Info,
]
