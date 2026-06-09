# tabs

Tab navigation for pages. Subjects can go back and forth between sections on a single page. Puts players back on the final tab if form validation fails (useful for comprehension checks).

## How to load

```python
load_config(uproot_server, config="tabs", apps=["tabs"])
```

## Setup

This app requires `tabs.css` and `tabs.js` in the project-level `_static/` folder. Copy them from this repository's `_static/` directory into your own project's `_static/` directory. They are loaded via `projectstatic()`.
