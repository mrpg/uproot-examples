"""
Docs are available at https://uproot.science/
Examples are available at https://github.com/mrpg/uproot-examples

This example app is under the 0BSD license. You can use it freely and build on it
without any limitations and without any attribution. However, these two lines must be
preserved in any uproot app (the license file is automatically installed in a project):

Third-party dependencies:
- uproot: LGPL v3+, see ../uproot_license.txt
"""

from uproot.fields import *
from uproot.smithereens import *

DESCRIPTION = "Simple round game with history table"


class NewRound(Page):
    pass


class EnterData(Page):
    fields = dict(
        number=IntegerField(label="Please enter a number."),
    )


class Results(Page):
    pass


page_order = [
    Rounds(NewRound, EnterData, n=4),  # repeat NewRound and EnterData four times
    Results,  # show Results only at the end
]
