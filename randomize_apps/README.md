# randomize\_apps

Load this app using

```python
load_config(uproot_server, config="randomize_apps", apps=["randomize_apps"])
```
## Implementation note

`randomize_apps` is a “meta app” of sorts.

It is *allowed but not required to* contain any pages or any logic besides (1) importation of the apps to be randomized and (2) using `Random(Bracket(*appX.page_order), …)` in its own `page_order`.

This folder contains a minimal working example (MWE).

## Important: Don't forget to load all your apps

Remember to load the apps to be randomized, too! E.g.,

```python
load_config(uproot_server, config="all_apps", apps=["app1", "app2", "app3"])
```

Not doing that will make constants unavailable, and potentially cause other issues.

## Important: Call app-level functions manually

If any of your apps uses `new_player` or `new_session`, you must call these functions from the corresponding function of `randomize_apps`.
