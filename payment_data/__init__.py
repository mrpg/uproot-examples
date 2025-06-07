from uproot.fields import *
from uproot.smithereens import *
from uproot.types import Page


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
