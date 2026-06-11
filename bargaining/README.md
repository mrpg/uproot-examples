# bargaining

Unstructured real-time bargaining over a fixed pie, in the spirit of free-form bargaining experiments (e.g., Karagözoğlu & Riedl, 2015). Two players have 120 seconds to divide $10. At any time, each player can send a proposal stating how much of the pie they want for themselves, and accept the other player's standing proposal. The first acceptance ends the bargaining; if the deadline passes without an agreement, both players earn nothing.

This app demonstrates how to combine `@live` methods, `notify`, `jsvars` (for restoring state after a reload), a shared group deadline via `timeout`, and `may_proceed` on a single page.

Load this app using

```python
load_config(uproot_server, config="bargaining", apps=["bargaining"])
```
