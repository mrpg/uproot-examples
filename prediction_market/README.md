## Loading

In `main.py`, use:

```python
load_config(uproot_server, config="prediction_market", apps=["prediction_market"])
```

## Resolving the market

Run the pipeline with the event outcome as the data argument:

```json
{"event": true}
```

Pass `true` if the event occurred or `false` if it did not. This moves all players to the Results page.

## Refunding players

You can also terminate the market and refund players:

```json
{"refund": true}
```

This allows you to implement a simple *decision* market.
