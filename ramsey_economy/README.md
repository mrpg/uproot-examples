# Ramsey Economy

A miniature laboratory economy based on the Ramsey growth model.

Three participants form a closed economy with Cobb–Douglas production. Each period:

1. **Labor stage**: Participants simultaneously perform a real-effort task (captcha puzzles) to earn labor income. Each correct puzzle = 1 unit of labor, up to a maximum.
2. **Consumption stage**: Participants observe wages, rental rates, and their available resources, then choose how much to consume. The remainder is saved as capital for the next period.

Consumption generates a concave redemption value (u(c) = 2√c) that determines earnings. The game continues with a known probability (default 90%) after each period, inducing discounting without end-game effects.

## Session settings

| Key      | Default | Description                              |
|----------|---------|------------------------------------------|
| `beta`   | `0.9`   | Continuation probability                 |
| `tau_l`  | `0.0`   | Proportional tax rate on labor income     |
| `tau_k`  | `0.0`   | Proportional tax rate on capital income   |

## Loading

Add to your `main.py`:

```python
load_config(uproot_server, config="ramsey_economy", apps=["ramsey_economy"])
```
