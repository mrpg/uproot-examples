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

DESCRIPTION = "Multiple price list"


class MultiplePriceList(Page):
    context = {
        "options_a": [
            "$0 today",
            "$10 today",
            "$20 today",
            "$30 today",
            "$40 today",
        ],
        "options_b": [
            "$40 tomorrow",
            "$40 tomorrow",
            "$40 tomorrow",
            "$40 tomorrow",
            "$40 tomorrow",
        ],
    }
    fields = {f"choseA{i}": RadioField() for i in range(5)}


page_order = [
    MultiplePriceList,
]
