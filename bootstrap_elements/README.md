# bootstrap\_elements

A guided walkthrough of [Bootstrap 6](https://getbootstrap.com/docs/6.0/) and [Bootstrap Icons](https://icons.getbootstrap.com/) for experiments. Twelve chapters, grouped by purpose, explain when to use each element, show live examples, and point out pitfalls specific to uproot:

1. Welcome
2. Layout
3. Text and media
4. Icons
5. Tables
6. Cards and lists
7. Buttons
8. Feedback
9. Show and hide
10. Overlays
11. Utilities
12. Putting it together (with a home-made guided tour and a confirmation dialog)

For form fields, see the `input_elements` app instead.

## How to load

```python
load_config(uproot_server, config="bootstrap_elements", apps=["bootstrap_elements"])
```

## Files

- `Chapter.html` is the shared layout of all chapters. It loads Bootstrap Icons and renders the progress bar and the Next/Back buttons.
- `_static/walkthrough.css` frames the examples. It is not needed to use Bootstrap.
- `_static/tour.js` and `_static/tour.css` implement the guided tour with Bootstrap’s popover styles, without third-party code. Copy them into your own app’s `_static` folder to use the tour there.
