This repository contains example apps for `uproot`, a framework for browser-based behavioral experiments. Treat the example apps as templates when building or modifying experiments.

Before making changes, read `README.md` for the full app table and scan `main.py` to see every loaded example. Then study 2-3 relevant apps directly: read each app's `__init__.py` completely and inspect the matching HTML templates.

Each app directory typically contains:
- `__init__.py` for all Python logic, constants, fields, and page classes
- `*.html` templates that match page class names
- `README.md` with loading notes or extra context

When looking for an implementation pattern, search the repo instead of guessing. Useful terms include `GroupCreatingWait`, `SynchronizingWait`, `Rounds(`, `fields = dict(`, `@live`, `notify(`, `Random(`, `timeout(`, and `um.create_model`.

When adding a new app:
- Copy the closest existing example as a starting point
- Preserve the required license header at the top of `__init__.py`
- Define `DESCRIPTION` and `page_order`
- Create matching HTML templates for each page class
- Add the app to `main.py` with `load_config()`
- Add the app to the `README.md` apps table with a short description and difficulty

Frontend notes:
- Bootstrap 5 CSS/JS and Alpine.js are already available on every page
- Follow Bootstrap layout and form conventions
- Put repeating markup in separate templates and include them with `{{ include "APP_NAME/file.html" }}`

Validation and local run:
- Run `uv run uproot run` to start the project
- If installed, run `black`, `isort`, and `ruff` after changes
- Issues about star imports may be ignored here
