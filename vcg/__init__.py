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

DESCRIPTION = "Public good provision via the Vickrey–Clarke–Groves mechanism"
SUGGESTED_MULTIPLE = 3


class C:
    GROUP_SIZE = 3
    COST = cu("150")
    MAX_VALUE = 100


class Context(PlayerContext):
    @property
    def members(self):
        return self.player.group.players

    @property
    def group_total_reported(self):
        return sum(p.reported_value for p in self.player.group.players)

    @property
    def total_payments(self):
        return sum(p.payment for p in self.player.group.players)

    @property
    def deficit(self):
        if self.player.provided:
            return C.COST - sum(p.payment for p in self.player.group.players)

        return cu(0)


class GroupPlease(GroupCreatingWait):
    group_size = C.GROUP_SIZE

    @classmethod
    def after_grouping(page, group):
        for player in group.players:
            player.true_value = cu(rng().randint(0, C.MAX_VALUE))


class Introduction(Page):
    pass


class Report(Page):
    fields = dict(
        reported_value=DecimalField(
            label="Your reported value for the project:",
            addon_start="$",
            min=0,
            max=C.MAX_VALUE,
            places=2,
        ),
    )


class Sync(SynchronizingWait):
    @classmethod
    def all_here(page, group):
        players = group.players
        total_reported = sum(p.reported_value for p in players)
        provided = total_reported >= C.COST

        for player in players:
            others_total = sum(p.reported_value for p in players if p is not player)
            would_provide_without = others_total >= C.COST
            pivotal = provided and not would_provide_without

            if pivotal:
                payment = C.COST - others_total
            else:
                payment = cu(0)

            player.provided = provided
            player.pivotal = pivotal
            player.payment = payment
            player.others_total = others_total

            if provided:
                player.payoff = player.true_value - payment
            else:
                player.payoff = cu(0)


class Results(Page):
    pass


def pipeline(session):
    rows = []

    for group in session.groups(app=__name__):
        players = group.players

        for member_id, player in enumerate(players):
            player_data = player.within(app=__name__)

            rows.append(
                {
                    "session": session.name,
                    "group": group.name,
                    "uname": player.name,
                    "member_id": member_id,
                    "true_value": player_data.get("true_value"),
                    "reported_value": player_data.get("reported_value"),
                    "provided": player_data.get("provided"),
                    "pivotal": player_data.get("pivotal"),
                    "payment": player_data.get("payment"),
                    "others_total": player_data.get("others_total"),
                    "payoff": player_data.get("payoff"),
                }
            )

    return rows


page_order = [
    GroupPlease,
    Introduction,
    Report,
    Sync,
    Results,
]
