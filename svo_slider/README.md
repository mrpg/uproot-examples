# svo\_slider

The Social Value Orientation slider measure (Murphy, Ackermann & Handgraaf, 2011), using the six primary items. Participants allocate points between themselves and an anonymous other person by moving sliders; each slider position corresponds to one own/other allocation pair.

From the mean allocations, the app computes the SVO angle, `atan2(mean_other − 50, mean_self − 50)`, and classifies participants as altruistic, prosocial, individualistic, or competitive.

For simplicity, the allocations in this example are not paid out. In an incentivized study, you would pair participants, randomly select one item per pair, and pay the chosen allocation.

Load this app using

```python
load_config(uproot_server, config="svo_slider", apps=["svo_slider"])
```
