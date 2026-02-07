# Docs are available at https://uproot.science/
# Examples are available at https://github.com/mrpg/uproot-examples
#
# This example app is under the 0BSD license. You can use it freely and build on it
# without any limitations and without any attribution. However, these two lines must be
# preserved in any uproot app (the license file is automatically installed in projects):
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt

import wtforms
from uproot.fields import *
from uproot.smithereens import *

DESCRIPTION = "Showcasing uproot input elements and typography features"
LANDING_PAGE = False

# CONSTANTS


class C:
    """Values from class C can be directly included in HTML templates."""

    BUDGET = 10.00  # Budget per player in €
    PRECISION = 0.01


# PAGES


class ExampleInputsWTForms(Page):
    """Examples of input fields provided by WTForms."""

    @classmethod
    def fields(page, player):
        return {
            "boolean_field": wtforms.BooleanField(
                description=safe(
                    "Description for the <code class='text-black-50'>wtforms.BooleanField</code>."
                ),
                label=safe(
                    "Select the checkbox if you agree to participate in this study. <code class='ms-3 text-black-50'>wtforms.BooleanField</code>"
                ),
            ),
            "date_field": wtforms.DateField(
                description=safe(
                    "Description for the <code class='text-black-50'>wtforms.DateField</code>."
                ),
                label=safe(
                    "Specify the date at which you would like to participate in Part 2 of this study. <code class='ms-3 text-black-50'>wtforms.DateField</code>"
                ),
                render_kw={"class": "w-auto"},
            ),
            "decimal_field": wtforms.DecimalField(
                default=1.23,
                description=safe(
                    "Description for the <code class='text-black-50'>wtforms.DecimalField</code>."
                ),
                label=safe(
                    "Which amount of money (in €) are you willing to contribute to the group project? <code class='ms-3 text-black-50'>wtforms.DecimalField</code>"
                ),
                places=2,
                render_kw={"class": "w-auto"},
                validators=[wtforms.validators.NumberRange(min=0, max=C.BUDGET)],
                widget=wtforms.widgets.NumberInput(step=C.PRECISION),
            ),
            "decimal_range_field": wtforms.fields.DecimalRangeField(
                default=3.45,
                description=safe(
                    "Description for the <code class='text-black-50'>wtforms.DecimalRangeField</code>."
                ),
                label=safe(
                    "Which amount of money (in €) are you willing to contribute to the group project? <code class='ms-3 text-black-50'>wtforms.DecimalRangeField</code>"
                ),
                render_kw={"class": "w-50"},
                validators=[wtforms.validators.NumberRange(min=0, max=C.BUDGET)],
            ),
            "email_field": wtforms.EmailField(
                description=safe(
                    "Description for the <code class='text-black-50'>wtforms.EmailField</code>."
                ),
                label=safe(
                    "Enter your e-mail address here to be informed as soon as your payoff has been transferred to your bank account. <code class='ms-3 text-black-50'>wtforms.EmailField</code>"
                ),
                render_kw={"class": "w-75"},
                # validators=[wtforms.validators.Email()],  # This requires email_validator to be installed
            ),
            "file_field": wtforms.FileField(
                description=safe(
                    "Description for the <code class='text-black-50'>wtforms.FileField</code>."
                ),
                label=safe(
                    "Select the file that you wish to upload to the server. <code class='ms-3 text-black-50'>wtforms.FileField</code>"
                ),
                render_kw={"class": "w-50"},
            ),
            "integer_field": wtforms.IntegerField(
                default=4,
                description=safe(
                    "Description for the <code class='text-black-50'>wtforms.IntegerField</code>."
                ),
                label=safe(
                    "How would you rate this hotel (in ★🌟)? <code class='ms-3 text-black-50'>wtforms.IntegerField</code>"
                ),
                render_kw={"class": "w-auto"},
                validators=[wtforms.validators.NumberRange(min=0, max=5)],
            ),
            "radio_field": wtforms.RadioField(
                choices=[(1, "Yes"), (0, "No")],
                default=0,
                description=safe(
                    "Description for the <code class='text-black-50'>wtforms.RadioField</code>."
                ),
                label=safe(
                    "Would you be willing to serve as your group’s leader? <code class='ms-3 text-black-50'>wtforms.RadioField</code>"
                ),
            ),
            "radio_field_inline": wtforms.RadioField(
                choices=[(1, "Yes"), (0, "No"), (0.5, "Maybe")],
                default=0,
                description=safe(
                    "Description for the <code class='text-black-50'>wtforms.RadioField</code>."
                ),
                label=safe(
                    "Would you be willing to serve as your group’s leader? <span class='text-body-tertiary'><code class='ms-3 text-black-50'>wtforms.RadioField</code> with <code class='text-black-50'>class='form-check-inline'</code></span>"
                ),
                render_kw={"class": "form-check-inline"},
            ),
            "select_field": wtforms.SelectField(
                choices=[
                    (0, "Please select an option"),
                    (1, "Bayer Leverkusen"),
                    (2, "VfB Stuttgart"),
                    (3, "Bayern München"),
                    (4, "RB Leipzig"),
                    (5, "BVB 09 Dortmund"),
                ],
                default=0,
                description=safe(
                    "Description for the <code class='text-black-50'>wtforms.SelectField</code>."
                ),
                label=safe(
                    "Which of the following soccer teams would you like to win the German championship? <code class='ms-3 text-black-50'>wtforms.SelectField</code>"
                ),
                render_kw={"class": "w-auto"},
            ),
            "string_field": wtforms.StringField(
                description=safe(
                    "Description for the <code class='text-black-50'>wtforms.StringField</code>."
                ),
                label=safe(
                    "Please state your primary field of study. <code class='ms-3 text-black-50'>wtforms.StringField</code>"
                ),
                render_kw={"placeholder": "Insert primary field of study here."},
            ),
            "text_area_field": wtforms.TextAreaField(
                description=safe(
                    "Description for the <code class='text-black-50'>wtforms.TextAreaField</code>."
                ),
                label=safe(
                    "Please state your primary field of study. <code class='ms-3 text-black-50'>wtforms.TextAreaField</code>"
                ),
                # render_kw={"placeholder": "Insert primary field of study here."},
            ),
            "text_area_field_only_floating_label": wtforms.TextAreaField(
                description=safe(
                    "Description for the <code class='text-black-50'>wtforms.TextAreaField</code>."
                ),
                label="",
                render_kw={"placeholder": "Insert primary field of study here."},
            ),
        }


class ExampleInputsUprootFields(Page):
    """
    Examples of input fields provided by uproot. These fields are based on WTForms but simplify the syntax substantially.
    """

    @classmethod
    def fields(page, player):
        return {
            "boolean_field": BooleanField(
                description="Description for the <code class='text-black-50'>BooleanField</code>.",
                label=safe(
                    "Select the checkbox if you agree to participate in this study. <code class='ms-3 text-black-50'>BooleanField</code>"
                ),
                render_kw={"class": "border-primary"},
            ),
            "date_field": DateField(
                description="Description for the <code class='text-black-50'>DateField</code>.",
                label=safe(
                    "Specify the date at which you would like to participate in Part 2 of this study. <code class='ms-3 text-black-50'>DateField</code>"
                ),
                render_kw={"class": "w-auto"},
            ),
            "decimal_field": DecimalField(
                addon_start="€",
                default=1.23,
                description="Description for the <code class='text-black-50'>DecimalField</code>.",
                label=safe(
                    "Which amount of money are you willing to contribute to the group project? <code class='ms-3 text-black-50'>DecimalField</code>"
                ),
                max=C.BUDGET,
                min=0,
                places=2,
                render_kw={
                    "style": "flex: unset !important; width: fit-content !important;"
                },
                step=C.PRECISION,
            ),
            "decimal_range_field": DecimalRangeField(
                class_wrapper="w-75",
                default=3.45,
                description="Description for the <code class='text-black-50'>DecimalRangeField</code> with <code class='text-black-50'>class_wrapper=\"w-75\"</code> and default labels left and right.",
                label=safe(
                    "Which amount of money (in €) are you willing to contribute to the group project? <code class='ms-3 text-black-50'>DecimalRangeField</code>"
                ),
                max=C.BUDGET,
                min=0,
                places=2,
                step=C.PRECISION,
            ),
            "decimal_range_field_no_popover": DecimalRangeField(
                class_wrapper="w-50",
                default=5.0,
                description="Description for the <code class='text-black-50'>DecimalRangeField</code> with <code class='text-black-50'>hide_popover=True</code> and empty labels.",
                hide_popover=True,
                label=safe(
                    "Position the slider as close to the middle as you can. <code class='ms-3 text-black-50'>DecimalRangeField</code>"
                ),
                label_max="",
                label_min="",
                max=10,
                min=0,
                places=1,
                step=0.1,
            ),
            "decimal_range_field_no_anchoring": DecimalRangeField(
                anchoring=False,
                default=3.45,
                description="Description for the <code class='text-black-50'>DecimalRangeField</code> with <code class='text-black-50'>anchoring=False</code> and custom labels left and right.",
                label=safe(
                    "What is your willingness to pay? <code class='ms-3 text-black-50'>DecimalRangeField</code>"
                ),
                label_max=safe("<span class='text-success fw-semibold'>My entire<br>budget</span>"),
                label_min=safe("<span class='text-danger fw-semibold'>Nothing<br>at all</span>"),
                max=C.BUDGET,
                min=0,
                places=2,
                step=C.PRECISION,
            ),
            "decimal_range_field_no_anchoring_custom_formatter": DecimalRangeField(
                anchoring=False,
                default=3.45,
                description="Description for the <code class='text-black-50'>DecimalRangeField</code> with <code class='text-black-50'>anchoring=False</code> and a custom formatter.",
                label=safe(
                    "Which amount would you like to donate? <code class='ms-3 text-black-50'>DecimalRangeField</code>"
                ),
                max=C.BUDGET,
                min=-C.BUDGET,
                places=2,
                step=C.PRECISION,
            ),
            "email_field_top_complete": EmailField(
                description="Description for the <code class='text-black-50'>EmailField</code> with both main (top) and floating label.",
                label=safe(
                    "Enter your e-mail address here to be informed as soon as your payoff has been transferred to your bank account. <code class='ms-3 text-black-50'>EmailField</code>"
                ),
                label_floating="Your e-mail address",
                render_kw={"class": "w-75"},
            ),
            "email_field_old_school": EmailField(
                description="Description for the <code class='text-black-50'>EmailField</code> with empty floating label but a placeholder (AKA old-school styling).",
                label=safe(
                    "Enter your e-mail address here to be informed as soon as your payoff has been transferred to your bank account. <code class='ms-3 text-black-50'>EmailField</code>"
                ),
                render_kw={"class": "w-75", "placeholder": "example@example.org"},
            ),
            "email_field_floating_label_only": EmailField(
                description="Description for the <code class='text-black-50'>EmailField</code> with floating label only.",
                label_floating="Enter your e-mail address here to be informed about your payoff",
                render_kw={"class": "w-75"},
            ),
            "file_field": FileField(
                description="Description for the <code class='text-black-50'>FileField</code>.",
                label=safe(
                    "Select the file that you wish to upload to the server. <code class='ms-3 text-black-50'>FileField</code>"
                ),
                render_kw={"class": "w-50"},
            ),
            "integer_field": IntegerField(
                addon_start=safe("I would award <em>this</em> hotel"),
                addon_end="★★.",
                class_addon_start="bg-danger-subtle border-warning text-danger",
                class_addon_end="bg-warning border-warning",
                class_wrapper="mb-5 mt-5 card card-body bg-warning-subtle border-warning w-50",
                description="Description for the <code class='text-black-50'>IntegerField</code>. This demonstrates the extent to which manual formatting can be applied.",
                label=safe(
                    "How would you rate <em>this</em> hotel? <code class='ms-3 text-black-50'>IntegerField</code>"
                ),
                max=5,
                min=0,
                render_kw={
                    "class": "border-warning font-monospace fw-bold",
                    "style": "flex: unset !important; width: fit-content !important;",
                },
            ),
            "likert_field": LikertField(
                class_wrapper="border-primary card my-4 px-4 py-3 w-75",
                description="Description for the <code class='text-black-50'>LikertField</code> with custom CSS classes set via <code class='text-black-50'>class_wrapper</code>.",
                label=safe(
                    "I like ice cream. <code class='ms-3 text-black-50'>LikertField</code>"
                ),
                label_max="Agree strongly",
                label_min="Disagree strongly",
                max=10,
                min=-3,
                render_kw={"class": "fw-bold text-body-tertiary"},
            ),
            "likert_field_2": LikertField(
                description="Description for the Bonn <code class='text-black-50'>LikertField</code>.",
                label=safe(
                    "Would you like to visit Bonn? <code class='ms-3 text-black-50'>LikertField</code>"
                ),
                label_max="Very much",
                label_min="Not at all",
                max=5,
                min=-5,
            ),
            "likert_field_3": LikertField(
                description="Description for the Cologne <code class='text-black-50'>LikertField</code>.",
                label=safe(
                    "Would you like to visit Cologne? <code class='ms-3 text-black-50'>LikertField</code>"
                ),
                label_max="Very much",
                label_min="Not at all",
                max=5,
                min=-5,
            ),
            "likert_field_4": LikertField(
                label=safe(
                    "Would you like to visit Münster or Bonn or Cologne or Darmstadt or Seeheim-Jugenheim or Bielefeld or Berlin or Hamburg?"
                ),
                label_max="Very much",
                label_min="Not at all",
                max=5,
                min=-5,
            ),
            "likert_field_5": LikertField(
                label=safe("Would you like to visit Melbourne?"),
                label_max="Very much",
                label_min="Not at all",
                min=-5,
                max=5,
            ),
            "radio_field": RadioField(
                choices=[(True, "Yes"), (False, "No")],
                description="Description for the <code class='text-black-50'>RadioField</code>, vertical.",
                label=safe(
                    "Would you be willing to serve as your group’s leader? <code class='ms-3 text-black-50'>RadioField</code>"
                ),
            ),
            "radio_field_inline": RadioField(
                choices=[
                    (1, safe("<b class='text-success'>Yes</b>")),
                    (0, safe("<b class='text-danger'>No</b>")),
                    (0.5, safe("<b class='text-warning'>Maybe</b>")),
                ],
                description="Description for the <code class='text-black-50'>RadioField</code>, horizontal.",
                label=safe(
                    "Would you be willing to serve as your group’s leader? <code class='ms-3 text-black-50'>RadioField</code>"
                ),
                layout="horizontal",
            ),
            "radio_field_optional": RadioField(
                choices=[("f", "Female"), ("m", "Male"), ("x", "Nonbinary")],
                description="You can skip this question if you prefer not to answer.",
                label=safe(
                    "What is your gender? "
                    + "<span class='text-black-50'><code class='ms-3 text-black-50'>RadioField</code> with attribute "
                    + "<code class='text-black-50'>optional=True</code></span>"
                ),
                optional=True,
            ),
            "select_field": SelectField(
                choices=[
                    (0, "Please select an option"),
                    (1, "Bayer Leverkusen"),
                    (2, "VfB Stuttgart"),
                    (3, "Bayern München"),
                    (4, "RB Leipzig"),
                    (5, "BVB 09 Dortmund"),
                ],
                default=0,
                description="Description for the <code class='text-black-50'>SelectField</code>.",
                label=safe(
                    "Which of the following soccer teams would you like to win the German championship? <code class='ms-3 text-black-50'>SelectField</code>"
                ),
                render_kw={"class": "w-auto"},
            ),
            "string_field_complete": StringField(
                addon_start="Major field of study",
                addon_end="Minor field of study can be omitted.",
                class_addon_end="text-black-50",
                description="Description for the <code class='text-black-50'>StringField</code> with both main (top) and floating label.",
                label=safe(
                    "Please state your primary field of study. <code class='ms-3 text-black-50'>StringField</code>"
                ),
                label_floating="Your primary field of study",
            ),
            "text_area_field_placeholder": TextAreaField(
                addon_start="Test",
                description="Description for the <code class='text-black-50'>TextAreaField</code> with empty floating label but a placeholder (AKA old-school styling).",
                label=safe(
                    "Please explain <i>in your own words</i> which criteria you used to make decisions in this study. <code class='ms-3 text-black-50'>TextAreaField</code>"
                ),
                render_kw={
                    "placeholder": "Your description",
                    "style": "height: 100px;",
                },
            ),
            "text_area_field_only_floating_label": TextAreaField(
                addon_end="Test",
                description="Description for the <code class='text-black-50'>TextAreaField</code> with floating label only.",
                label="",
                label_floating="Name your primary field of study here",
                render_kw={"style": "height: 100px"},
            ),
            # "iban_field": IBANField(
            #     class_wrapper="mt-5 card card-body bg-warning-subtle border-warning",
            #     description="Description for the <code class='text-black-50'>IBANField</code>.",
            #     label=safe(
            #         "Please provide an IBAN <i>from the euro area</i> so that we can transfer your remuneration to your bank account. <code class='ms-3 text-black-50'>IBANField</code>"
            #     ),
            #     label_floating="IBAN of your bank account",
            #     render_kw={"class": "border-warning"},
            # ),
        }


class Typography(Page):
    """Showcase the default fonts used by uproot if webfonts are loaded"""

    pass


class TypographyNoWebfonts(Page):
    """Showcase the default fonts used by uproot if no webfonts are used"""

    pass


# PAGE ORDER


page_order = [
    Typography,
    TypographyNoWebfonts,
    ExampleInputsUprootFields,
    ExampleInputsWTForms,
]
