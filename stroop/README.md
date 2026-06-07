# Stroop Color-Word Test

A classic cognitive psychology task measuring interference in reaction time, going back to Stroop, J.R. (1935), “Studies of interference in serial verbal reactions,” Journal of Experimental Psychology, 18(6), 643–662, https://doi.org/10.1037/h0054651. The version used here is adapted from the computerized version used in Gerhardt, H., Schildberg-Hörisch, H., Willrodt, J. (2017), “Does self-control depletion affect risk attitudes?”, European Economic Review, 100, 463–487, https://doi.org/10.1016/j.euroecorev.2017.09.004.

## How to load

```python
load_config(uproot_server, config="stroop", apps=["stroop"])
```

## Features

- Client-side timing using `performance.now()` for accurate reaction time measurement
- Each trial is one `Rounds()` round and is stored on the player
- Balanced congruent/incongruent trials
- Results page showing accuracy, mean RT, and Stroop effect
