# Docs are available at https://uproot.science/
# Examples are available at https://github.com/mrpg/uproot-examples
#
# This example app is under the 0BSD license. You can use it freely and build on it
# without any limitations and without any attribution. However, these two lines must be
# preserved in any uproot app (the license file is automatically installed in projects):
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt

import random

from uproot.fields import *
from uproot.smithereens import *

DESCRIPTION = "Public goods game with strategy method (Fischbacher et al., 2001)"
SUGGESTED_MULTIPLE = 4


class C:
    ENDOWMENT = 20
    MPCR = cu("0.4")
    GROUP_SIZE = 4


class GroupPlease(GroupCreatingWait):
    group_size = C.GROUP_SIZE


class Instructions(Page):
    pass


class Unconditional(Page):
    fields = dict(
        unconditional=IntegerField(
            label="Your unconditional contribution (0-20 tokens):",
            min=0,
            max=C.ENDOWMENT,
        ),
    )


class ContributionTable(Page):
    templatevars = {"levels": list(range(C.ENDOWMENT + 1))}

    @classmethod
    def fields(page, player: PlayerType) -> dict[str, Field]:
        return {
            f"cond_{i}": IntegerField(min=0, max=C.ENDOWMENT)
            for i in range(C.ENDOWMENT + 1)
        }


class Sync(SynchronizingWait):
    @classmethod
    def all_here(page, group: GroupType) -> None:
        players = list(group.players)

        table_idx = random.Random().randrange(C.GROUP_SIZE)

        for i, player in enumerate(players):
            player.is_table_player = i == table_idx

            if not player.is_table_player:
                player.contribution = player.unconditional

        others = [p for p in players if not p.is_table_player]
        avg = round(sum(p.unconditional for p in others) / len(others))

        table_player = players[table_idx]
        table_player.contribution = getattr(table_player, f"cond_{avg}")
        total = sum(p.contribution for p in players)

        for player in players:
            player.others_avg = avg
            player.total = total
            player.payoff = C.ENDOWMENT - player.contribution + C.MPCR * total


class Results(Page):
    pass


def pipeline(session: SessionType) -> list[dict[str, Any]]:
    rows = []

    for group in session.groups(app=__name__):
        for player in group.players:
            pd = player.within(app=__name__)
            row = {
                "session": session.name,
                "group": group.name,
                "uname": player.name,
                "member_id": player.member_id,
                "unconditional": pd.get("unconditional"),
                "is_table_player": pd.get("is_table_player"),
                "contribution": pd.get("contribution"),
                "others_avg": pd.get("others_avg"),
                "total": pd.get("total"),
                "payoff": pd.get("payoff"),
            }

            for i in range(C.ENDOWMENT + 1):
                row[f"cond_{i}"] = pd.get(f"cond_{i}")

            rows.append(row)

    return rows


page_order = [
    GroupPlease,
    Instructions,
    Unconditional,
    ContributionTable,
    Sync,
    Results,
]
