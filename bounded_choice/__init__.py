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

DESCRIPTION = "BoundedChoiceField examples"
LANDING_PAGE = False


class C:
    pass


class Fields(Page):
    fields = dict(
        color=BoundedChoiceField(
            label="Select at most one color.",
            choices=[
                "Red",
                "Blue",
                "Green",
            ],
            min=0,
            max=1,
        ),
        fruit=BoundedChoiceField(
            label="Select exactly one fruit.",
            choices=[
                "Apple",
                "Banana",
                "Citron",
            ],
            min=1,
            max=1,
        ),
        winners=BoundedChoiceField(
            label="Select exactly three winners.",
            choices=[1, 2, 3, 4, 5, 6],
            min=3,
            max=3,
        ),
        hobbies=BoundedChoiceField(
            label="Select up to two hobbies.",
            choices={
                "A": "Art",
                "B": "Books",
            },
            min=0,
            max=2,
        ),
        toppings=BoundedChoiceField(
            label="Select at least one pizza topping.",
            choices=["Cheese", "Pepperoni", "Mushrooms"],
            min=1,
        ),
    )


class Results(Page):
    pass


page_order = [
    Fields,
    Results,
]
