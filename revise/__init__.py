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

DESCRIPTION = "Revise decisions across rounds"


class C:
    ROUNDS = 3


class Decision(Page):
    @classmethod
    def fields(page, player):
        return dict(
            number=IntegerField(
                label="Please enter a number.",
            ),
        )

    @classmethod
    def templatevars(page, player):
        return dict(actual_round=player.round)


class Revise(Decision):
    template = f"{__name__}/Decision.html"

    @classmethod
    def templatevars(page, player):
        return dict(actual_round=player.revise_round)

    @classmethod
    def show(page, player):
        return player.get("revise_round")

    @classmethod
    def fields(page, player):
        # Show the old answer as the starting value when a player revises a round.
        current = player.within(app=__name__, round=player.revise_round).get("number")

        return dict(
            number=IntegerField(label="Please enter a number.", default=current),
        )

    @classmethod
    def before_form_save(page, player, data):
        # This page is shown after all normal rounds are over. Before uproot saves
        # the form, we set player.round to the chosen old round so the new answer
        # is stored as a replacement for that round.
        player.round = player.revise_round


class Review(Page):
    @classmethod
    def templatevars(page, player):
        # Most history tables in these examples loop over the raw round history.
        # Here a revised round has more than one history entry, so loop over the
        # known round numbers instead. within(...) gives the current answer for
        # each round, including any later revision.
        round_data = list()

        for round_num in range(1, C.ROUNDS + 1):
            number = player.within(app=__name__, round=round_num).get("number")

            if number is not None:
                round_data.append((round_num, number))

        return dict(round_data=round_data)

    @live
    def revise(page, player, round_num: int):
        if not 1 <= round_num <= C.ROUNDS:
            return

        # The Revise page sits just before Review in page_order. Moving back one
        # page sends the player to that form, then reload() makes the browser show
        # it right away.
        player.revise_round = round_num
        player.show_page -= 1
        reload(player)


page_order = [
    Rounds(
        Decision,
        n=C.ROUNDS,
    ),
    Revise,
    Review,
]
