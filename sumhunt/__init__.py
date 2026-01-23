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
from itertools import combinations
from sys import stderr

from uproot.fields import *
from uproot.smithereens import *

DESCRIPTION = "Real effort task about finding sums in matrices"
LANDING_PAGE = False


class C:
    NUMMIN = 10
    NUMMAX = 99
    GRID = (3, 3)
    TARGET = 100
    TERMS = 2
    SEED = 0x1337  # Every player sees the same matrices over time

    __export__ = ["GRID", "TERMS"]


def new_player(player):
    player.matrix = None
    player.solutions = 0
    player.rng = random.Random(C.SEED)


def all_unique(values: list[int]) -> bool:
    return len(values) == len(set(values))


def count_combinations_with_sum(
    nums: list[int],
    k: int,
    target: int,
) -> int:
    return sum(1 for combo in combinations(nums, k) if sum(combo) == target)


def random_k_sum(
    rng: random.Random,
    k: int,
    target: int,
    min_val: int = 0,
    max_val: int | None = None,
) -> list[int]:
    if max_val is None:
        max_val = target - (k - 1) * min_val

    if k * min_val > target or k * max_val < target:
        raise ValueError("No valid combination exists")

    result = []
    remaining = target

    for i in range(k - 1):
        remaining_count = k - i
        lo = max(min_val, remaining - (remaining_count - 1) * max_val)
        hi = min(max_val, remaining - (remaining_count - 1) * min_val)
        val = rng.randint(lo, hi)
        result.append(val)
        remaining -= val

    result.append(remaining)

    return result


def generate_matrix(
    rng: random.Random,
    length: int,
    k: int,
    target: int,
    min_val: int = 0,
    max_val: int | None = None,
) -> list[int]:
    while True:
        solution = random_k_sum(rng, k, target, min_val, max_val)
        matrix = solution + [rng.randint(min_val, max_val) for _ in range(length - k)]

        rng.shuffle(matrix)

        if all_unique(matrix) and count_combinations_with_sum(matrix, k, target) == 1:
            print("New matrix:", matrix, file=stderr)
            print("With solution:", solution, file=stderr)

            return matrix


class Sumhunt(Page):
    timeout = 120

    @live
    async def get_matrix(page, player):
        if player.matrix is None:
            player.matrix = generate_matrix(
                player.rng,
                C.GRID[0] * C.GRID[1],
                C.TERMS,
                C.TARGET,
                C.NUMMIN,
                C.NUMMAX,
            )

        return player.matrix

    @live
    async def propose_solution(page, player, solution: list[int]):
        if (
            player.matrix is not None
            and len(solution) == C.TERMS
            and all(x in player.matrix for x in solution)
            and sum(solution) == C.TARGET
        ):
            player.solutions += 1
            player.matrix = generate_matrix(
                player.rng,
                C.GRID[0] * C.GRID[1],
                C.TERMS,
                C.TARGET,
                C.NUMMIN,
                C.NUMMAX,
            )

            return True

        return False


page_order = [
    Sumhunt,
]
