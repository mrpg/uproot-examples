# vcg

Public good provision using the Vickrey–Clarke–Groves (VCG) mechanism with the Clarke pivot rule. Each player in a group of 3 receives a random private value (between $0 and $100) for a shared project that costs $150 to fund. Players simultaneously report how much the project is worth to them. The project is funded if the total reported values reach the cost; otherwise it is not.

Each player pays only if they are *pivotal* — that is, if the project would not have been funded without their report. A pivotal player pays just the gap between the cost and the other members' reported values. Truthful reporting is a dominant strategy.

The mechanism does not balance the budget: total payments are typically less than the project cost. The deficit illustrates a fundamental result in mechanism design — efficiency, incentive compatibility, individual rationality, and budget balance cannot all hold simultaneously.

Load this app using

```python
load_config(uproot_server, config="vcg", apps=["vcg"])
```
