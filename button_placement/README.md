# button_placement

Demonstrates helpers for placing built-in page controls at arbitrary positions:

- `button_next()` and `button_back()` place navigation buttons with custom styling. When either is called, the default buttons are suppressed.
- `timeout_box()` and `timeout()` place the live timeout display outside the default header location. The `TimeoutDisplay` page intentionally empties the default `timeoutbox` block before rendering the timer in the main content.

Load this app using

```python
load_config(uproot_server, config="button_placement", apps=["button_placement"])
```
