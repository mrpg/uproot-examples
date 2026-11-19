# balanced\_page\_order

Load this app using

```python
load_config(uproot_server, config="balanced_page_order", apps=["balanced_page_order"])
```

This example shows pages in an order that is balanced across participants.
`RandomOrder` shuffles pages independently for each participant. With few
participants, as in a pilot, some orders may then be much more common than
others. This app instead gives each new participant the order that is most
underrepresented so far in the session.

`page_order` is a function here, not a list. uproot calls it once for each
participant, when they start. It counts the orders already assigned in the
session, stores the index of the chosen order in `player.order`, and returns
the pages in that order. `ORDERS` holds every order of `PAGES`. `WEIGHTS`
sets the target share of each order. The default is equal shares.

When several orders are equally underrepresented, the app chooses at random
among them. `rng().sample` shuffles the candidates before `max`, so each tied
order is equally likely. This preserves balance while avoiding a fixed order
sequence across sessions.

## Variants

Each variant below adapts the assignment in `__init__.py`.

### Leaving out dropouts

Participants who drop out still count, so their orders end up underrepresented
among those who finish. To let later arrivals take their place, watch for
dropouts as in the example `dropouts`, and count only players who have not
dropped out:

```python
def new_player(player: PlayerType) -> None:
    player.dropout = False
    watch_for_dropout(player, handle_dropout)


async def handle_dropout(player: PlayerType) -> None:
    player.dropout = True
    move_to_end(player)
```

In `page_order`, change the condition of the list comprehension to

```python
if p.get("order") is not None and not p.get("dropout")
```

`move_to_end` sends a dropout to the end of the experiment. Without it, they
could come back and finish. They would still be marked as a dropout, so they
would not count, and their order would be overrepresented among those who
finish.

Call `stop_watching_for_dropout(player)` once a participant is past `PAGES`, for
example in `before_once` of `End`. Otherwise, a participant who leaves on the
last page counts as a dropout and their order is handed out again.

### Balancing within treatments

To balance orders within each treatment, assign `player.treatment` in
`new_player`. `new_player` runs before `page_order`, so the treatment is known
when the order is chosen. For balanced treatments, move the counting from
`AssignTreatment` in the example `treatments_balanced` into `new_player`:

```python
TREATMENTS = [1, 2]


def new_player(player: PlayerType) -> None:
    counts = Counter(
        p.get("treatment")
        for p in player.session.players
        if p.get("treatment") is not None
    )
    player.treatment = min(
        rng().sample(TREATMENTS, len(TREATMENTS)),
        key=lambda x: counts.get(x, 0),
    )
```

Do not assign the treatment on a page, as `treatments_balanced` does. Pages run
only after `page_order` has been called, so `player.treatment` would not exist
yet, and `page_order` would raise an `AttributeError`. If you also leave out
dropouts, put both parts in the same `new_player`.

Then, in `page_order`, count only players in the same treatment:

```python
if p.get("order") is not None and p.get("treatment") == player.treatment
```

### Why `p.get(...)`

Use `p.get("field")` in these conditions, not `p.field` or
`player.session.players.filter(_.field == ...)`. A session can contain players
who have not started yet. They do not have your fields, so `p.field` and
`filter()` raise an `AttributeError`, while `p.get("field")` returns `None`.
