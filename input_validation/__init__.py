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
    Example of how to validate an input field before allowing the participant to proceed to the next page.
    """

    @classmethod
    def fields(page, player):
        return {
            "code_to_proceed": StringField(
                description=safe(f"Hint: The code to proceed is <b class='font-monospace'>{C.CODE}</b>."),
                label=safe(
                    "Please enter the code provided to you by the experimenter to proceed to the next page."
                ),
                render_kw={"autofocus": True, "class": "font-monospace w-auto"},
            ),
        }

    @classmethod
    def validate(page, player, data):
        if data.get("code_to_proceed") != C.CODE:
            return "The code you entered is incorrect. Please try again."


class InputValidationAdvanced(Page):
    """
    Example of how to validate multiple input fields before allowing the participant to proceed to the next page.
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
                max = 100,
                min = 0,
                render_kw={"class": "flex-grow-0 text-end", "style": "width: max-content !important;"},
            ),
            "share_risky_asset": IntegerField(
                addon_end="%",
                label=safe(
                    "Which share of your budget would you like to invest in the <em>risky</em> asset?"
                ),
                max = 100,
                min = 0,
                render_kw={"class": "flex-grow-0 text-end", "style": "width: max-content !important;"},
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


# PAGE ORDER


page_order = [
    InputValidationBasic,
    InputValidationAdvanced,
]
