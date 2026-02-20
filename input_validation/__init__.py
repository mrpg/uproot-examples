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

DESCRIPTION = "Demonstrate how to validate input(s) and provide feedback before proceeding to the next page."
LANDING_PAGE = False


# CONSTANTS


class C:
    """Constants"""

    CODE = "R2-D2"


# PAGES


class InputValidationBasic(Page):
    """
    Example of how to validate input fields before allowing the participant to proceed to the next page.

    This is useful for cases in which you want to ensure that participants enter a particular value or values that are consistent with each other before they can proceed.
    """

    @classmethod
    def fields(page, player):
        return {
            "share_min": IntegerField(
                addon_end="%",
                label=safe(
                    "What is the <em>minimum</em> share of your budget that would like to invest in the group project?"
                ),
                max=100,
                min=0,
                render_kw={
                    "class": "flex-grow-0 text-end",
                    "style": "width: max-content !important;",
                },
            ),
            "share_max": IntegerField(
                addon_end="%",
                label=safe(
                    "What is the <em>maximum</em> share of your budget that would like to invest in the group project?"
                ),
                max=100,
                min=0,
                render_kw={
                    "class": "flex-grow-0 text-end",
                    "style": "width: max-content !important;",
                },
            ),
        }

    @classmethod
    def validate(page, player, data):
        if data.get("share_min") > data.get("share_max"):
            return "The maximum share must be at least as large as the minimum share."


class InputValidationStealthField(Page):
    """
    Example of how to validate an input field that is not stored in the database (a “stealth field”) before allowing the participant to proceed to the next page.

    This is useful if your input validation amounts to allowing a particular value only (like in a password gate or in many comprehension checks) so that there is no need to store the input in the database.
    """

    stealth_fields = ["code_to_proceed"]

    @classmethod
    def fields(page, player):
        return {
            "code_to_proceed": StringField(
                label=safe(
                    f"Please enter the code provided to you by the experimenter to proceed to the next page. <span class='fw-normal ms-2 text-body-tertiary'>(The code is <span class='font-monospace'>{C.CODE}</span>.)</span>"
                ),
                render_kw={"autofocus": True, "class": "font-monospace w-auto"},
            ),
        }

    @classmethod
    def handle_stealth_fields(page, player, data):
        if data.get("code_to_proceed") != C.CODE:
            return "The code you entered is incorrect. Please try again."


class InputValidationAdvanced(Page):
    """
    Example of how to validate multiple input fields and provide custom error messages before allowing the participant to proceed to the next page.
    """

    @classmethod
    def before_always_once(page, player):
        # We use the before_always_once hook to initialize a counter for invalid inputs. This counter is then
        # incremented in the validate method every time the participant enters an incorrect value.
        player.input_errors = 0

    @classmethod
    def fields(page, player):
        return {
            "share_safe_asset": IntegerField(
                addon_end="%",
                label=safe(
                    "Which share of your budget would you like to invest in the <em>safe</em> asset?"
                ),
                max=100,
                min=0,
                render_kw={
                    "class": "flex-grow-0 text-end",
                    "style": "width: max-content !important;",
                },
            ),
            "share_risky_asset": IntegerField(
                addon_end="%",
                label=safe(
                    "Which share of your budget would you like to invest in the <em>risky</em> asset?"
                ),
                max=100,
                min=0,
                render_kw={
                    "class": "flex-grow-0 text-end",
                    "style": "width: max-content !important;",
                },
            ),
        }

    @classmethod
    def validate(page, player, data):
        if data.get("share_safe_asset") + data.get("share_risky_asset") != 100:
            player.input_errors += 1
            return [
                safe(
                    f"The sum of the two shares must equal 100%. You have to set this share to {100 - data.get('share_risky_asset')}% if you choose to invest {data.get('share_risky_asset')}% of your budget in the <em>risky</em> asset."
                ),
                safe(
                    f"The sum of the two shares must equal 100%. You have to set this share to {100 - data.get('share_safe_asset')}% if you choose to invest {data.get('share_safe_asset')}% of your budget in the <em>safe</em> asset."
                ),
            ]


class InputValidationBootstrapClasses(Page):
    """
    Example of how to validate multiple input fields and provide custom error messages with formatting based on Bootstrap classes only.
    """

    stealth_fields = ["conversion_rate", "group_size"]

    @classmethod
    def fields(page, player):
        return {
            "group_size": RadioField(
                choices=[1, 2, 3, 4, 5],
                label=safe(
                    "What is the group size in this study? <span class='fw-normal ms-2 text-body-tertiary'>(The correct answer is <span class='font-monospace'>1</span>.)</span>"
                ),
                layout="horizontal",
            ),
            "conversion_rate": DecimalField(
                addon_end="€/ECU",
                label=safe(
                    "What is the conversion rate between real money (€) and experimental currency units (ECU) in this study? <span class='fw-normal ms-2 text-body-tertiary'>(The correct answer is <span class='font-monospace'>1.95583</span>.)</span>"
                ),
                step=0.00001,
                render_kw={
                    "class": "flex-grow-0 text-end",
                    "style": "width: max-content !important;",
                },
            ),
        }

    @classmethod
    def validate(page, player, data):
        invalid_inputs = []
        if data.get("group_size") != 1:
            invalid_inputs += ["group_size"]
        if not (
            data.get("conversion_rate") > 1.955829
            and data.get("conversion_rate") < 1.955831
        ):
            invalid_inputs += ["conversion_rate"]
        if len(invalid_inputs) > 0:
            return invalid_inputs
        else:
            return None


# PAGE ORDER


page_order = [
    InputValidationBasic,
    InputValidationStealthField,
    InputValidationAdvanced,
    InputValidationBootstrapClasses,
]
