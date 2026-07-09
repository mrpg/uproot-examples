# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt

"""
Emoji Sorting Task for Kids

Children see 10 emoji cards and drag each one into either the "NICE" or
"NASTY" bucket.  Each placement is recorded via a hidden RadioField
(value 1 = NICE, value 2 = NASTY).
"""

from uproot.fields import *
from uproot.smithereens import *

DESCRIPTION = "Sort emojis into NICE or NASTY buckets"
LANDING_PAGE = False


class C:
    ITEMS = [
        "\U0001f60a",  # 😊 smiling face with smiling eyes
        "\U0001f621",  # 😡 pouting face
        "\U0001f970",  # 🥰 smiling face with hearts
        "\U0001f4a9",  # 💩 pile of poo
        "\U0001f31e",  # 🌞 sun with face
        "\U0001f480",  # 💀 skull
        "\U0001f338",  # 🌸 cherry blossom
        "\U0001f47f",  # 👿 angry face with horns
        "\U0001f308",  # 🌈 rainbow
        "\U0001f40d",  # 🐍 snake
    ]

    NUM_ITEMS = len(ITEMS)
    BUCKET_LABELS = ("NICE", "NASTY")

    __export__ = ["NUM_ITEMS", "ITEMS", "BUCKET_LABELS"]


def item_field_name(index):
    return f"item_{index}"


class Categorize(Page):
    # allow_back = True

    @classmethod
    def fields(page, player: PlayerType) -> dict[str, Field]:
        return {
            item_field_name(i): RadioField(
                label=item,
                choices=[
                    (1, C.BUCKET_LABELS[0]),
                    (2, C.BUCKET_LABELS[1]),
                ],
                class_wrapper="d-none",
            )
            for i, item in enumerate(C.ITEMS)
        }


class Results(Page):
    allow_back = True


page_order = [
    Categorize,
    Results,
]
