# quiz

Load this app using

```python
load_config(uproot_server, config="quiz", apps=["quiz"])
```

## Why `hash()` in `__init__.py`?

*This is expert-level information. If you’re just an academic using the quiz app, you can safely ignore this section.*

On line 76, the answer shuffling is seeded with `hash(player.name + f"q{i}")`. The reason for using `hash()` here is to prevent participants from reverse-engineering the correct answer order from their name and the question number, and thus inferring which answer is correct.

Python’s `hash()` function is randomized across interpreter restarts (via `PYTHONHASHSEED`), which adds unpredictability. Without this, a deterministic seed based solely on the player name and question number could allow a savvy participant to predict the shuffle order and deduce the correct answer position.
