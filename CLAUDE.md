# Claude Instructions for uproot-examples

This repository contains example apps for [uproot](https://uproot.science/), a framework for browser-based behavioral experiments. Use these examples as templates when building new experiments.

## Before Writing Any Code

**Always explore existing examples first.** This repository contains 30+ apps covering most common experimental paradigms. The best way to build a new experiment is to find a similar one and adapt it.

### Step 1: Find Relevant Examples

1. Read `README.md` in the repository root - it lists all apps with brief descriptions and difficulty ratings
2. Browse app directories - each folder is a self-contained experiment
3. Apps marked with † are primarily for internal testing and benchmarking, but useful as simple examples of individual uproot features

### Step 2: Study the Example Apps

Each app has the same structure:
- `__init__.py` - All Python logic (pages, fields, callbacks)
- `*.html` files - Jinja2 templates matching page class names
- `README.md` - Loading instructions (sometimes additional context)

**To understand a pattern, read the `__init__.py` of at least 2-3 apps that use it.** Look for:
- Simple examples first (difficulty: Easy)
- Then medium complexity for more features
- Advanced examples for real-time or complex interactions

### Step 3: Check the Documentation

Full documentation is available at:
- https://uproot.science/ (web docs)

Key documentation sections:
- `docs/building/` - Pages, forms, data storage
- `docs/multiplayer/` - Groups, synchronization, real-time features
- `docs/advanced/` - Rounds, timeouts, dropouts, uploads
- `docs/reference/` - Field types, page methods, CLI

## How to Find Specific Patterns

### "How do I create groups/pairs?"
Look at: `dictator_game`, `prisoners_dilemma`, `ultimatum_game`
Search for: `GroupCreatingWait`, `group_size`

### "How do I synchronize players?"
Look at: `dictator_game`, `public_goods_game`
Search for: `SynchronizingWait`, `all_here`

### "How do I repeat pages/rounds?"
Look at: `prisoners_dilemma_repeated`, `rounds`, `big5_short`
Search for: `Rounds(`, `player.round`

### "How do I collect form data?"
Look at: `dictator_game` (simple), `quiz` (dynamic), `mpl` (complex)
Search for: `fields = dict(`, field type names like `RadioField`, `DecimalField`

### "How do I handle real-time interactions?"
Look at: `double_auction` (advanced), `chat`, `drawing_board`, `observed_diary`
Search for: `@live`, `notify(`, `uproot.invoke`

### "How do I handle sensitive data?"
Look at: `payment_data`, `quiz`
Search for: `stealth_fields`, `handle_stealth_fields`

### "How do I randomize pages or apps?"
Look at: `randomize_pages`, `randomize_pages_allow_back`, `randomize_apps`
Search for: `Random(`, `shuffled`

### "How do I handle timeouts?"
Look at: `timeout_multipage`, `double_auction`, `sumhunt`
Search for: `timeout(`, `timeout_reached`, `DURATION`

### "How do I store complex data?"
Look at: `double_auction`
Search for: `mod.Entry`, `mod.create_model`, `mod.add_entry`

### "How do I show results/history?"
Look at: `prisoners_dilemma_repeated`, `rounds`
Search for: `digest(`, `player.within(`

## Recommended Exploration Order

For a new experiment type:

1. **Find the closest example** in the README table
2. **Read its `__init__.py` completely** - understand the page flow
3. **Read its HTML templates** - see how data is displayed
4. **Check cross-references** - similar apps may show alternative approaches
5. **Consult docs** at https://uproot.science/ for detailed explanations

## Key Files to Understand

- `main.py` - Shows how apps are loaded with `load_config()`
- `dictator_game/__init__.py` - Canonical example of a 2-player game
- `quiz/__init__.py` - Dynamic fields and stealth field validation
- `double_auction/__init__.py` - Complex real-time interactions
- `prisoners_dilemma_repeated/__init__.py` - Rounds and history access

## When Building New Apps

1. **Copy an existing similar app** as your starting point
2. **Preserve the license header** at the top of `__init__.py`
3. **Define `DESCRIPTION` and `page_order`** - these are required
4. **Create matching HTML templates** for each page class
5. **Add to `main.py`** with `load_config()` to test

## Exploring the Framework Source

When documentation and examples aren't enough—for understanding internal behavior, available imports, or advanced features—clone the uproot source:

```bash
git clone https://github.com/mrpg/uproot /tmp/uproot
```

Useful for:
- Finding all available imports from `uproot.fields` or `uproot.smithereens`
- Understanding how page lifecycle methods are called
- Discovering undocumented features or helper functions
- Debugging unexpected behavior

Key source locations to explore:
- `uproot/fields.py` - All field type definitions
- `uproot/smithereens.py` - Core utilities (`players()`, `notify()`, `other_in_group()`, etc.)
- `uproot/types.py` - Page base classes and decorators

## Running the Examples

```bash
uv run uproot run  # or "uproot run" in a classic venv
```

This starts all loaded apps. Access the admin interface to create sessions and test.
