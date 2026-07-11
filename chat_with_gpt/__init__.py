# Docs are available at https://uproot.science/
# Examples are available at https://github.com/mrpg/uproot-examples
#
# This example app is under the 0BSD license. You can use it freely and build on it
# without any limitations and without any attribution. However, these two lines must be
# preserved in any uproot app (the license file is automatically installed in projects):
#
# Third-party dependencies:
# - uproot: LGPL v3+, see ../uproot_license.txt

import openai
from uproot.fields import *
from uproot.smithereens import *

DESCRIPTION = "Chat with GPT"


async def respond(chat_mid: ModelIdentifier) -> None:
    from openai.types.responses import ResponseInputParam

    messages: ResponseInputParam = []
    for _, _, msg in chat.messages(chat_mid):
        if msg.sender == "GPT":
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

    async with openai.AsyncOpenAI() as client:
        response = await client.responses.create(
            model="gpt-5.5",
            max_output_tokens=2048,
            instructions=system,
            input=messages,
        )

    response_text = response.output_text
    msg_id = chat.add_message(chat_mid, "GPT", response_text)

    await chat.notify(chat_mid, msg_id, "GPT", None, response_text)


async def on_chat_message(
    chat: ModelIdentifier,
    player: None | PlayerType,
    message: str,
) -> None:
    if player is None:
        return

    spawn(respond(chat))


def new_player(player: PlayerType) -> None:
    player.my_chat = chat.create(player.session)
    chat.add_player(player.my_chat, player)
    chat.on_message(player.my_chat, on_chat_message)


class Chat(Page):
    pass


page_order = [
    Chat,
]
