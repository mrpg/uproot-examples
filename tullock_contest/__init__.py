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

DESCRIPTION = "Tullock rent-seeking contest (Tullock, 1980)"
SUGGESTED_MULTIPLE = 2
APP_NAME = __name__


class C:
    GROUP_SIZE = 2
    ENDOWMENT = 20
    PRIZE = 20


class GroupPlease(GroupCreatingWait):
    group_size = C.GROUP_SIZE


class Invest(Page):
    fields = dict(
        spend=IntegerField(
            label="How much do you invest in the contest?",
            addon_start="$",
            min=0,
            max=C.ENDOWMENT,
            render_kw={"style": "flex: unset !important; width: 6rem !important;"},
        ),
    )


class Sync(SynchronizingWait):
    @classmethod
    def all_here(page, group):
        players = list(group.players)
        total = sum(p.spend for p in players)

        if total > 0:
            winner = rng().choices(players, weights=[p.spend for p in players])[0]
        else:
            winner = None

        for player in players:
            player.total_spend = total
            player.win_probability = player.spend / total if total else 0.0
            player.winner = player is winner
            player.payoff = cu(C.ENDOWMENT - player.spend) + (
                cu(C.PRIZE) if player.winner else cu(0)
            )


class Results(Page):
    pass


def pipeline(session):
    rows = []

    for group, players in contest_groups(session):
        for member_id, player in enumerate(players):
            player_data = player.within(app=APP_NAME)

            rows.append(
                {
                    "session": session.name,
                    "group": group.name,
                    "uname": player.name,
                    "member_id": member_id,
                    "spend": player_data.get("spend"),
                    "total_spend": player_data.get("total_spend"),
                    "win_probability": player_data.get("win_probability"),
                    "winner": player_data.get("winner"),
                    "payoff": player_data.get("payoff"),
                }
            )

    return rows


def contest_groups(session):
    groups = []

    for group in session.groups:
        players = group.players

        if len(players) == C.GROUP_SIZE and is_app_group(group, players):
            groups.append((group, players))

    return groups


def is_app_group(group, players):
    with group:
        if group.get("app") == APP_NAME:
            return True

        gid = group.gid

    return all(
        player.within(app=APP_NAME).get("_uproot_group") == gid for player in players
    )


page_order = [
    GroupPlease,
    Invest,
    Sync,
    Results,
]
