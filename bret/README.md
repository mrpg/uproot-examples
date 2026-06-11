# bret

The Bomb Risk Elicitation Task (Crosetto & Filippin, 2013) in its static variant. Participants face a 5×5 grid of boxes, one of which contains a bomb. They choose how many boxes to collect (in reading order) by clicking on the grid. Each collected box earns $1, but if the bomb — placed uniformly at random after the decision — is among the collected boxes, everything is lost.

The number of boxes collected is a simple measure of risk attitude: a risk-neutral participant collects 12 or 13 boxes, risk-averse participants collect fewer.

Load this app using

```python
load_config(uproot_server, config="bret", apps=["bret"])
```
