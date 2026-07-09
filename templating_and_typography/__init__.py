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

DESCRIPTION = "Showcasing the template blocks and default fonts used by uproot."
LANDING_PAGE = False


# PAGES


class Templating(Page):
    """Showcase the template blocks provided by uproot"""

    @classmethod
    def timeout(page, player: PlayerType) -> float:
        return 1200


class Typography(Page):
    """Showcase the default fonts used by uproot if webfonts are loaded"""

    pass


class TypographyPNum(Page):
    """Showcase the default fonts used by uproot if webfonts are loaded"""

    pass


class TypographyNoWebfonts(Page):
    """Showcase the default fonts used by uproot if no webfonts are used"""

    pass


# PAGE ORDER


page_order = [
    Templating,
    Typography,
    TypographyPNum,
    TypographyNoWebfonts,
]
