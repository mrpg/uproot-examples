# Message Board

Load this app by adding the following to your `main.py`:

```python
load_config(uproot_server, config="message_board", apps=["message_board"])
```

Participants submit short text messages that are collected in a shared model. The **AdminDigest** shows all messages as cards on a projection screen.

## Session settings

| Key              | Type | Default | Description                                              |
|------------------|------|---------|----------------------------------------------------------|
| `show_to_others` | bool | `false` | Whether participants see everyone's messages on their own screen. When `false`, participants only see their own submissions; the full board is visible only on the AdminDigest. |

## Adapting the data type

The `Post` model stores a `body: str`. To collect numbers instead, change the model field to `score: int` (or `value: float`, etc.), adjust the validation in `add_post`, and update the HTML input accordingly.

## Recipe: Forward posts to your phone via XMPP

You can get every post as a chat message on your phone, for example to monitor questions during a lecture. The key ingredients are:

1. **A client that lives in uproot's event loop.** There is no separate process. Posts are queued, and a background task sends them once the XMPP session is up. Participants therefore never wait for XMPP.
2. **uproot's lifespan hook.** `uproot.deployment.lifespan_start` runs once the server's event loop is up, so the connection is ready before the first post arrives.
3. **One line in `add_post`** that hands the post to the client.

Install [slixmpp](https://codeberg.org/poezio/slixmpp) (`uv add slixmpp`), then put this in `xmpp_notify.py` next to `main.py`:

```python
import asyncio
import os

import slixmpp

RECIPIENT = slixmpp.JID("you@example.org")

_client: "Notifier | None" = None
_loop: asyncio.AbstractEventLoop | None = None
_tasks: set[asyncio.Task[None]] = set()


class Notifier(slixmpp.ClientXMPP):
    def __init__(self, jid: str, password: str) -> None:
        super().__init__(jid, password)

        self.outbox: asyncio.Queue[str] = asyncio.Queue()
        self.ready = asyncio.Event()
        self.stopping = False

        self.register_plugin("xep_0199", {"keepalive": True, "interval": 60})
        self.add_event_handler("session_start", self.on_session_start)
        self.add_event_handler("disconnected", self.on_disconnected)

    async def on_session_start(self, _: object) -> None:
        self.send_presence()
        await self.get_roster()

        # Ask once to become contacts, so servers that block strangers deliver
        if self.client_roster[RECIPIENT]["subscription"] not in ("to", "both"):
            self.send_presence_subscription(pto=RECIPIENT)

        self.ready.set()

    def on_disconnected(self, _: object) -> None:
        self.ready.clear()

        if not self.stopping:
            self.connect()  # Reconnect; queued posts are sent afterwards

    async def deliver(self) -> None:
        while True:
            body = await self.outbox.get()
            await self.ready.wait()
            self.send_message(mto=RECIPIENT, mbody=body, mtype="chat")


async def start() -> None:
    global _client, _loop

    _loop = asyncio.get_running_loop()
    _client = Notifier(os.environ["XMPP_USER"], os.environ["XMPP_PASSWORD"])
    _client.connect()
    _tasks.add(_loop.create_task(_client.deliver()))


async def stop() -> None:
    if _client is not None:
        _client.stopping = True
        await asyncio.wait_for(_client.disconnect(wait=1), timeout=3)


def forward(text: str) -> None:
    """Queue text for delivery. Never blocks; safe to call from any thread."""
    if _client is not None and _loop is not None:
        _loop.call_soon_threadsafe(_client.outbox.put_nowait, text)
```

In `main.py`, before `cli()`, wrap uproot's lifespan hooks:

```python
import xmpp_notify

_lifespan_start, _lifespan_stop = upd.lifespan_start, upd.lifespan_stop


async def lifespan_start(*args, **kwargs):
    await _lifespan_start(*args, **kwargs)
    await xmpp_notify.start()


async def lifespan_stop(*args, **kwargs):
    await xmpp_notify.stop()
    await _lifespan_stop(*args, **kwargs)


upd.lifespan_start, upd.lifespan_stop = lifespan_start, lifespan_stop
```

Wrap the original hooks rather than replacing them: `lifespan_stop` closes the database. Finally, in `add_post`, after `um.add_entry(...)`:

```python
from xmpp_notify import forward  # at the top of __init__.py

forward(f"Player {player.id}: {body}")
```

Use a dedicated XMPP account for the sender and put `XMPP_USER=…` and `XMPP_PASSWORD=…` in your project's `.env`, which uproot loads automatically. Keep `.env` out of version control. Your XMPP client already timestamps each message, and `player.id` matches the player number on the AdminDigest. The same pattern works for any app: call `forward()` wherever something happens that you want to hear about.
