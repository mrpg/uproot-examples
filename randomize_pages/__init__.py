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

DESCRIPTION = "Randomize pages"


class A(Page):
    pass


class B(Page):
    pass


class C(Page):
    pass


class D(Page):
    pass


class E(Page):
    pass


page_order = [
    Random(
        A,
        Bracket(
            B,
            C,
        ),
        D,
        E,
    ),
]
