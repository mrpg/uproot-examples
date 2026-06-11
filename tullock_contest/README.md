# tullock\_contest

A Tullock rent-seeking contest (Tullock, 1980). Each player in a group of two receives an endowment of $20 and invests any whole amount of it in a contest for a $20 prize. A player's probability of winning equals their own investment divided by the total investment in the group; investments are sunk. If nobody invests, the prize is not awarded.

In the Nash equilibrium of the two-player contest, each player invests a quarter of the prize ($5); experiments typically find substantial overinvestment.

Load this app using

```python
load_config(uproot_server, config="tullock_contest", apps=["tullock_contest"])
```
