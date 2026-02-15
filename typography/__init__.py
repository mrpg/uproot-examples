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

DESCRIPTION = (
    "Showcase the default fonts used by uproot if web fonts are loaded or not."
)
LANDING_PAGE = False


# PAGES


class Typography(Page):
    """Showcase the default fonts used by uproot if webfonts are loaded"""

    pass


class TypographyNoWebfonts(Page):
    """Showcase the default fonts used by uproot if no webfonts are used"""

    pass


# PAGE ORDER


page_order = [
    Typography,
    TypographyNoWebfonts,
]
