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

DESCRIPTION = "A session-level chat"


def new_session(session):
    session.chat = chat.create(session)


class ChatHere(Page):
    @classmethod
    async def before_once(page, player):
        chat.add_player(
            player.session.chat,
            player,
            pseudonym=f"Player {player.id}",
        )  # Pseudonym is optional


page_order = [
    ChatHere,
]
