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

DESCRIPTION = "Quiz/comprehension check"
LANDING_PAGE = False

QUIZ = [
    (
        "Question 1",
        [
            "Answer 1",  # The CORRECT answer must always be placed first - will be randomized
            "Answer 2",
            "Answer 3",
        ],
    ),
    (
        "Question 2",
        [
            "Answer 1",  # The CORRECT answer must always be placed first - will be randomized
            "Answer 2",
            "Answer 3",
        ],
    ),
    (
        "Question 3",
        [
            "Answer 1",  # The CORRECT answer must always be placed first - will be randomized
            "Answer 2",
            "Answer 3",
        ],
    ),
]


def new_player(player):
    player.quiz_bad_attempts = 0


def shuffled(iterable, *, seed=None):
    from random import Random

    result = list(iterable)
    Random(seed).shuffle(result)

    return result


class C:
    pass


class Quiz(Page):
    stealth_fields = [f"q{i}" for i, _ in enumerate(QUIZ)]

    @classmethod
    async def fields(page, player):
        from uproot.types import sha256

        return {
            f"q{i}": RadioField(
                label=question,
                choices=[
                    (sha256(answer), answer)
                    for answer in shuffled(
                        answers,
                        seed=player.name + f"q{i}",
                    )
                ],
            )
            for i, (question, answers) in enumerate(QUIZ)
        }

    @classmethod
    async def handle_stealth_fields(page, player, **responses):
        # This method was written in a highly verbose style so that
        # you can add custom logic by adapting the algorithm.

        from uproot.types import sha256

        mistakes = 0

        for i, (question, answers) in enumerate(QUIZ):
            # Iterate through each question in QUIZ
            correct = sha256(answers[0])  # Internal representation of correct answer

            if responses[f"q{i}"] != correct:
                # This response was not correct
                mistakes += 1  # Add 1 to local mistakes counter

        if mistakes > 0:
            # At least one response was not correct
            player.quiz_bad_attempts += 1  # Add 1 to player's own counter

            return "Please try again."


page_order = [
    Quiz,
]
