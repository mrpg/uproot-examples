# Docs are available at https://uproot.science/
# Examples are available at https://github.com/mrpg/uproot-examples
#
# This example app is under the 0BSD license. You can use it freely and build on it
# without any limitations and without any attribution. However, these two lines must be
# preserved in any uproot app (the license file is automatically installed in projects):
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt

import random

from uproot.fields import *
from uproot.smithereens import *

DESCRIPTION = "Simple treatment assignment"
LANDING_PAGE = False
TREATMENTS = [1, 2]  # These can have any supported type and there may be more than 2


def new_player(player):
    player.treatment = random.choice(TREATMENTS)


class C:
    pass


class Info(Page):
    pass


page_order = [
    Info,
]
