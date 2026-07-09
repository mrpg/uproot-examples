# Docs are available at https://uproot.science/
# Examples are available at https://github.com/mrpg/uproot-examples
#
# This example app is under the 0BSD license. You can use it freely and build on it
# without any limitations and without any attribution. However, these two lines must be
# preserved in any uproot app (the license file is automatically installed in projects):
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt

"""
Drag and Drop Sorting Task

Participants see a set of draggable items and must sort them into two buckets.
By default, each item is tracked individually via a hidden RadioField that
records which bucket it was placed in (1 or 2).

This example demonstrates:
  - HTML5 drag-and-drop with a Bootstrap UI
  - One hidden RadioField per item, populated by client-side JavaScript
  - A flexible, well-commented structure for easy customization

To customize:
  - Change ITEMS in class C to use your own labels, images, or HTML snippets.
  - Change BUCKET_LABELS to rename the two buckets.
  - For identical/fungible items where only the *count* matters (not which
    specific item went where), see the "COUNT-ONLY MODE" comment block below
    for an alternative using a single IntegerField.
"""

from uproot.fields import *
from uproot.smithereens import *

DESCRIPTION = "Drag-and-drop sorting into two buckets"
LANDING_PAGE = False


class C:
    """
    Constants exposed to templates via {{ app.C }}.

    Customize ITEMS to change what participants sort. Each entry is a short
    string that will appear inside a draggable card. You can use plain text
    or HTML (e.g., '<img src="..." class="img-fluid" style="max-height:40px">').
    """

    # The items to sort. Each gets its own hidden RadioField.
    # Replace these with your own stimuli (words, images, icons, etc.).
    ITEMS = [
        "Apple",
        "Banana",
        "Cherry",
        "Dog",
        "Elephant",
        "Frog",
        "Guitar",
        "Hammer",
        "Igloo",
        "Jacket",
    ]

    # Derived from ITEMS — no need to keep this in sync manually.
    NUM_ITEMS = len(ITEMS)

    # Labels for the two buckets. Shown as headings above each bucket.
    BUCKET_LABELS = ("Bucket 1", "Bucket 2")

    # Export constants so they are available in templates as {{ app.C.… }}
    __export__ = ["NUM_ITEMS", "ITEMS", "BUCKET_LABELS"]


# ─── Field name helper ───────────────────────────────────────────────
# Each item gets a field named "item_0", "item_1", … so we can look them
# up from both Python and JavaScript.


def item_field_name(index: int) -> str:
    """Return the form field name for item at the given index."""
    return f"item_{index}"


# ─── Pages ────────────────────────────────────────────────────────────


class DragAndDrop(Page):
    """
    Main drag-and-drop page.

    One hidden RadioField per item records which bucket it was placed in.
    JavaScript keeps these values in sync with the drag-and-drop UI so that
    the normal form submission stores every placement decision.
    """

    @classmethod
    def fields(page, player: PlayerType) -> dict[str, Field]:
        # Build one hidden RadioField per item.
        # Value 1 = Bucket 1, value 2 = Bucket 2.
        # Items start unsorted, so no default is set — the participant must
        # place every item before submitting.
        return {
            item_field_name(i): RadioField(
                label=item,
                choices=[
                    (1, C.BUCKET_LABELS[0]),
                    (2, C.BUCKET_LABELS[1]),
                ],
                # Hide the rendered field; JS sets the value via the DOM.
                class_wrapper="d-none",
            )
            for i, item in enumerate(C.ITEMS)
        }


# ─────────────────────────────────────────────────────────────────────
# COUNT-ONLY MODE
#
# If your items are identical / fungible and you only care about *how many*
# went into Bucket 1 (not *which* ones), replace the fields() method above
# with the simpler version below. You will also need to adjust the HTML
# template: instead of setting one hidden radio per item, set a single
# hidden input named "bucket1_count".
#
#   class DragAndDrop(Page):
#       @classmethod
#       def fields(page, player: PlayerType) -> dict[str, Field]:
#           return dict(
#               bucket1_count=IntegerField(
#                   label="Items in Bucket 1",
#                   min=0,
#                   max=C.NUM_ITEMS,
#                   default=0,
#                   class_wrapper="d-none",
#               ),
#           )
#
# In the template JS, replace the per-item syncField() calls with:
#
#   const input = document.querySelector('input[name="bucket1_count"]');
#   input.value = bucket1.querySelectorAll(".draggable-item").length;
#
# And in Results.html, display player.bucket1_count instead of the
# per-item table.
# ─────────────────────────────────────────────────────────────────────


class Results(Page):
    """
    Displays a summary of each item's placement.
    """

    pass


page_order = [
    DragAndDrop,
    Results,
]
