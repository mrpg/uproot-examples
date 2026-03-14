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

DESCRIPTION = "Chat with Claude"


async def _respond(chat_mid):
    import anthropic

    messages = []
    for _, _, msg in chat.messages(chat_mid):
        if msg.sender == "Claude":
            messages.append({"role": "assistant", "content": msg.text})
        else:
            messages.append({"role": "user", "content": msg.text})

    system = (
        "You are a helpful assistant embedded in a research study. "
        "Be concise, friendly, and helpful. "
        "Always respond in full, well-formed sentences. "
        "Do not use Markdown, bullet points, numbered lists, code blocks, or any special formatting. "
        "Write in plain prose only. "
        "You must refuse any request that is harmful, unethical, illegal, or inappropriate, "
        "including but not limited to: generating malware or exploits, "
        "producing hateful or violent content, facilitating deception or fraud, "
        "providing personal data about real individuals, "
        "or bypassing safety guidelines. "
        "If a request is problematic, briefly explain that you cannot help with it "
        "and offer to assist with something else."
    )

    async with anthropic.AsyncAnthropic() as client:
        response = await client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            system=system,
            messages=messages,
        )

    response_text = response.content[0].text
    msg_id = chat.add_message(chat_mid, "Claude", response_text)

    await chat.notify(chat_mid, msg_id, "Claude", None, response_text)


async def on_chat_message(chat, player, message):
    if player is None:
        return

    asyncio.create_task(_respond(chat))


def new_player(player):
    player.my_chat = chat.create(player.session)
    chat.add_player(player.my_chat, player)
    chat.on_message(player.my_chat, on_chat_message)


class Chat(Page):
    pass


page_order = [
    Chat,
]
