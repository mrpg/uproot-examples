# first\_price\_auction

A first-price sealed-bid auction with independent private values. Each bidder receives a private value between $0 and $100 and submits one sealed bid. The highest bidder wins the item, pays their own bid, and earns their value minus their bid; everyone else earns nothing. Ties are broken at random.

Since the winner pays their own bid, bidders have an incentive to shade their bids below their values. Compare `second_price_auction`, where truthful bidding is a dominant strategy.

Load this app using

```python
load_config(uproot_server, config="first_price_auction", apps=["first_price_auction"])
```
