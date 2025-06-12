from uproot.fields import *
from uproot.smithereens import *


class GroupPlease(GroupCreatingWait):
    group_size = 2


class Dilemma(Page):
    fields = dict(
        cooperate=BooleanField(label="Do you wish to cooperate?"),
    )


class Sync(SynchronizingWait):
    @classmethod
    def set_payoff(page, player):
        other = other_in_group(player)

        match player.cooperate, other.cooperate:
            case True, True:
                player.payoff = 10
            case True, False:
                player.payoff = 0
            case False, True:
                player.payoff = 15
            case False, False:
                player.payoff = 3

    @classmethod
    def all_here(page, group):
        players(group).apply(page.set_payoff)


class Results(Page):
    @classmethod
    def context(page, player):
        return dict(
            other=other_in_group(player),
        )


page_order = [
    GroupPlease,
    Dilemma,
    Sync,
    Results,
]
