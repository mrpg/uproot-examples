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

DESCRIPTION = "Survey with follow-up verification"
LANDING_PAGE = False


class C:
    pass


class Survey(Page):
    fields = dict(
        age=IntegerField(
            label="What is your current age in years?",
            description="Full years only, please.",
            min=0,
            max=120,
        ),
        econ=RadioField(
            label="Have you ever taken a class in economics at the university level?",
            choices=[(True, "Yes"), (False, "No")],
        ),
        sport=RadioField(
            label="What is your favorite sport?",
            description="This field is optional.",
            choices=[
                "Soccer",
                "American football",
                "Baseball",
                "Basketball",
            ],
            optional=True,
        ),
    )


class Verification(Page):
    allow_back = True


page_order = [
    Survey,
    Verification,
]
