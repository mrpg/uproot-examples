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

DESCRIPTION = "Stackelberg quantity competition (sequential)"
SUGGESTED_MULTIPLE = 2


class C:
    MAX_UNITS = 100
    # Demand: P = 100 - Q_total, zero costs
    # First mover chooses quantity, then second mover observes and responds


class Context(PlayerContext):
    @property
    def leader_units(self) -> Any:
        return self.player.group.players.find_one(first_mover=True).units

    @property
    def follower_units(self) -> Any:
        return self.player.group.players.find_one(first_mover=False).units

    @property
    def total_units(self) -> Any:
        return self.leader_units + self.follower_units

    @property
    def price(self) -> Any:
        return max(0, 100 - self.total_units)


class GroupPlease(GroupCreatingWait):
    group_size = 2

    @classmethod
    def after_grouping(page, group: GroupType) -> None:
        for player, is_first in zip(group.players, [True, False]):
            player.first_mover = is_first


class Instructions(Page):
    pass


class LeaderDecision(Page):
    fields = dict(
        units=IntegerField(
            label="How many units do you produce?",
            addon_end="units",
            min=0,
            max=C.MAX_UNITS,
            render_kw={"style": "flex: unset !important; width: 6rem !important;"},
        ),
    )

    @classmethod
    def show(page, player: PlayerType) -> bool:
        return bool(player.first_mover)


class WaitForLeader(SynchronizingWait):
    pass


class FollowerDecision(Page):
    @classmethod
    def show(page, player: PlayerType) -> bool:
        return not player.first_mover

    @classmethod
    def fields(page, player: PlayerType) -> dict[str, Field]:
        leader = player.group.players.find_one(first_mover=True)
        return dict(
            units=IntegerField(
                label=f"The first mover produced {leader.units} units. How many units do you produce?",
                addon_end="units",
                min=0,
                max=C.MAX_UNITS,
                render_kw={"style": "flex: unset !important; width: 6rem !important;"},
            ),
        )


class Sync(SynchronizingWait):
    @classmethod
    def all_here(page, group: GroupType) -> None:
        leader = group.players.find_one(first_mover=True)
        follower = group.players.find_one(first_mover=False)
        total = leader.units + follower.units
        price = max(0, 100 - total)
        leader.payoff = price * leader.units
        follower.payoff = price * follower.units


class Results(Page):
    pass


def pipeline(session: SessionType) -> list[dict[str, Any]]:
    rows = []

    for group in session.groups(app=__name__):
        players = group.players
        player_rows = [(player, player.within(app=__name__)) for player in players]
        leader, leader_data = next(
            (player, data) for player, data in player_rows if data.get("first_mover")
        )
        follower, follower_data = next(
            (player, data)
            for player, data in player_rows
            if not data.get("first_mover")
        )
        leader_units = leader_data.get("units")
        follower_units = follower_data.get("units")

        if leader_units is None or follower_units is None:
            total_units = None
            price = None
        else:
            total_units = leader_units + follower_units
            price = max(0, 100 - total_units)

        for player, player_data in player_rows:
            rows.append(
                {
                    "session": session.name,
                    "group": group.name,
                    "uname": player.name,
                    "role": (
                        "leader" if player_data.get("first_mover") else "follower"
                    ),
                    "leader_uname": leader.name,
                    "follower_uname": follower.name,
                    "leader_units": leader_units,
                    "follower_units": follower_units,
                    "total_units": total_units,
                    "price": price,
                    "payoff": player_data.get("payoff"),
                }
            )

    return rows


page_order = [
    GroupPlease,
    Instructions,
    LeaderDecision,
    WaitForLeader,
    FollowerDecision,
    Sync,
    Results,
]
