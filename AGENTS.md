# Agent Instructions for uproot-examples

This repository contains example apps for [uproot](https://uproot.science/), a framework for browser-based behavioral experiments. Use these examples as templates when building new experiments.

## Before Writing Any Code

**Always explore existing examples first.** This repository contains 40+ apps covering most common experimental paradigms. The best way to build a new experiment is to find a similar one and adapt it.

### Step 1: Get the Full Picture

Before looking for specific patterns, understand what examples are available:

1. **Read `README.md`** - Contains a complete table of all apps with descriptions and difficulty ratings
2. **Scan `main.py`** - Shows all apps that are loaded; gives you the full list of available examples

This overview is essential. Don't skip to specific examples without first knowing what's available—you might miss a better starting point.

### Step 1.5: Always Read `input_elements`

**Always read `input_elements/__init__.py`** before building any app that uses form fields. It is the canonical showcase of every field type uproot provides (BooleanField, DateField, DecimalField, DecimalRangeField, EmailField, FileField, IntegerField, LikertField, RadioField, SelectField, StringField, TextAreaField, BoundedChoiceField, IBANField) and demonstrates their parameters, labels, descriptions, addons, and layout options. Use it as your primary reference for field usage.

### Step 2: Study Relevant Examples

Once you've identified promising examples from the README table:

1. **Read the `__init__.py`** of each relevant app completely
2. **Read the HTML templates** to see how data is displayed
3. **Compare 2-3 similar apps** to understand alternative approaches

Each app has the same structure:
- `__init__.py` - All Python logic (constants, pages, fields, callbacks)
- `*.html` files - Jinja2 templates matching page class names
- `README.md` - Loading instructions (sometimes additional context)

Apps marked with † are primarily for internal testing and benchmarking, but useful as simple examples of individual uproot features.

### Step 3: Check the Documentation

Full documentation is available at:
- https://uproot.science/ (web docs)
- https://github.com/mrpg/uproot-docs (source — **you are free to clone this and search through the Markdown files directly**)

```bash
git clone https://github.com/mrpg/uproot-docs /tmp/uproot-docs
```

Key documentation sections (under `docs/`):
- `building/` - Pages, forms, data storage
- `multiplayer/` - Groups, synchronization, real-time features
- `advanced/` - Rounds, timeouts, dropouts, uploads
- `reference/` - Field types, page methods, CLI

## Finding Patterns

When looking for how to implement something specific, use grep/search across the codebase rather than relying on a predetermined list. Common search terms:

- Groups: `GroupCreatingWait`, `group_size`
- Synchronization: `SynchronizingWait`, `all_here`
- Rounds: `Rounds(`, `player.round`, `digest(`
- Forms: `fields = dict(`, field type names like `RadioField`, `DecimalField`
- Real-time: `@live`, `notify(`, `uproot.invoke`
- Sensitive data: `stealth_fields`, `handle_stealth_fields`
- Randomization: `Random(`, `shuffled`
- Timeouts: `timeout(`, `timeout_reached`
- Constants/parameters: `C`
- Custom models: `um.Entry`, `um.create_model`

## When Building New Apps

1. **Copy an existing similar app** as your starting point
2. **Preserve the legally required license header** at the top of `__init__.py`
3. **Define `DESCRIPTION` and `page_order`**
4. **Create matching HTML templates** for each page class
5. **Add to `main.py`** with `load_config()` to test
6. **Add to `README.md`** in the Apps table with description and difficulty
7. **Add a `simulate.js`** to enable automated testing. This file runs on player pages in sessions created with "Simulate responses" enabled. Check existing examples for the pattern: use `uproot.currentPage` to match pages, fill in form fields (e.g., set radio buttons, input values), and call `uproot.submit()` to advance. Look at a similar app's `simulate.js` as a starting point.

### Frontend Libraries

uproot includes **Bootstrap 5 CSS and JS** on every page, as well as **Alpine.js**. These are available out of the box—no need to add script tags or imports.

When writing HTML templates, always follow Bootstrap best practices for layout and components (e.g., use the grid system, proper form classes, responsive utilities).

Put repeating parts in separate HTML files, and include them with `{{ include "ACTUAL_APP_NAME/SEPARATE_TEMPLATE_FILE.html" }}`.

## Exploring the Framework Source

**You may clone the uproot source code if necessary or useful.** When documentation and examples aren't enough, the source is the definitive reference:

```bash
git clone https://github.com/mrpg/uproot /tmp/uproot
```

The most important files for most users (find them by name):
- `smithereens.py` - Core utilities (`notify()`, etc.). This is where the key helper functions live.
- `fields.py` - All field type definitions. Essential for understanding what field types are available and how they work.
- `uproot.js` - Client-side JavaScript API for real-time features, form handling, and WebSocket communication.

Also useful:
- `uproot/types.py` - Page base classes and decorators

Reading the source helps with:
- Finding all available imports and their signatures
- Understanding how page lifecycle methods are called
- Discovering features not fully covered in documentation
- Debugging unexpected behavior

## Running the Examples

```bash
uv run uproot run  # or "uproot run" in a classic venv
```

This starts all loaded apps. Access the admin interface to create sessions and test.

## Best practices

If installed, run `black`, `isort`, `ruff` on any new apps. Issues with star imports may be safely ignored.

One tab is to equal 4 spaces, the standard indentation for all markup and programming languages.

### Jinja2 number formatting

Use the `fmtnum` filter when printing currency amounts in templates. Do not use older `to(1)`/`to(2)` filters or hand-written currency prefixes such as `${{ amount }}`.

For dollar amounts, include the dollar sign through the filter and use two decimal places:

```jinja2
{{ number | fmtnum(pre="$", places=2) }}
```

SI units may be printed as follows:

```jinja2
{{ distance | fmtnum(post=" meters", places=0) }}
```

Keep the spacing around filters and arguments readable; do not be breathless.

### Python vertical spacing

Add a blank line before `if`, `return`, `while`, and `for` statements. The exception is right after a line that ends with a colon (i.e., the first statement in any block) — no blank line there. Do not be breathless.
