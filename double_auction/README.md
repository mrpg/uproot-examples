# double\_auction

Load this app using

```python
load_config(uproot_server, config="double_auction", apps=["double_auction"])
```

A continuous double auction market experiment inspired by Vernon Smith's (1962) seminal design. Buyers and sellers trade a single indivisible unit each round by posting bids and asks in real time. When a participant accepts an opposing offer, a trade executes immediately at the posted price.

## How it works

### Page flow

1. **RaiseHands** -- Attendance check. Players toggle a switch to indicate presence. A configurable detection period (default 30 s) runs; only players who marked themselves present proceed.
2. **Assignment** (invisible) -- Assigns each present player a role (buyer or seller) and a private value or cost drawn from the configured schedules.
3. **Instructions** -- Explains the auction rules, tailored to the player's assigned role.
4. **Trade** (repeated for `num_rounds` rounds, each preceded by **RoundInfo**):
   - **RoundInfo** -- Shows the player their role, private value/cost, any applicable tax, and the profit formula for the upcoming round.
   - **Trade** -- The live trading page. Players submit, replace, or cancel offers and can accept opposing offers. A shared timer counts down the trading period. Once a player trades, they see their profit and can no longer participate in that round.

### Trading mechanics

- **Buyers** post **bids** (willingness to pay). A bid cannot exceed the buyer's valuation minus any buyer tax.
- **Sellers** post **asks** (minimum acceptable price). An ask cannot be below the seller's cost plus any seller tax.
- Each player may have at most one active offer at a time. Submitting a new offer replaces the old one.
- Clicking an opposing offer accepts it, executing a trade at the posted price. Both parties' offers are cancelled and neither can trade again that round.
- The market book, transaction history, and offer changes are broadcast to all participants in real time via WebSocket diffs (`MarketDiff` and `OfferAccepted` events).

### Profit calculation

| Role   | Formula                                    |
|--------|--------------------------------------------|
| Buyer  | Profit = Valuation &minus; Price &minus; Buyer Tax |
| Seller | Profit = Price &minus; Cost &minus; Seller Tax     |

If a player does not trade in a round, their profit for that round is zero.

### Role assignment

Roles are assigned by **tiling** the configured `values` and `costs` lists across the present participants. The combined list of buyer and seller roles is repeated (tiled) as many times as it fits into the number of players. Any remaining participants beyond a full tile receive alternating buyer/seller roles with the most favorable value or cost (highest value for extra buyers, lowest cost for extra sellers).

For example, with `values: [100, 100]` and `costs: [50, 50, 50]` (5 roles per tile) and 12 participants: the tile repeats twice (10 players), and the 2 extra players get one additional buyer (value 100) and one additional seller (cost 50).

## Settings

All settings are optional. Configure them via `session.settings` (e.g., in a scenario file or the admin interface).

| Setting       | Type            | Default                          | Description |
|---------------|-----------------|----------------------------------|-------------|
| `values`      | list of int     | `[10, 9, 8, 7, 6, 5, 4, 3, 2, 1]` | Buyer valuations. One entry per buyer role. |
| `costs`       | list of int     | `[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]` | Seller costs. One entry per seller role. |
| `num_rounds`  | int             | `3`                              | Number of trading rounds. |
| `duration`    | int (seconds)   | `1500` (25 min)                  | Length of each trading period. |
| `buyer_tax`   | int or list     | `0`                              | Per-unit tax on buyers. If a list, one entry per round (length must equal `num_rounds`). |
| `seller_tax`  | int or list     | `0`                              | Per-unit tax on sellers. If a list, one entry per round (length must equal `num_rounds`). |

### Example scenarios

**Symmetric market, no taxes** (3 rounds, 10 min each):

```json
{
    "values": [100, 85, 70, 55, 44, 38, 30, 20, 10],
    "costs": [5, 15, 25, 35, 40, 50, 60, 75, 90],
    "buyer_tax": [0, 0, 0],
    "seller_tax": [0, 0, 0],
    "duration": 600,
    "num_rounds": 3
}
```

**Tax incidence study** (9 rounds: 3 baseline, 3 with buyer tax, 3 with seller tax):

```json
{
    "values": [100, 100],
    "costs": [50, 50, 50],
    "buyer_tax": [0, 0, 0, 25, 25, 25, 0, 0, 0],
    "seller_tax": [0, 0, 0, 0, 0, 0, 25, 25, 25],
    "duration": 600,
    "num_rounds": 9
}
```

**Asymmetric costs** (3 rounds, no taxes):

```json
{
    "values": [100, 100, 100, 100],
    "costs": [10, 10, 10, 80, 80],
    "buyer_tax": [0, 0, 0],
    "seller_tax": [0, 0, 0],
    "duration": 600,
    "num_rounds": 3
}
```

## Admin digest

The digest (shown in the admin interface after the session ends) provides per-round analysis:

- **Expected equilibrium** -- Computed from the assigned values and costs (adjusted for taxes) using a competitive equilibrium solver. Reports the clearing price range and equilibrium quantity.
- **Supply and demand chart** -- Step-function curves of the (tax-adjusted) demand and supply schedules, with the equilibrium price and quantity annotated.
- **Actual trades chart** -- Scatter plot of realized transaction prices in execution order, with the expected equilibrium price overlaid for comparison.

This allows the experimenter to compare theoretical predictions against observed market outcomes.

## Files

| File                  | Purpose |
|-----------------------|---------|
| `__init__.py`         | All Python logic: constants, pages, models, live handlers, digest |
| `RaiseHands.html`     | Attendance toggle (Alpine.js) |
| `RoundInfo.html`      | Per-round role and profit info |
| `RoundInfoText.html`  | Shared text fragment for role/tax display (included by RoundInfo and Trade) |
| `InstructionsText.html` | Shared instructions text (included by Instructions page and the in-trade modal) |
| `Trade.html`          | Trading interface with offer book, transaction log, and input controls |
| `AdminDigest.html`    | Admin digest template with Chart.js supply/demand and transaction charts |
| `_static/trade.js`    | Client-side trading logic: offer submission, acceptance, real-time market updates |
