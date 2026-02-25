# grouping_test_one_spare

Demonstrates simple grouping where participants are split into two equal-sized groups, with at most one surplus participant left ungrouped.

All participants wait on a page with a short timeout, then a session-wide synchronizing wait creates two groups of equal size. If the number of participants is odd, the last one (alphabetically) is excluded and shown a message that they were not grouped.

To test, run with an odd number of participants to see the surplus handling.

Load this app using

```python
load_config(uproot_server, config="grouping_test_one_spare", apps=["grouping_test_one_spare"])
```
