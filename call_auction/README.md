# call\_auction

Load this app using

```python
load_config(uproot_server, config="call_auction", apps=["call_auction"])
```

A call auction (batch auction) where buyers and sellers submit sealed bids and asks during a timed period. When the period ends, a single clearing price is determined and all compatible offers execute simultaneously at that price.

## How it works

### Page flow

1. **Assignment** (invisible) -- Assigns each player a role (buyer or seller) and a private value or cost.
2. **Instructions** -- Explains the auction rules, tailored to the player's role.
3. **Submit** (repeated for `num_rounds` rounds) -- Players submit a bid or ask during a timed period. Offers can be revised before the period ends.
4. **Results** (repeated) -- Shows the clearing price, whether the player traded, and their profit.

### Clearing mechanics

After the bidding period ends:
1. Bids are sorted descending, asks are sorted ascending.
2. The competitive equilibrium is computed using a supply/demand intersection solver.
3. The clearing price is the midpoint of the equilibrium price range (rounded to the nearest integer).
4. Buyers who bid at or above the clearing price trade. Sellers who asked at or below the clearing price trade. All trades execute at the clearing price.

### Profit calculation

| Role   | Formula                             |
|--------|-------------------------------------|
| Buyer  | Profit = Valuation &minus; Clearing Price |
| Seller | Profit = Clearing Price &minus; Cost      |

If a player does not trade (or does not submit), their profit is zero.

### Role assignment

Identical to the double auction: roles are assigned by tiling the configured `values` and `costs` lists across all participants. Extra participants beyond a full tile receive alternating buyer/seller roles with the most favorable value or cost.

## Settings

All settings are optional. Configure them via `session.settings`.

| Setting       | Type            | Default                             | Description                        |
|---------------|-----------------|-------------------------------------|------------------------------------|
| `values`      | list of int     | `[10, 9, 8, 7, 6, 5, 4, 3, 2, 1]` | Buyer valuations (one per role).   |
| `costs`       | list of int     | `[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]` | Seller costs (one per role).       |
| `num_rounds`  | int             | `3`                                 | Number of auction rounds.          |
| `duration`    | int (seconds)   | `300` (5 min)                       | Length of each bidding period.     |

## Files

| File                | Purpose                                                        |
|---------------------|----------------------------------------------------------------|
| `__init__.py`       | All Python logic: constants, pages, live handlers, digest      |
| `Instructions.html` | Auction rules, tailored to buyer/seller role                   |
| `Submit.html`       | Bidding interface with input and timer                         |
| `Results.html`      | Round results: clearing price, trade outcome, profit           |
| `AdminDigest.html`  | Admin digest with per-round summary                            |
