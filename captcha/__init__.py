# Docs are available at https://uproot.science/
# Examples are available at https://github.com/mrpg/uproot-examples
#
# This example app is under the 0BSD license. You can use it freely and build on it
# without any limitations and without any attribution. However, these two lines must be
# preserved in any uproot app (the license file is automatically installed in projects):
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt

from io import BytesIO

from fastapi import HTTPException
from fastapi.responses import Response
from PIL import Image, ImageDraw, ImageFont
from uproot.fields import *
from uproot.smithereens import *

DESCRIPTION = "Captcha image generated through api2()"
LANDING_PAGE = False


class C:
    """Change these values to customize the captcha."""

    CAPTCHA_LENGTH = 5
    CAPTCHA_CHARACTERS = "0123456789"

    PROMPT = "Enter the numbers shown in the image."
    ERROR_MESSAGE = "The numbers you entered do not match the image. Please try again."

    IMAGE_WIDTH = 180
    IMAGE_HEIGHT = 70
    BACKGROUND_COLOR = "white"
    FONT_SIZE = 38
    LINE_COUNT = 12
    TEXT_COLOR = (40, 55, 75)
    LINE_COLOR_MIN = 130
    LINE_COLOR_MAX = 220
    DIGIT_VERTICAL_JITTER = 4


def make_captcha_code():
    random = rng()

    return "".join(random.choice(C.CAPTCHA_CHARACTERS) for _ in range(C.CAPTCHA_LENGTH))


def new_player(player):
    player.captcha_code = make_captcha_code()
    player.captcha_attempts = 0
    player.captcha_solved = False


def captcha_png(code):
    from random import Random as PyRandom

    random = PyRandom(code)
    image = Image.new("RGB", (C.IMAGE_WIDTH, C.IMAGE_HEIGHT), C.BACKGROUND_COLOR)
    draw = ImageDraw.Draw(image)

    for _ in range(C.LINE_COUNT):
        start = (random.randint(0, C.IMAGE_WIDTH), random.randint(0, C.IMAGE_HEIGHT))
        end = (random.randint(0, C.IMAGE_WIDTH), random.randint(0, C.IMAGE_HEIGHT))
        color = tuple(
            random.randint(C.LINE_COLOR_MIN, C.LINE_COLOR_MAX) for _ in range(3)
        )
        draw.line([start, end], fill=color, width=1)

    try:
        font = ImageFont.load_default(size=C.FONT_SIZE)
    except TypeError:
        font = ImageFont.load_default()

    left, top, right, bottom = draw.textbbox((0, 0), code, font=font)
    text_width = right - left
    text_height = bottom - top
    x = (C.IMAGE_WIDTH - text_width) // 2
    y = (C.IMAGE_HEIGHT - text_height) // 2 - top

    for i, digit in enumerate(code):
        offset = i * (text_width // len(code))
        draw.text(
            (
                x + offset,
                y
                + random.randint(
                    -C.DIGIT_VERTICAL_JITTER,
                    C.DIGIT_VERTICAL_JITTER,
                ),
            ),
            digit,
            fill=C.TEXT_COLOR,
            font=font,
        )

    buffer = BytesIO()
    image.save(buffer, format="PNG")

    return buffer.getvalue()


class SolveCaptcha(Page):
    stealth_fields = ["captcha_answer"]

    @classmethod
    def fields(page, player):
        return {
            "captcha_answer": StringField(
                label=C.PROMPT,
                render_kw={
                    "autocomplete": "off",
                    "autofocus": True,
                    "class": "font-monospace w-auto",
                    "inputmode": "numeric",
                    "pattern": "[0-9]*",
                },
            ),
        }

    @classmethod
    def handle_stealth_fields(page, player, data):
        submitted = data.get("captcha_answer", "").strip()

        if submitted != player.captcha_code:
            player.captcha_attempts += 1

            return C.ERROR_MESSAGE

        player.captcha_solved = True

    @classmethod
    def may_proceed(page, player):
        return player.captcha_solved


class Results(Page):
    pass


async def api2(session, request):
    uname = request.query_params.get("uname")

    if uname not in {player.name for player in session.players}:
        raise HTTPException(status_code=404, detail="Unknown player")

    with Player(session.name, uname) as player:
        code = player.captcha_code

    return Response(
        content=captcha_png(code),
        media_type="image/png",
        headers={"Cache-Control": "no-store"},
    )


page_order = [
    SolveCaptcha,
    Results,
]
