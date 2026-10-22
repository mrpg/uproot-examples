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

DESCRIPTION = "A guided walkthrough of Bootstrap 6 and Bootstrap Icons for experiments"
LANDING_PAGE = False


# CONSTANTS


class C:
    """Example data shown in the templates. Nothing here is specific to Bootstrap."""

    ROUNDS = 10
    CURRENT_ROUND = 3
    ENDOWMENT = 20

    PARAMETERS = [
        ("Endowment", "$20.00 per round"),
        ("Rounds", "10, one of which is paid out at random"),
        ("Group size", "4 participants, re-matched every round"),
        ("Duration", "About 25 minutes"),
    ]

    HISTORY = [
        dict(round=1, you="Cooperate", other="Cooperate", payoff=8),
        dict(round=2, you="Cooperate", other="Defect", payoff=0),
        dict(round=3, you="Defect", other="Defect", payoff=4),
        dict(round=4, you="Defect", other="Cooperate", payoff=12),
        dict(round=5, you="Cooperate", other="Cooperate", payoff=8),
    ]

    PD_CHOICES = ["Cooperate", "Defect"]
    PD_PAYOFFS = {
        ("Cooperate", "Cooperate"): (8, 8),
        ("Cooperate", "Defect"): (0, 12),
        ("Defect", "Cooperate"): (12, 0),
        ("Defect", "Defect"): (4, 4),
    }

    # Payoff: 20 - contribution + 0.4 * (sum of contributions = 42)
    GROUP_RESULTS = [
        dict(player="Participant A", contribution=12, payoff=24.80, you=False),
        dict(player="Participant B", contribution=20, payoff=16.80, you=True),
        dict(player="Participant C", contribution=0, payoff=36.80, you=False),
        dict(player="Participant D", contribution=10, payoff=26.80, you=False),
    ]

    EARNINGS = [
        ("Part 1: Questionnaire", 2.50),
        ("Part 2: Public goods game", 8.75),
        ("Part 3: Risk elicitation", 4.00),
    ]

    LOTTERIES = [
        dict(
            name="Safe",
            icon="shield-check",
            color="success",
            outcomes=["$5.00 for sure"],
        ),
        dict(
            name="Balanced",
            icon="sliders",
            color="primary",
            outcomes=["50%: $8.00", "50%: $3.00"],
        ),
        dict(
            name="Risky",
            icon="lightning-charge",
            color="danger",
            outcomes=["10%: $40.00", "90%: $1.00"],
        ),
    ]

    ICON_GALLERY = {
        "Money and payoffs": [
            "coin",
            "cash-stack",
            "wallet2",
            "piggy-bank",
            "bank",
            "graph-up-arrow",
        ],
        "People and groups": [
            "person",
            "person-fill",
            "people",
            "people-fill",
            "person-circle",
            "diagram-3",
        ],
        "Time": [
            "clock",
            "hourglass-split",
            "stopwatch",
            "alarm",
            "calendar-event",
            "arrow-repeat",
        ],
        "Status and feedback": [
            "check-circle-fill",
            "x-circle-fill",
            "exclamation-triangle-fill",
            "info-circle-fill",
            "question-circle",
            "lock-fill",
        ],
        "Tasks and stimuli": [
            "dice-5",
            "trophy",
            "lightbulb",
            "puzzle",
            "keyboard",
            "bullseye",
        ],
        "Communication": [
            "chat-dots",
            "envelope",
            "hand-thumbs-up",
            "hand-thumbs-down",
            "megaphone",
            "bell",
        ],
    }

    OPTIONS = [
        dict(
            value="A",
            name="Option A",
            icon="shield-check",
            color="success",
            outcomes=["$5.00 for sure"],
        ),
        dict(
            value="B",
            name="Option B",
            icon="dice-5",
            color="danger",
            outcomes=["50%: $10.00", "50%: $0.00"],
        ),
    ]

    PAST_CHOICES = [
        dict(round=1, option="Option A", payoff=5),
        dict(round=2, option="Option B", payoff=10),
    ]


# PAGES


class Chapter(Page):
    """
    Shared by all chapters: participants may go back, and each template learns
    which chapter it is (for the progress bar and the label of the Next button).
    """

    allow_back = True

    @classmethod
    def templatevars(page, player: PlayerType) -> dict[str, Any]:
        number = page_order.index(page) + 1

        return dict(
            number=number,
            total=len(page_order),
            chapters=page_order,
        )


class Welcome(Chapter):
    allow_back = False  # There is nothing to go back to
    title = "Welcome"
    icon = "signpost-split"
    summary = "What is available, how this walkthrough works, and the few rules that matter in uproot."


class Layout(Chapter):
    title = "Layout"
    icon = "grid-1x2"
    summary = "Containers, the grid, breakpoints, flexbox, spacing, and sizing."


class TextAndMedia(Chapter):
    title = "Text and media"
    icon = "fonts"
    summary = "Headings, long instructions, text utilities, lists, quotes, and images."


class Icons(Chapter):
    title = "Icons"
    icon = "emoji-smile"
    summary = "Bootstrap Icons: loading, sizing, coloring, avatars, accessibility, and a gallery."


class Tables(Chapter):
    title = "Tables"
    icon = "table"
    summary = "History tables, results, payoff matrices, and tables on small screens."


class CardsAndLists(Chapter):
    title = "Cards and lists"
    icon = "card-heading"
    summary = "Cards, grids of cards, and list groups to structure content."


class Buttons(Chapter):
    title = "Buttons"
    icon = "hand-index-thumb"
    summary = "Variants, sizes, icons, groups, toggles, and one pitfall."


class Feedback(Chapter):
    title = "Feedback"
    icon = "chat-square-text"
    summary = (
        "Alerts, callouts, badges, progress bars, steppers, spinners, and placeholders."
    )


class ShowAndHide(Chapter):
    title = "Show and hide"
    icon = "arrows-collapse"
    summary = "Collapse, accordions, tabs, carousels, drawers, and pagination."


class Overlays(Chapter):
    title = "Overlays"
    icon = "window-stack"
    summary = "Dialogs, tooltips, popovers, toasts, and menus."


class Utilities(Chapter):
    title = "Utilities"
    icon = "tools"
    summary = (
        "Colors, borders, shadows, visibility, positioning, interaction, and dark mode."
    )


class PuttingItTogether(Chapter):
    title = "Putting it together"
    icon = "stars"
    summary = "A realistic decision screen with a home-made guided tour and a confirmation dialog."

    fields = dict(
        option=RadioField(
            label="Which option do you choose?",
            choices=[(option["value"], option["name"]) for option in C.OPTIONS],
        ),
    )


# PAGE ORDER


page_order = [
    Welcome,
    Layout,
    TextAndMedia,
    Icons,
    Tables,
    CardsAndLists,
    Buttons,
    Feedback,
    ShowAndHide,
    Overlays,
    Utilities,
    PuttingItTogether,
]
