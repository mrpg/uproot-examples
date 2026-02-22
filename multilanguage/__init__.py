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
from uproot.i18n import load as load_all
from uproot.smithereens import *

DESCRIPTION = "App with language switcher"
LANDING_PAGE = False

# This loads strings for all languages
load_all("multilanguage/")


def new_player(player):
    player.language = "en"


def language(player):
    return player.language


class C:
    pass


class SelectLanguage(Page):
    fields = dict(
        language=RadioField(
            choices=[
                ("de", "Deutsch"),
                ("en", "English"),
                ("es", "Español"),
                ("fr", "Français"),
                ("he", "עברית"),
                ("hi", "हिन्दी"),
                ("ja", "日本語"),
                ("pt", "Português"),
                ("sw", "Kiswahili"),
                ("yue", "廣東話"),
            ],
        )
    )


class Hello(Page):
    allow_back = True


page_order = [
    SelectLanguage,
    Hello,
]
