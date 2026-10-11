# Docs are available at https://uproot.science/
# Examples are available at https://github.com/mrpg/uproot-examples
#
# This example app is under the 0BSD license. You can use it freely and build on it
# without any limitations and without any attribution. However, these two lines must be
# preserved in any uproot app (the license file is automatically installed in projects):
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt

from uproot.fields import IntegerField
from uproot.smithereens import Page, PlayerType, Repeat, Rounds

DESCRIPTION = "Named round blocks, resumed counters, and nested rounds"
LANDING_PAGE = False


class Step(Page):
    template = "blocks/Step.html"
    fields = dict(number=IntegerField(label="Enter any number for this round."))


class RepeatStep(Step):
    @classmethod
    def before_once(page, player: PlayerType) -> None:
        # Red has already completed rounds 1 and 2. Repeat round 3 once more,
        # then stop after round 4.
        player.add_round = player.round == 3


class Summary(Page):
    pass


page_order = [
    Rounds(Step, n=2, block="red"),  # red rounds 1, 2
    Rounds(Step, n=1, block="blue"),  # blue round 1
    Repeat(RepeatStep, block="red"),  # red rounds 3, 4
    Rounds(
        Step,  # blue round 2 (outer)
        Rounds(Step, n=2),  # blue rounds 3, 4 (nested; inherits blue)
        n=1,
        block="blue",
    ),
    Summary,
]
