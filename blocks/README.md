# blocks

Load this app using

~~~python
load_config(uproot_server, config="blocks", apps=["blocks"])
~~~

This deliberately small app asks for one number on each round. Watch the
three values shown on every page:

| Page sequence | `player.block` | `player.round` | `player.round_nested` |
|---------------|----------------|----------------|-----------------------|
| First `Rounds`, step 1 | `red` | 1 | `[1]` |
| First `Rounds`, step 2 | `red` | 2 | `[2]` |
| Second `Rounds` | `blue` | 1 | `[1]` |
| `Repeat`, step 1 | `red` | 3 | `[3]` |
| `Repeat`, step 2 | `red` | 4 | `[4]` |
| Final `Rounds`, outer step | `blue` | 2 | `[2]` |
| Final `Rounds`, inner step 1 | `blue` | 3 | `[2, 1]` |
| Final `Rounds`, inner step 2 | `blue` | 4 | `[2, 2]` |

The two blocks have independent counters. Switching from red to blue starts
blue at 1; returning to red resumes at 3. The red `Repeat` uses the same
counter as red `Rounds`. `RepeatStep.before_once` sets `player.add_round` on
red round 3, so `Repeat` runs exactly twice.

The final, inner `Rounds` has no `block` argument: it inherits blue from its
outer `Rounds`. Each inner round increments `player.round`, while
`player.round_nested` also shows its position inside blue round 2. An inner
`Rounds` cannot name a separate block. Since this app has several outer loops,
each outer `Rounds` or `Repeat` must name a block.

The Summary page retrieves answers with
`player.within(app="blocks", block=block).along("round")`. Red round 1 and
blue round 1 are separate records. In the admin data viewer, filter by block;
in grouped exports, use `app`, `block`, and `round`. Block counters start over
in each app, so another app can reuse the names red and blue.

This examples branch uses the matching `blocks` branch of uproot.
