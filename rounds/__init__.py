from uproot.fields import *
from uproot.smithereens import *


class EnterData(Page):
    fields = dict(
        number=IntegerField(label="Please enter a number."),
    )


page_order = [
    Rounds(EnterData, n=4),  # repeat EnterData four times
]
