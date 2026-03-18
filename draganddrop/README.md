# draganddrop

Drag-and-drop sorting task. Participants see 10 draggable items and must place each one into one of two buckets. Each item's placement is tracked individually via a hidden RadioField (`1` = Bucket 1, `2` = Bucket 2).

Uses HTML5 drag-and-drop with Bootstrap styling. Includes a basic touch fallback for mobile devices.

## Customization

Edit class `C` in `__init__.py` to:

- **Change items** — replace the `ITEMS` list with your own labels, HTML snippets, or `<img>` tags.
- **Rename buckets** — change `BUCKET_LABELS`.
- **Count-only mode** — if items are identical and you only need how many went into Bucket 1, see the commented-out `COUNT-ONLY MODE` block in `__init__.py` for a single-IntegerField alternative.

## Load this app

```python
load_config(uproot_server, config="draganddrop", apps=["draganddrop"])
```
