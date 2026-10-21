# market

Load this app using

```python
load_config(uproot_server, config="market", apps=["market"])
```

A continuous limit order book where participants can submit limit and market orders, cancel resting orders, and watch book and trade updates in real time.

## How it works

Players stay on a single live trading page until the market closes. The first player to reach the page starts a session-wide clock of `C.DURATION` seconds; once it expires, orders and cancellations are rejected and everyone advances. Limit orders rest in the book until they trade or are cancelled. Market orders sweep the currently available opposite side of the book up to the submitted quantity, then discard any unfilled remainder.

The app stores book and trade events in uproot models so the in-memory exchange can be reconstructed after a restart.

This app uses Max Grossmann’s [mini-exchange](https://github.com/mrpg/mini-exchange).
