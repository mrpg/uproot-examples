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

DESCRIPTION = "Gift exchange game (Fehr et al., 1993)"


class C:
    MIN_WAGE = cu("1")
    MAX_WAGE = cu("10")
    MIN_EFFORT = cu("0.1")
    MAX_EFFORT = cu("1")
    EFFORT_COST_MULTIPLIER = cu("5")  # Cost = multiplier * effort


class Context(PlayerContext):
    @property
    def wage(self):
        return self.player.group.players.find_one(employer=True).wage

    @property
    def effort(self):
        return self.player.group.players.find_one(employer=False).effort

    @property
    def effort_cost(self):
        return (
            C.EFFORT_COST_MULTIPLIER
            * self.player.group.players.find_one(employer=False).effort
        )


class GroupPlease(GroupCreatingWait):
    group_size = 2

    @classmethod
    def after_grouping(page, group):
        for player, is_employer in zip(group.players, [True, False]):
            player.employer = is_employer


class SetWage(Page):
    fields = dict(
        wage=DecimalField(
            label="What wage do you offer?",
            min=C.MIN_WAGE,
            max=C.MAX_WAGE,
        ),
    )

    @classmethod
    def show(page, player):
        return player.employer


class WaitForWage(SynchronizingWait):
    pass


class ChooseEffort(Page):
    fields = dict(
        effort=DecimalField(
            label="What effort level do you choose?",
            min=C.MIN_EFFORT,
            max=C.MAX_EFFORT,
            step=cu("0.1"),
        ),
    )

    @classmethod
    def show(page, player):
        return not player.employer


class Sync(SynchronizingWait):
    @classmethod
    def all_here(page, group):
        employer = group.players.find_one(employer=True)
        worker = group.players.find_one(employer=False)

        effort_cost = C.EFFORT_COST_MULTIPLIER * worker.effort

        # Employer payoff: effort * 10 - wage
        employer.payoff = worker.effort * 10 - employer.wage

        # Worker payoff: wage - cost(effort)
        worker.payoff = employer.wage - effort_cost


class Results(Page):
    pass


page_order = [
    GroupPlease,
    SetWage,
    WaitForWage,
    ChooseEffort,
    Sync,
    Results,
]
