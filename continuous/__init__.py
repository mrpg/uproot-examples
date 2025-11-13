# Docs are available at https://uproot.science/
# Examples are available at https://github.com/mrpg/uproot-examples
#
# This example app is under the 0BSD license. You can use it freely and build on it
# without any limitations and without any attribution. However, these two lines must be
# preserved in any uproot app (the license file is automatically installed in projects):
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt

import asyncio

from uproot.fields import *
from uproot.smithereens import *
from uproot.storage import Admin, Session

DESCRIPTION = "Do something in intervals"
LANDING_PAGE = False


async def increment_state(sname):
    while True:
        with Session(sname) as session:
            session.my_state += 1

            send_to(players(session), data=session.my_state)

        await asyncio.sleep(1)


async def restart():
    with Admin() as admin:
        for sname in admin.sessions:
            with Session(sname) as session:
                if session.get("my_state") is not None:
                    asyncio.create_task(increment_state(sname))


class C:
    pass


class EnsureBackgroundTask(NoshowPage):
    @classmethod
    async def after_always_once(page, player):
        if player.session.get("my_state") is None:
            player.session.my_state = 0
            asyncio.create_task(increment_state(player.session.name))


class FirstPage(Page):
    pass


page_order = [
    EnsureBackgroundTask,
    FirstPage,
]
