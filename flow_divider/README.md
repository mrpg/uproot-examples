# flow\_divider

Load this app using

```python
load_config(uproot_server, config="flow_divider", apps=["flow_divider"])
```

Create the destination rooms first. When creating the divider session, enter one
room name per line in its custom settings form. This stores a required
`room_names` list of strings, for example:

```json
{
    "room_names": ["shore-a", "shore-b"]
}
```

Players are sent through that list in round-robin order using their zero-based
ID: player 0 goes to `shore-a`, player 1 to `shore-b`, player 2 to `shore-a`,
and so on. The browser redirect uses a relative room URL, so it also works when
uproot is hosted in a subdirectory.

The destination rooms should use configs that do not include `flow_divider`, or
players will be redirected again.
