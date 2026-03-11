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

DESCRIPTION = "Cournot quantity competition"


class C:
    MAX_UNITS = 100
    # Demand: P = 100 - Q_total, zero costs


class Context(PlayerContext):
    @property
    def other_units(self):
        return self.player.other_in_group.units

    @property
    def total_units(self):
        return self.player.units + self.other_units

    @property
    def price(self):
        return max(0, 100 - self.total_units)


class GroupPlease(GroupCreatingWait):
    group_size = 2


class Instructions(Page):
    pass


class Decision(Page):
    fields = dict(
        units=IntegerField(
            label="How many units do you produce?",
            addon_end="units",
            min=0,
            max=C.MAX_UNITS,
            render_kw={"style": "flex: unset !important; width: 6rem !important;"},
        ),
    )


class Sync(SynchronizingWait):
    @classmethod
    def all_here(page, group):
        p1, p2 = group.players
        total = p1.units + p2.units
        price = max(0, 100 - total)
        p1.payoff = price * p1.units
        p2.payoff = price * p2.units


class Results(Page):
    pass


page_order = [
    GroupPlease,
    Instructions,
    Decision,
    Sync,
    Results,
]
