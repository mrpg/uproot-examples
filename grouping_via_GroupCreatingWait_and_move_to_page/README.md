# grouping\_via\_GroupCreatingWait\_and\_move\_to\_page

Demonstrates grouping with a configurable group size, timeout-based dropout handling, and multi-round group interactions.

Participants first see a page with a timeout. Those who time out (or voluntarily abort) are excluded before grouping. The remaining participants are split into groups of size `C.GROUP_SIZE`, and any surplus participants who do not fit into a full group are notified and removed. Grouped participants then go through multiple rounds where further timeouts cause the entire group to drop out together.

To test, run with varying numbers of participants — in particular, numbers that are not a multiple of `C.GROUP_SIZE` (default: 3).

Load this app using

```python
load_config(uproot_server, config="grouping_via_GroupCreatingWait_and_move_to_page", apps=["grouping_via_GroupCreatingWait_and_move_to_page"])
```
