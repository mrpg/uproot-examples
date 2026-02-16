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

    NOTE: The "code_to_proceed" field below could also be set up as a stealth field. Stealth fields
    are not recorded in the database at all -- they are processed exclusively via the
    handle_stealth_fields() method. This is useful for fields that serve a purely functional purpose
    (like a password gate) and whose values you do not want to persist.

    To convert this page to use stealth fields, you would:

    1. Add a class attribute listing the stealth field names:

           stealth_fields = ["code_to_proceed"]

       IMPORTANT: The field must still be defined in fields() as well! The stealth_fields attribute
       only controls whether the field's value is stored in the database. The field definition in
       fields() is still required so that uproot knows how to render and validate the form input.

    2. Replace the validate() method with handle_stealth_fields(), which receives the stealth field
       values as its arguments:

           @classmethod
           def handle_stealth_fields(page, player, code_to_proceed):
               if code_to_proceed != C.CODE:
                   return "The code you entered is incorrect. Please try again."

       Returning a string from handle_stealth_fields() shows an error and prevents the participant
       from advancing, just like validate(). Returning None (the default) lets them proceed.

    The validate() method and stealth fields can coexist on the same page: use stealth_fields for
    data you do not want stored (e.g. passwords, comprehension checks) and regular fields + validate()
    for data you do want stored. See the "quiz" example app for a full stealth fields demonstration.
    """

    @classmethod
    def fields(page, player):
        return {
            "code_to_proceed": StringField(
                description=safe(
                    f"Hint: The code to proceed is <b class='font-monospace'>{C.CODE}</b>."
                ),
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


# PAGE ORDER


page_order = [
    InputValidationBasic,
    InputValidationAdvanced,
]
