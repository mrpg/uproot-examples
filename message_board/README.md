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
