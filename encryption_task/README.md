# encryption\_task

Load this app using

```python
load_config(uproot_server, config="encryption_task", apps=["encryption_task"])
```

This app implements the encryption task described in:

> Nisvan Erkal, Lata Gangadharan, Nikos Nikiforakis; [Relative Earnings and Giving in a Real-Effort Experiment.](https://www.aeaweb.org/articles?id=10.1257/aer.101.7.3330) American Economic Review, 2011; 101(7): 3330-48.

Participants see an encryption table that maps all 26 letters of the alphabet to random digits (0-9). They must decode a “word” (random letter string, e.g., `QMFKWT`) into the corresponding digits by looking up each letter in the table.

To reduce cognitive load, only the first 13 letters of the shuffled alphabet are used when generating words to decode. The full 26-letter table is displayed but participants only need to search the top half.

The following parameters are configurable in `class C`:

- `ACTIVE_LETTERS` (default: 13) — Only these many letters (from the shuffled alphabet) are used for puzzles
- `WORD_LENGTH` (default: 6) — Length of strings to decode
- `DURATION` (default: 120) — Task duration in seconds
- `TABLE_MODE` (default: `"fixed"`) — `"fixed"` keeps the same table throughout; `"random"` generates a new table for each puzzle
- `SEED` (default: `None`) — Random seed; set to a value for reproducible sequences across participants

*Note*: Incorrect submissions do not advance participants to the next puzzle.

*Note*: In `"fixed"` mode (the default), all puzzles use the same encryption table, only the word changes. This matches the original design where learning the table layout is part of the task.
