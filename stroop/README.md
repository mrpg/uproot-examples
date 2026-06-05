# Stroop Task

A classic cognitive psychology task measuring interference in reaction time.

## How to load

```python
load_config(uproot_server, config="stroop", apps=["stroop"])
```

## Features

- Client-side timing using `performance.now()` for accurate reaction time measurement
- Each trial is one `Rounds()` round and is stored on the player
- Balanced congruent/incongruent trials
- Results page showing accuracy, mean RT, and Stroop effect
