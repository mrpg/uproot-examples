from uproot.fields import *
from uproot.smithereens import *


def new_player(player):
    player.payoff = 0  # initialize this field on player entry


class GroupPlease(GroupCreatingWait):
    group_size = 2


class Claim(Page):
    fields = dict(
        claim=DecimalField(label="How much do you claim?"),
    )


class Sync(SynchronizingWait):
    @classmethod
    def set_payoff(page, player):
        other = other_in_group(player)

        if player.claim + other.claim <= 100:
            player.payoff = player.claim

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
    Claim,
    Sync,
    Results,
]
