# second\_price\_auction

A second-price sealed-bid auction (Vickrey, 1961) with independent private values. Each bidder receives a private value between $0 and $100 and submits one sealed bid. The highest bidder wins the item but pays only the second-highest bid, earning their value minus that price; everyone else earns nothing. Ties are broken at random.

Bidding one's true value is a (weakly) dominant strategy, which makes this auction a workhorse for studying overbidding. Compare `first_price_auction`, where bidders shade their bids.

Load this app using

```python
load_config(uproot_server, config="second_price_auction", apps=["second_price_auction"])
```
