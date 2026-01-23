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

DESCRIPTION = "Timeout that spans multiple pages"
LANDING_PAGE = False


class InitializeTimeout(NoshowPage):
    @classmethod
    def after_always_once(page, player):
        from time import time

        player.custom_timeout_until = time() + C.TOTAL_TIMEOUT
        player.failed = False


class PageWithCustomTimeout(Page):
    @classmethod
    def timeout(page, player):
        from time import time

        return max(0, player.custom_timeout_until - time())

    @classmethod
    def timeout_reached(page, player):
        if not player.failed:
            player.failed = True


class C:
    TOTAL_TIMEOUT = 15.0


class Hello(Page):
    pass


class A(PageWithCustomTimeout):
    pass


class B(PageWithCustomTimeout):
    pass


class C_(PageWithCustomTimeout):
    pass


class D(PageWithCustomTimeout):
    pass


class Bye(Page):
    pass


page_order = [
    Hello,
    InitializeTimeout,
    A,
    B,
    C_,
    D,
    Bye,
]
