# bootstrap\_elements

A guided walkthrough of [Bootstrap 5](https://getbootstrap.com/docs/5.3/) and [Bootstrap Icons](https://icons.getbootstrap.com/) for experiments. Twelve chapters, grouped by purpose, explain when to use each element, show live examples, and point out pitfalls specific to uproot:

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
12. Putting it together (with a home-made guided tour and a confirmation modal)

For form fields, see the `input_elements` app instead.

## How to load

```python
load_config(uproot_server, config="bootstrap_elements", apps=["bootstrap_elements"])
```

## Files

- `Chapter.html` is the shared layout of all chapters. It loads Bootstrap Icons and renders the progress bar and the Next/Back buttons.
- `_static/walkthrough.css` frames the examples. It is not needed to use Bootstrap.
- `_static/tour.js` and `_static/tour.css` implement the guided tour on top of Bootstrap’s popovers, without third-party code. Copy them into your own app’s `_static` folder to use the tour there.
