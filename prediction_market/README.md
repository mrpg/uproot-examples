## Loading

In `main.py`, use:

```python
load_config(uproot_server, config="prediction_market", apps=["prediction_market"])
```

## Resolving the market

Run the pipeline with the event outcome as the data argument:

```json
{"event": 1}
```

Pass `1` if the event occurred or `0` if it did not. This moves all players to the Results page.
