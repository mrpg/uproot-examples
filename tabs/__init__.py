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

DESCRIPTION = (
    "Tab navigation for Pages — subjects can go back and forth between sections"
)


class Tabs(Page):
    fields = dict(
        age=IntegerField(
            label="Please enter your age.",
            min=18,
            max=120,
        ),
    )


page_order = [
    Tabs,
]
