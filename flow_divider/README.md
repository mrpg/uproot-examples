# flow\_divider

Load this app using

```python
load_config(uproot_server, config="flow_divider", apps=["flow_divider"])
```

Create the destination rooms first. The custom settings form shows the available
rooms; enter one room name per line in the desired allocation order. This stores
a required `room_names` list of strings, for example:

```json
{
    "room_names": ["shore-a", "shore-b"]
}
```

Players are sent through that list in round-robin order using their zero-based
ID: player 0 goes to `shore-a`, player 1 to `shore-b`, player 2 to `shore-a`,
and so on. The browser redirect uses a relative room URL, so it also works when
uproot is hosted in a subdirectory.

The app validates the settings again, against current server state, immediately
before uproot creates the session. This also protects sessions created through
the REST API, automatic room creation, the quick-session CLI, or direct framework
calls; missing rooms prevent the session from being created.

The room lookup is only one use of uproot’s generic hooks:
`admin_settings_context()` returns values for `AdminSettings.html`, and
the synchronous `validate_session_settings()` callback can reject any invalid
settings before creation.

When uproot runs as a public demo, the settings form does not expose room names.

The destination rooms should use configs that do not include `flow_divider`, or
players will be redirected again.
