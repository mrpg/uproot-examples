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

DESCRIPTION = "Stroop task"
LANDING_PAGE = False
APP_NAME = __name__


class C:
    NUM_TRIALS = 12
    COLORS = ["red", "green", "blue", "yellow"]


class Context(PlayerContext):
    @property
    def results(self):
        trials = [
            self.player.within(app=APP_NAME, round=round_num)
            for round_num in range(1, C.NUM_TRIALS + 1)
        ]
        completed = [trial for trial in trials if trial.get("response") is not None]
        correct = [trial for trial in completed if trial.get("correct")]
        congruent = [trial for trial in correct if trial.get("congruent")]
        incongruent = [trial for trial in correct if not trial.get("congruent")]
        congruent_rt = mean_rt(congruent)
        incongruent_rt = mean_rt(incongruent)

        return dict(
            total_trials=len(completed),
            correct_count=len(correct),
            accuracy=round(percent(len(correct), len(completed)), 1),
            mean_rt=mean_rt(correct),
            congruent_rt=congruent_rt,
            incongruent_rt=incongruent_rt,
            stroop_effect=round(incongruent_rt - congruent_rt, 1),
        )


def new_player(player):
    player.trial_sequence = make_trials()


def make_trials():
    trials = []
    random = rng()

    for _ in range(C.NUM_TRIALS // 2):
        color = random.choice(C.COLORS)
        trials.append([color.upper(), color, True])

    for _ in range(C.NUM_TRIALS - len(trials)):
        word_color = random.choice(C.COLORS)
        ink_color = random.choice([color for color in C.COLORS if color != word_color])
        trials.append([word_color.upper(), ink_color, False])

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
    def before_once(page, player):
        player.word, player.ink_color, player.congruent = player.trial_sequence[
            player.round - 1
        ]

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
    Rounds(Stroop, n=C.NUM_TRIALS),
    Results,
]
