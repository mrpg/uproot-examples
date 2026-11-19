# treatments\_balanced

Load this app using

```python
load_config(uproot_server, config="treatments_balanced", apps=["treatments_balanced"])
```

This example assigns treatments so that they stay balanced within a session.
Assigning each participant a treatment at random, as in the example
`treatments`, can leave arms unequal when there are few participants, as in a
pilot. Here, each participant instead gets the treatment that the fewest
players in the session have so far.

To balance the order of pages rather than treatments, see the example
`balanced_page_order`.

## Breaking ties at random

When several treatments have the fewest players, the app takes the first of
them. Participants therefore cycle through `TREATMENTS` in the same sequence in
every session: the first participant in each session always gets the first
treatment, and so on. If arrival order is related to who your participants are
(for example, keen participants arrive first), treatment is then confounded
with arrival rank. To pick at random among the tied treatments, replace

```python
TREATMENTS,
```

in the call to `min` with

```python
rng().sample(TREATMENTS, len(TREATMENTS)),
```

## Counting only some players

To count only some players, add conditions to the list comprehension in
`AssignTreatment`. For example, to leave out dropouts, change its condition to

```python
if p.get("treatment") is not None and not p.get("dropout")
```

This requires a `dropout` field. See the section on dropouts in the README of
`balanced_page_order` for how to set it up. To count only players who
contributed more than 10, as in the example `public_goods_game`, use

```python
if p.get("treatment") is not None and p.get("contribution", 0) > 10
```

Use `p.get("field")` in these conditions, not `p.field` or
`player.session.players.filter(_.field == ...)`. A session can contain players
who have not started yet. They do not have your fields, so `p.field` and
`filter()` raise an `AttributeError`, while `p.get("field")` returns `None`.
