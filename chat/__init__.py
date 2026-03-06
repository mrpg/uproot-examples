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

    # Optionally, you can register a callback that fires whenever a message
    # is sent in this chat. This is not required for the chat to work — it is
    # just a way to react to messages in your experiment code (e.g., for
    # logging, triggering game logic, etc.).
    chat.on_message(session.chat, on_chat_message)


# This is just an example of how on_message could be used; it is by no means
# mandatory or necessary for a working chat. You can safely remove it.
def on_chat_message(chat, player, message):
    print(f"Chat message from {player.name}: {message}")


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
