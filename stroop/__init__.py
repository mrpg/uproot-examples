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

DESCRIPTION = "Stroop color-word test (Stroop, 1935) in a version adapted from Gerhardt et al. (2017)"
LANDING_PAGE = False


class C:
    NUM_TRIALS = 15
    NUM_TRIALS_NEUTRAL = 10
    COLORS = ["blue", "green", "red", "yellow"]


class Context(PlayerContext):
    @property
    def results(self):
        trials = [
            self.player.within(app=__name__, round=round_num)
            for round_num in range(1, C.NUM_TRIALS + C.NUM_TRIALS_NEUTRAL + 1)
        ]
        completed = [trial for trial in trials if trial.get("response") is not None]
        correct = [trial for trial in completed if trial.get("correct")]
        congruent = [trial for trial in completed if trial.get("type") == "congruent"]
        congruent_rt = mean_rt(congruent)
        congruent_correct = [trial for trial in congruent if trial.get("correct")]
        congruent_correct_rt = mean_rt(congruent_correct)
        congruent_incorrect = [trial for trial in congruent if not trial.get("correct")]
        congruent_incorrect_rt = mean_rt(congruent_incorrect)
        incongruent = [
            trial for trial in completed if trial.get("type") == "incongruent"
        ]
        incongruent_rt = mean_rt(incongruent)
        incongruent_correct = [trial for trial in incongruent if trial.get("correct")]
        incongruent_correct_rt = mean_rt(incongruent_correct)
        incongruent_incorrect = [
            trial for trial in incongruent if not trial.get("correct")
        ]
        incongruent_incorrect_rt = mean_rt(incongruent_incorrect)
        neutral = [trial for trial in completed if trial.get("type") == "neutral"]
        neutral_rt = mean_rt(neutral)
        neutral_correct = [trial for trial in neutral if trial.get("correct")]
        neutral_incorrect = [trial for trial in neutral if not trial.get("correct")]
        neutral_correct_rt = mean_rt(neutral_correct)
        neutral_incorrect_rt = mean_rt(neutral_incorrect)

        return dict(
            total_trials=len(completed),
            correct_count=len(correct),
            mean_rt=mean_rt(completed),
            congruent_trials=len(congruent),
            congruent_correct_count=len(congruent_correct),
            congruent_incorrect_count=len(congruent_incorrect),
            congruent_accuracy=round(
                percent(len(congruent_correct), len(congruent)), 1
            ),
            congruent_rt=congruent_rt,
            congruent_correct_rt=congruent_correct_rt,
            congruent_incorrect_rt=congruent_incorrect_rt,
            incongruent_trials=len(incongruent),
            incongruent_correct_count=len(incongruent_correct),
            incongruent_incorrect_count=len(incongruent_incorrect),
            incongruent_accuracy=round(
                percent(len(incongruent_correct), len(incongruent)), 1
            ),
            incongruent_rt=incongruent_rt,
            incongruent_correct_rt=incongruent_correct_rt,
            incongruent_incorrect_rt=incongruent_incorrect_rt,
            delta_accuracy=round(
                percent(len(congruent_correct), len(congruent))
                - percent(len(incongruent_correct), len(incongruent)),
                1,
            ),
            stroop_effect=(
                round(incongruent_correct_rt - congruent_correct_rt, 1)
                if congruent_correct and incongruent_correct
                else None
            ),
            neutral_trials=len(neutral),
            neutral_correct_count=len(neutral_correct),
            neutral_incorrect_count=len(neutral_incorrect),
            neutral_accuracy=round(percent(len(neutral_correct), len(neutral)), 1),
            neutral_rt=neutral_rt,
            neutral_correct_rt=neutral_correct_rt,
            neutral_incorrect_rt=neutral_incorrect_rt,
        )


def new_player(player):
    player.trial_sequence = make_trials()


def make_trials():
    import math

    trials = []
    random = rng()

    # Let 40%–60% of all trials be congruent trials
    num_congruent_trials = random.randint(
        math.floor(0.8 * C.NUM_TRIALS // 2), math.ceil(1.2 * C.NUM_TRIALS // 2)
    )

    for _ in range(num_congruent_trials):
        color = random.choice(C.COLORS)
        order = random.sample(C.COLORS, len(C.COLORS))
        trials.append([color, color, "congruent", order])

    for _ in range(C.NUM_TRIALS - len(trials)):
        word_color = random.choice(C.COLORS)
        ink_color = random.choice([color for color in C.COLORS if color != word_color])
        order = random.sample(C.COLORS, len(C.COLORS))
        trials.append([word_color, ink_color, "incongruent", order])

    for _ in range(C.NUM_TRIALS_NEUTRAL):
        word_color = safe("<span style='font-size: 125%;'>&bull;</span>")
        ink_color = random.choice(C.COLORS)
        order = random.sample(C.COLORS, len(C.COLORS))
        trials.append([word_color, ink_color, "neutral", order])

    random.shuffle(trials)

    return trials


class Instructions(Page):
    pass


class Stroop(Page):
    fields = dict(
        response=StringField(render_kw={"type": "hidden"}),
        reaction_time_ms=DecimalField(render_kw={"type": "hidden"}),
    )

    @classmethod
    def templatevars(page, player):
        player.word, player.ink_color, player.type, player.button_order = (
            player.trial_sequence[player.round - 1]
        )

        if player.ink_color == "blue":
            player.hex_color = "#0066cc"  # "#0a58ca"
        elif player.ink_color == "green":
            player.hex_color = "#339966"  # "#198754"
        elif player.ink_color == "red":
            player.hex_color = "#cc0033"  # "#b02a37"
        elif player.ink_color == "yellow":
            player.hex_color = "#ffcc00"  # "#ffc107"

    @classmethod
    def validate(page, player, data):
        if data["response"] not in C.COLORS:
            return "Please choose one of the colors."

        if data["reaction_time_ms"] < 0:
            return "Reaction time must be non-negative."

        return []

    @classmethod
    def before_form_save(page, player, data):
        player.correct = data["response"] == player.ink_color


class Results(Page):
    pass


def percent(numerator, denominator):
    if denominator == 0:
        return 0

    return 100 * numerator / denominator


def mean_rt(trials):
    reaction_times = [float(trial.get("reaction_time_ms")) for trial in trials]

    if not reaction_times:
        return 0

    return round(sum(reaction_times) / len(reaction_times), 1)


page_order = [
    Instructions,
    Rounds(Stroop, n=C.NUM_TRIALS + C.NUM_TRIALS_NEUTRAL),
    Results,
]
