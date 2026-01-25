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

LABELS = dict(
    age="What is your current age in years?",
    econ="Have you ever taken a class in economics at the university level?",
    sport="What is your favorite sport?",
)


class C:
    pass


class Survey(Page):
    @classmethod
    async def fields(page, player):
        return dict(
            age=IntegerField(
                label=LABELS["age"],
                description="Full years only, please.",
                default=player.get("age"),
                min=0,
                max=120,
            ),
            econ=RadioField(
                label=LABELS["econ"],
                choices=[(True, "Yes"), (False, "No")],
                default=player.get("econ"),
            ),
            sport=RadioField(
                label=LABELS["sport"],
                description="This field is optional.",
                choices=[
                    "Soccer",
                    "American football",
                    "Baseball",
                    "Basketball",
                ],
                default=player.get("sport"),
                optional=True,
            ),
        )


class Verification(Page):
    allow_back = True


page_order = [
    Survey,
    Verification,
]
