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

DESCRIPTION = "Enter Student ID"
LANDING_PAGE = False


class C:
    pass


class EnterID(Page):
    fields = dict(
        student_id=StringField(label="Enter your Student ID:"),
        student_id2=StringField(label="Enter your Student ID again:"),
    )

    @classmethod
    def validate(page, player, data):
        if data["student_id"] != data["student_id2"]:
            return "Student IDs don’t match."


class Verification(Page):
    allow_back = True


page_order = [
    EnterID,
    Verification,
]
