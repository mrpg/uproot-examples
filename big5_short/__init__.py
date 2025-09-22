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

DESCRIPTION = "20-item Big 5 questionnaire (Mini-IPIP) with scoring"
LANDING_PAGE = False


class C:
    # These items are adapted from https://ipip.ori.org/MiniIPIPKey.htm and
    # Donnellan, M. B., Oswald, F. L., Baird, B. M., & Lucas, R. E. (2006). The Mini-
    # IPIP scales: Tiny-yet-effective measures of the Big Five factors of personality.
    # Psychological Assessment, 18, 192-203.
    # - These items are in the public domain.
    # - The factor Intellect/Imagination has been relabelled to Openness.
    # - Item 15 has been changed from
    #       "Have difficulty understanding abstract ideas."
    #   to
    #       "Have no difficulty understanding abstract ideas."
    #   in order to provide a completely symmetrical scoring of Openness.

    # fmt: off
    ITEMS = {
        1: ("Am the life of the party.", "Extraversion", +1),
        2: ("Sympathize with others' feelings.", "Agreeableness", +1),
        3: ("Get chores done right away.", "Conscientiousness", +1),
        4: ("Have frequent mood swings.", "Neuroticism", +1),
        5: ("Have a vivid imagination.", "Openness", +1),
        6: ("Don't talk a lot.", "Extraversion", -1),
        7: ("Am not interested in other people's problems.", "Agreeableness", -1),
        8: ("Often forget to put things back in their proper place.", "Conscientiousness", -1),
        9: ("Am relaxed most of the time.", "Neuroticism", -1),
        10: ("Am not interested in abstract ideas.", "Openness", -1),
        11: ("Talk to a lot of different people at parties.", "Extraversion", +1),
        12: ("Feel others' emotions.", "Agreeableness", +1),
        13: ("Like order.", "Conscientiousness", +1),
        14: ("Get upset easily.", "Neuroticism", +1),
        15: ("Have no difficulty understanding abstract ideas.", "Openness", +1),  # <- CHANGED!
        16: ("Keep in the background.", "Extraversion", -1),
        17: ("Am not really interested in others.", "Agreeableness", -1),
        18: ("Make a mess of things.", "Conscientiousness", -1),
        19: ("Seldom feel blue.", "Neuroticism", -1),
        20: ("Do not have a good imagination.", "Openness", -1)
    }
    # fmt: on


class RandomlyOrderItems(NoshowPage):  # Note: NoshowPage hides a page
    @classmethod
    def after_always_once(page, player):
        itemorder = {}

        itemkeys = list(C.ITEMS.keys())
        random.shuffle(itemkeys)

        for round, itemkey in enumerate(itemkeys, 1):
            # Note: the keys in this dict must be strings because JSON supports only
            # str keys. The same limitation thus applies to uproot.
            itemorder[str(round)] = itemkey

        player.itemorder = itemorder


class Response(Page):
    @classmethod
    def context(page, player):
        itemhere = player.itemorder[str(player.round)]
        itemtext = f"I {C.ITEMS[itemhere][0].lower()}"

        return {"itemtext": itemtext}

    @classmethod
    def fields(page, player):
        itemhere = player.itemorder[str(player.round)]

        return {
            f"item{itemhere}": RadioField(
                label="How accurate is this statement as a description of you?",
                description="Describe yourself as you generally are now, not as you "
                "wish to be in the future. Describe yourself as you honestly see "
                "yourself, in relation to other people you know of the same gender "
                "as you are, and roughly your same age.",
                choices=[
                    (1, "Very Inaccurate"),
                    (2, "Moderately Inaccurate"),
                    (3, "Neither Accurate Nor Inaccurate"),
                    (4, "Moderately Accurate"),
                    (5, "Very Accurate"),
                ],
            ),
        }


class Score(NoshowPage):
    @classmethod
    def after_always_once(page, player):
        factors = {}

        # Collect data
        for k, item in C.ITEMS.items():
            _, factor, direction = item

            if factor not in factors:
                factors[factor] = []

            if direction == +1:
                factors[factor].append(getattr(player, f"item{k}"))
            else:
                # Reverse scoring: 5 -> 1, ..., 1 -> 5
                factors[factor].append(6 - getattr(player, f"item{k}"))

        # Calculate actual factor scores and assign them to player
        for factor, values in factors.items():
            setattr(player, factor, sum(values) / len(values))


class Results(Page):
    pass


page_order = [
    RandomlyOrderItems,
    Rounds(Response, n=len(C.ITEMS)),
    Score,
    Results,
]
