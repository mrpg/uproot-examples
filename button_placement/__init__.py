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

DESCRIPTION = "Custom button placement with button_next() and button_back()"


class Default(Page):
    """No manual button placement — default buttons render as usual."""


class Styled(Page):
    """Custom classes and inline styles on the Next button."""


class Centered(Page):
    """Both buttons placed inside a centered container."""

    allow_back = True


class Relabeled(Page):
    """Custom button labels via the label= parameter."""


class TimeoutDisplay(Page):
    """Custom timeout placement with timeout_box() and timeout()."""

    timeout = 90


class Finale(Page):
    """Buttons at the top of the page, not the bottom."""

    allow_back = True


page_order = [
    Default,
    Styled,
    Centered,
    Relabeled,
    TimeoutDisplay,
    Finale,
]
