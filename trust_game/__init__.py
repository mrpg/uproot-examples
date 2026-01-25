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

DESCRIPTION = "Trust game (Berg et al., 1995)"

ENDOWMENT = cu("10")
MULTIPLIER = 3


class GroupPlease(GroupCreatingWait):
    group_size = 2

    @classmethod
    def after_grouping(page, group):
        for player, is_trustor in zip(players(group), [True, False]):
            player.trustor = is_trustor


class Send(Page):
    fields = dict(
        sent=DecimalField(
            label="How much do you send to the other player?",
            min=0,
            max=ENDOWMENT,
        ),
    )

    @classmethod
    def show(page, player):
        return player.trustor

    @classmethod
    def context(page, player):
        return dict(endowment=ENDOWMENT, multiplier=MULTIPLIER)


class WaitForSend(SynchronizingWait):
    pass


class Return(Page):
    @classmethod
    def show(page, player):
        return not player.trustor

    @classmethod
    def context(page, player):
        trustor = players(player.group).find_one(trustor=True)
        received = trustor.sent * MULTIPLIER
        return dict(received=received, endowment=ENDOWMENT)

    @classmethod
    def fields(page, player):
        trustor = players(player.group).find_one(trustor=True)
        received = trustor.sent * MULTIPLIER
        return dict(
            returned=DecimalField(
                label="How much do you return to the other player?",
                min=0,
                max=received,
            ),
        )


class Sync(SynchronizingWait):
    @classmethod
    def all_here(page, group):
        trustor = players(group).find_one(trustor=True)
        trustee = players(group).find_one(trustor=False)

        received = trustor.sent * MULTIPLIER

        trustor.payoff = ENDOWMENT - trustor.sent + trustee.returned
        trustee.payoff = ENDOWMENT + received - trustee.returned


class Results(Page):
    @classmethod
    def context(page, player):
        trustor = players(player.group).find_one(trustor=True)
        trustee = players(player.group).find_one(trustor=False)
        return dict(
            sent=trustor.sent,
            tripled=trustor.sent * MULTIPLIER,
            returned=trustee.returned,
        )


page_order = [
    GroupPlease,
    Send,
    WaitForSend,
    Return,
    Sync,
    Results,
]
