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

DESCRIPTION = "Randomly choose one page or one bracketed page block"
LANDING_PAGE = False


class Intro(Page):
    pass


class ProductChoice(Page):
    @classmethod
    def fields(page, player: PlayerType) -> dict[str, Field]:
        return {
            "product_choice": RadioField(
                choices=[
                    ("basic", "Basic plan"),
                    ("pro", "Pro plan"),
                    ("team", "Team plan"),
                ],
                label="Which plan would you choose?",
            ),
        }


class TreatmentInfo(Page):
    pass


class TreatmentTask(Page):
    @classmethod
    def fields(page, player: PlayerType) -> dict[str, Field]:
        return {
            "treatment_code": StringField(
                label="Enter the code shown on the previous page.",
                render_kw={"class": "font-monospace w-auto"},
            ),
        }

    @classmethod
    def validate(page, player, data):
        if data.get("treatment_code", "").strip().upper() != "BLUE":
            return "The code is BLUE."


class OpenResponse(Page):
    @classmethod
    def fields(page, player: PlayerType) -> dict[str, Field]:
        return {
            "open_response": TextAreaField(
                label="What would make this product more useful?",
                render_kw={"rows": 4},
            ),
        }


class Results(Page):
    @classmethod
    def templatevars(page, player: PlayerType) -> dict[str, Any]:
        selected = player.get("between_showed", [])
        selected_page = selected[-1] if selected else None
        branch_names = {
            "between/ProductChoice": "Single-page choice branch",
            "between/TreatmentInfo": "Two-page bracketed treatment branch",
            "between/OpenResponse": "Single-page open-response branch",
        }
        branch_name = (
            branch_names.get(selected_page, "Unknown branch")
            if selected_page is not None
            else "Unknown branch"
        )

        return {
            "selected_page": selected_page,
            "branch_name": branch_name,
        }


page_order = [
    Intro,
    Between(
        ProductChoice,
        Bracket(
            TreatmentInfo,
            TreatmentTask,
        ),
        OpenResponse,
    ),
    Results,
]
