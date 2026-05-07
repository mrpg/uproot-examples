# Docs are available at https://uproot.science/
# Examples are available at https://github.com/mrpg/uproot-examples
#
# This example app is under the 0BSD license. You can use it freely and build on it
# without any limitations and without any attribution. However, these two lines must be
# preserved in any uproot app (the license file is automatically installed in projects):
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt

from uproot.smithereens import *

DESCRIPTION = "Total stranger matching with manually created groups"


class C:
    ROUNDS = 3
    GROUP_SIZE = 2


SUGGESTED_MULTIPLE = C.GROUP_SIZE * 2


def new_player(player):
    player.partners = []
    player.partner_history = []


def find_stranger_groups(players, group_size, used_pairs):
    n = len(players)
    num_groups = n // group_size
    leftover = n % group_size

    if num_groups == 0:
        return [[p] for p in players]

    solution = None

    def backtrack(idx, groups, sit_out):
        nonlocal solution

        if idx == n:
            if len(sit_out) == leftover:
                solution = [list(g) for g in groups] + [[p] for p in sit_out]
                return True
            return False

        player = players[idx]
        seen_empty = False

        for group in groups:
            if len(group) >= group_size:
                continue

            if not group:
                if seen_empty:
                    continue  # empty groups are interchangeable

                seen_empty = True

            if all(frozenset((player.name, m.name)) not in used_pairs for m in group):
                group.append(player)

                if backtrack(idx + 1, groups, sit_out):
                    return True

                group.pop()

        if len(sit_out) < leftover:
            sit_out.append(player)

            if backtrack(idx + 1, groups, sit_out):
                return True

            sit_out.pop()

        return False

    backtrack(0, [[] for _ in range(num_groups)], [])

    if solution is not None:
        return solution

    return [[p] for p in players]


class MatchStrangers(SynchronizingWait):
    synchronize = "session"

    @classmethod
    def all_here(page, session):
        all_players = list(session.players)
        rng().shuffle(all_players)

        used_pairs = set()

        for player in all_players:
            with player:
                for round_partners in player.partner_history:
                    for name in round_partners:
                        used_pairs.add(frozenset((player.name, name)))

        groups = find_stranger_groups(all_players, C.GROUP_SIZE, used_pairs)
        create_groups(session, groups, overwrite=True)

        for group in groups:
            names = sorted(p.name for p in group)

            for player in group:
                with player:
                    partners = [n for n in names if n != player.name]
                    player.partners = partners

                    history = list(player.partner_history)
                    history.append(partners)
                    player.partner_history = history


class ShowMatch(Page):
    @classmethod
    def templatevars(page, player):
        return dict(
            group_members=sorted(player.group.players, key=lambda p: p.name),
            total_rounds=C.ROUNDS,
        )


class Summary(Page):
    pass


page_order = [
    Rounds(
        MatchStrangers,
        ShowMatch,
        n=C.ROUNDS,
    ),
    Summary,
]
