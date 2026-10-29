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

DESCRIPTION = "Prisoner's dilemma with continuous chat"
SUGGESTED_MULTIPLE = 2


class C:
    PAYOFF_MATRIX = {
        # (you cooperate, other cooperates): your payoff
        (True, True): 10,
        (True, False): 0,
        (False, True): 15,
        (False, False): 3,
    }


class Instructions(Page):
    pass


class GroupPlease(GroupCreatingWait):
    group_size = 2

    @classmethod
    def after_grouping(page, group: GroupType) -> None:
        group.chat = chat.create(group.session)

        for i, p in enumerate(group.players, 1):
            chat.add_player(group.chat, p, pseudonym=f"Player {i}")


class Dilemma(Page):
    fields = dict(
        cooperate=RadioField(
            label="Do you wish to cooperate?",
            choices=[(True, "Yes"), (False, "No")],
        ),
    )


class Sync(SynchronizingWait):
    @classmethod
    def all_here(page, group: GroupType) -> None:
        for player in group.players:
            player.payoff = C.PAYOFF_MATRIX[
                player.cooperate,
                player.other_in_group.cooperate,
            ]


class Results(Page):
    pass


page_order = [
    Instructions,
    GroupPlease,
    Dilemma,
    Sync,
    Results,
]
