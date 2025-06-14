"""
Docs are available at https://uproot.science/
Examples are available at https://github.com/mrpg/uproot-examples

This example app is under the 0BSD license. You can use it freely and build on it
without any limitations and without any attribution. However, these two lines must be
preserved in any uproot app (the license file is automatically installed in a project):

Third-party dependencies:
- uproot: LGPL v3+, see ../uproot_license.txt
"""

from uproot.fields import *
from uproot.smithereens import *
from uproot.types import Page

DESCRIPTION = "Sample payment form with a 'stealth field'"


class PaymentForm(Page):
    fields = dict(
        iban=IBANField(  # install schwifty to use this field
            label="What is your International Bank Account Number (IBAN)?",
            description="Example IBAN: DE75512108001245126199",
        ),
        rating=DecimalRangeField(
            label="How would you rate this experiment?",
            min=0,
            max=5,
            step=1,
        ),
    )

    # fields listed here are handled by the method below and NOT saved to the DB
    stealth_fields = ["iban"]

    @classmethod
    async def handle_stealth_fields(page, player, iban: str):
        # this method could write the stealth field to a separate file, or do whatever else
        # however, since this is just an example, it just prints the IBAN:
        print(f"New payment data: {player} (rating: {player.rating}) has IBAN '{iban}'")

        # note: you cannot stop the player from proceeding - for that, you would have to
        # build a custom WTForms validator


page_order = [PaymentForm]
