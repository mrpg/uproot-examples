# multilanguage

Load this app using

```python
load_config(uproot_server, config="multilanguage", apps=["multilanguage"])
```

*Note*: Files ending in `.yml` in this directory are automatically loaded because of `load_all("multilanguage/")` in `__init__.py` — the patterns extend flexibly to further languages.

*Note*: Languages not natively provided by *uproot* (currently: de, en, es) may require you to translate strings like “Back” and “Next.” See, for example, `pt.yml` and contrast with `en.yml`.
