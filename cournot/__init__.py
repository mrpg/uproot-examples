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
SUGGESTED_MULTIPLE = 2


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


def pipeline(session):
    rows = []

    for group in session.groups(app=__name__):
        players = group.players
        units = [player.within(app=__name__).get("units") for player in players]
        total_units = sum(units) if all(unit is not None for unit in units) else None
        price = max(0, 100 - total_units) if total_units is not None else None

        for member_id, player in enumerate(players):
            other = players[1 - member_id]
            player_data = player.within(app=__name__)
            other_data = other.within(app=__name__)

            rows.append(
                {
                    "session": session.name,
                    "group": group.name,
                    "uname": player.name,
                    "member_id": member_id,
                    "units": player_data.get("units"),
                    "other_uname": other.name,
                    "other_units": other_data.get("units"),
                    "total_units": total_units,
                    "price": price,
                    "payoff": player_data.get("payoff"),
                }
            )

    return rows


page_order = [
    GroupPlease,
    Instructions,
    Decision,
    Sync,
    Results,
]
