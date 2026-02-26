# grouping\_test\_arbitrary\_size

Demonstrates grouping with a configurable group size, timeout-based dropout handling, and multi-round group interactions.

Participants first see a page with a timeout. Those who time out (or voluntarily abort) are excluded before grouping. The remaining participants are split into groups of size `C.GROUP_SIZE`, and any surplus participants who don't fit into a full group are notified and removed. Grouped participants then go through multiple rounds where further timeouts cause the entire group to drop out together.

To test, run with a number of participants that is not a multiple of `C.GROUP_SIZE` (default: 3).

Load this app using

```python
load_config(uproot_server, config="grouping_test_arbitrary_size", apps=["grouping_test_arbitrary_size"])
```
