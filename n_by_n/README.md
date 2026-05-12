## n_by_n

Generic n×n game (2 ≤ n ≤ 26). A generalization of `twobytwo` that supports
arbitrary payoff matrices via session settings.

### Loading

```python
load_config(uproot_server, config="n_by_n", apps=["n_by_n"])
```

### Session Settings

Defaults to 3×3 Rock-Paper-Scissors. Override by setting `matrix` in session
settings. Each cell is `[row_player_payoff, col_player_payoff]`. Actions are
automatically labeled A, B, C, … based on the matrix dimension.

Example 2×2 Prisoner's Dilemma:

```json
{
    "matrix": [
        [[10, 10], [0, 15]],
        [[15, 0],  [3, 3]]
    ]
}
```
