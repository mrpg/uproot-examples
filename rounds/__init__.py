from uproot.fields import *
from uproot.smithereens import *


class NewRound(Page):
    pass


class EnterData(Page):
    fields = dict(
        number=IntegerField(label="Please enter a number."),
    )


page_order = [
    Rounds(NewRound, EnterData, n=4),  # repeat NewRound and EnterData four times
]
