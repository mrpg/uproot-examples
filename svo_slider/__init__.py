# Docs are available at https://uproot.science/
# Examples are available at https://github.com/mrpg/uproot-examples
#
# This example app is under the 0BSD license. You can use it freely and build on it
# without any limitations and without any attribution. However, these two lines must be
# preserved in any uproot app (the license file is automatically installed in projects):
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt

import math

from uproot.fields import *
from uproot.smithereens import *

DESCRIPTION = "Social Value Orientation slider measure (Murphy et al., 2011)"
LANDING_PAGE = False
APP_NAME = __name__


class C:
    # The six primary slider items: (own allocations, other's allocations)
    ITEMS = [
        ([85, 85, 85, 85, 85, 85, 85, 85, 85], [85, 76, 68, 59, 50, 41, 33, 24, 15]),
        ([85, 87, 89, 91, 93, 94, 96, 98, 100], [15, 19, 24, 28, 33, 37, 41, 46, 50]),
        ([50, 54, 59, 63, 68, 72, 76, 81, 85], [100, 98, 96, 94, 93, 91, 89, 87, 85]),
        ([50, 54, 59, 63, 68, 72, 76, 81, 85], [100, 89, 79, 68, 58, 47, 36, 26, 15]),
        ([100, 94, 88, 81, 75, 69, 63, 56, 50], [50, 56, 63, 69, 75, 81, 88, 94, 100]),
        ([100, 98, 96, 94, 93, 91, 89, 87, 85], [50, 54, 59, 63, 68, 72, 76, 81, 85]),
    ]
    NUM_POSITIONS = 9


def categorize(angle):
    if angle > 57.15:
        return "altruistic"

    if angle > 22.45:
        return "prosocial"

    if angle > -12.04:
        return "individualistic"

    return "competitive"


class Allocate(Page):
    @classmethod
    def fields(page, player):
        result = {}

        for i, (own, other) in enumerate(C.ITEMS, 1):
            result[f"choice_{i}"] = DecimalRangeField(
                anchoring=False,
                label=f"Item {i}",
                label_min=safe(f"You: {own[0]}<br>Other: {other[0]}"),
                label_max=safe(f"You: {own[-1]}<br>Other: {other[-1]}"),
                min=1,
                max=C.NUM_POSITIONS,
                places=0,
                step=1,
                hide_popover=True,
                render_kw={"data-item": str(i)},
            )

        return result

    @classmethod
    def jsvars(page, player):
        return {
            "items": [{"own": own, "other": other} for own, other in C.ITEMS],
        }

    @classmethod
    def after_once(page, player):
        choices = [
            int(getattr(player, f"choice_{i}")) for i in range(1, len(C.ITEMS) + 1)
        ]
        mean_self = sum(
            own[choice - 1] for (own, _), choice in zip(C.ITEMS, choices)
        ) / len(choices)
        mean_other = sum(
            other[choice - 1] for (_, other), choice in zip(C.ITEMS, choices)
        ) / len(choices)

        player.mean_self = mean_self
        player.mean_other = mean_other
        player.svo_angle = math.degrees(math.atan2(mean_other - 50, mean_self - 50))
        player.svo_category = categorize(player.svo_angle)


class Results(Page):
    pass


def pipeline(session):
    rows = []

    for player in session.players:
        player_data = player.within(app=APP_NAME)
        angle = player_data.get("svo_angle")

        if angle is not None:
            rows.append(
                {
                    "session": session.name,
                    "uname": player.name,
                    **{
                        f"choice_{i}": player_data.get(f"choice_{i}")
                        for i in range(1, len(C.ITEMS) + 1)
                    },
                    "mean_self": player_data.get("mean_self"),
                    "mean_other": player_data.get("mean_other"),
                    "svo_angle": angle,
                    "svo_category": player_data.get("svo_category"),
                }
            )

    return rows


page_order = [
    Allocate,
    Results,
]
