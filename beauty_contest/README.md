# beauty\_contest

The beauty contest or p-guess game (Nagel, 1995). Players simultaneously choose a number between 0 and 100. The winner is the player whose guess is closest to p times the average of all guesses (default p = 2/3).

This game tests iterated reasoning and bounded rationality. The unique Nash equilibrium is for all players to guess 0.

Load this app using

```python
load_config(uproot_server, config="beauty_contest", apps=["beauty_contest"])
```
