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

DESCRIPTION = "Ultimatum game"


class GroupPlease(GroupCreatingWait):
    group_size = 2

    @classmethod
    def after_grouping(page, group):
        for player, is_proposer in zip(players(group), [True, False]):
            player.proposer = is_proposer


class Propose(Page):
    fields = dict(
        offer=DecimalField(
            label="How much do you offer to the other player?",
            min=0,
            max=10,
        ),
    )

    @classmethod
    def show(page, player):
        return player.proposer


class WaitForProposal(SynchronizingWait):
    pass


class Respond(Page):
    fields = dict(
        accept=RadioField(
            label="Do you accept the offer?",
            choices=[(True, "Yes"), (False, "No")],
        ),
    )

    @classmethod
    def show(page, player):
        return not player.proposer

    @classmethod
    def context(page, player):
        proposer = players(player.group).find_one(proposer=True)
        return dict(offer=proposer.offer)


class Sync(SynchronizingWait):
    @classmethod
    def all_here(page, group):
        proposer = players(group).find_one(proposer=True)
        responder = players(group).find_one(proposer=False)

        if responder.accept:
            proposer.payoff = cu(10) - proposer.offer
            responder.payoff = proposer.offer
        else:
            proposer.payoff = cu(0)
            responder.payoff = cu(0)


class Results(Page):
    @classmethod
    def context(page, player):
        proposer = players(player.group).find_one(proposer=True)
        responder = players(player.group).find_one(proposer=False)
        return dict(
            offer=proposer.offer,
            accepted=responder.accept,
        )


page_order = [
    GroupPlease,
    Propose,
    WaitForProposal,
    Respond,
    Sync,
    Results,
]
