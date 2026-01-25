# uproot examples

The folders in this repository contain [uproot](https://uproot.science/) examples.

## Running all examples

This repository is also an uproot *project*. That means: you can clone it and run `uv run uproot run` (or just `uproot run`, [depending on your setup](https://github.com/mrpg/uproot?tab=readme-ov-file#getting-started)) to enjoy these example apps *all at once* from the comfort of your home.

## Apps

| App                           | Description                                                   | Difficulty |
|-------------------------------|---------------------------------------------------------------|------------|
| barrier                       | Force players to stay on a page                               | Easy       |
| big5\_short                   | Short Big 5 questionnaire with scoring                        | Medium     |
| beauty\_contest               | Beauty contest / guessing game (Nagel, 1995)                  | Easy       |
| chat                          | Chat                                                          | Easy       |
| continuous                    | Do something in intervals (background tasks)                  | Medium     |
| counter†                      | Counter with live updates                                     | Easy       |
| counter\_alpine†              | Counter with live updates (Alpine.js)                         | Easy       |
| dictator\_game                | Standard dictator game                                        | Easy       |
| double\_auction               | Double auction (like Smith, 1962)                             | Advanced   |
| drawing\_board                | Session-level drawing board                                   | Medium     |
| dropouts                      | Handling dropouts                                             | Easy       |
| encryption\_task              | Encryption task (Erkal et al., 2011)                          | Medium     |
| focal\_point                  | Focal point game (like Schelling, 1957)                       | Easy       |
| gift\_exchange\_game          | Gift exchange game (Fehr et al., 1993)                        | Easy       |
| grouping\_test†               | Custom group creation                                         | Easy       |
| many\_fields†                 | Benchmark: insert many fields                                 | Easy       |
| mpl                           | Multiple price list                                           | Medium     |
| minimum\_effort\_game         | Minimum effort / weakest link game (Van Huyck et al., 1990)   | Easy       |
| notifications†                | Test notifications between players                            | Easy       |
| observed\_diary               | Observed diary/surveillance game                              | Medium     |
| payment\_data                 | Collecting payment data                                       | Easy       |
| ping†                         | WebSocket round-trip time benchmark                           | Easy       |
| prisoners\_dilemma            | Standard prisoner's dilemma                                   | Easy       |
| prisoners\_dilemma\_apply     | Standard prisoner's dilemma                                   | Medium     |
| prisoners\_dilemma\_repeated  | Repeated prisoner's dilemma (history table and digest)        | Easy       |
| public\_goods\_game           | Standard public goods game                                    | Easy       |
| quiz                          | Quiz/comprehension check                                      | Easy       |
| randomize\_apps               | Randomizing app order                                         | Easy       |
| randomize\_pages              | Randomizing page order                                        | Easy       |
| randomize\_pages\_allow\_back | Randomizing page order and allow going back                   | Easy       |
| read\_settings†               | Read session settings                                         | Easy       |
| rounds                        | Using rounds (history table)                                  | Easy       |
| student\_id                   | Have participants enter their Student ID                      | Easy       |
| sumhunt                       | Real effort task about finding sums in matrices               | Medium     |
| timeout\_multipage            | Timeout that spans multiple pages                             | Easy       |
| trigger\_jserrors†            | Test JavaScript error handling                                | Easy       |
| twobytwo                      | Generic 2×2 game with simulator                               | Medium     |
| trust\_game                   | Trust game (Berg et al., 1995)                                | Easy       |
| ultimatum\_game               | Standard ultimatum game                                       | Easy       |
| upload                        | Uploading files                                               | Easy       |

†Apps primarily for internal testing and benchmarking, but useful as simple examples of individual uproot features.

## Other examples

| Directory                     | Description                                 |
|-------------------------------|---------------------------------------------|
| progress\_bar                 | Automatic progress bar                      |
| start\_button                 | Start button                                |

## License

These examples are licensed under the **0BSD License** (Zero-Clause BSD).

### For users and developers

You are completely free to do anything with this code. No requirements, no attribution needed, no obligations of any kind. There is no warranty.

### For contributors

By contributing to this repository, your contributions are licensed under 0BSD, granting the same unlimited freedom to everyone.

### Full license

See [LICENSE](LICENSE) for the complete 0BSD license text.
