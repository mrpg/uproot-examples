# Public Goods Game with Strategy Method

One-shot public goods game using the strategy method (Fischbacher, Gächter & Fehr, 2001). Each player makes an unconditional contribution and fills out a contribution table. One random member's table is used; the other three members' unconditional contributions determine the relevant table entry.

## Loading

Add the following to your `main.py`:

```python
load_config(uproot_server, config="pgg_strategy_method", apps=["pgg_strategy_method"])
```

## Reference

Fischbacher, U., Gächter, S., & Fehr, E. (2001). Are people conditionally cooperative? Evidence from a public goods experiment. *Economics Letters*, 71(3), 397--404. https://doi.org/10.1016/S0165-1765(01)00394-9
