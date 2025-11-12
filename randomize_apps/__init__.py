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

DESCRIPTION = "This app randomizes app1, app2, app3."


import app1
import app2
import app3

page_order = [
    Random(
        Bracket(*app1.page_order),
        Bracket(*app2.page_order),
        Bracket(*app3.page_order),
    ),
]
