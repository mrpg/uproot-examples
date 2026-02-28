# uproot examples

The folders in this repository contain [uproot](https://uproot.science/) examples.

## Running all examples

This repository is also an uproot *project*. That means: you can clone it and run `uv run uproot run` (or just `uproot run`, [depending on your setup](https://github.com/mrpg/uproot?tab=readme-ov-file#getting-started)) to enjoy these example apps *all at once* from the comfort of your home.

## Apps

| App                                               | Description                                                     | Difficulty |
|---------------------------------------------------|-----------------------------------------------------------------|------------|
| `barrier`                                         | Force players to stay on a page                                 | Easy       |
| `beauty_contest`                                  | Beauty contest / guessing game (Nagel, 1995)                    | Easy       |
| `big5_short`                                      | Short Big 5 questionnaire with scoring                          | Medium     |
| `bounded_choice`                                  | Examples for the BoundedChoiceField                             | Easy       |
| `chat`                                            | Chat                                                            | Easy       |
| `continuous`                                      | Do something in intervals (background tasks)                    | Medium     |
| `counter_alpine`                                  | Counter with live updates (Alpine.js)                           | Easy       |
| `counter`                                         | Counter with live updates                                       | Easy       |
| `dictator_game`                                   | Standard dictator game                                          | Easy       |
| `double_auction`                                  | Double auction (like Smith, 1962)                               | Advanced   |
| `drawing_board`                                   | Session-level drawing board                                     | Medium     |
| `dropouts`                                        | Handling dropouts                                               | Easy       |
| `embed_static`                                    | Embedding a static file                                         | Easy       |
| `encryption_task`                                 | Encryption task (Erkal et al., 2011)                            | Medium     |
| `focal_point`                                     | Focal point game (like Schelling, 1957)                         | Easy       |
| `gift_exchange_game`                              | Gift exchange game (Fehr et al., 1993)                          | Easy       |
| `grouping_test`                                   | Custom group creation                                           | Easy       |
| `grouping_test_arbitrary_size`                    | Grouping with configurable size, timeouts, and dropout handling | Medium     |
| `grouping_test_one_spare`                         | Two equal groups with one surplus participant                   | Easy       |
| `grouping_via_GroupCreatingWait_and_move_to_page` | Grouping with configurable size, timeouts, and dropout handling | Medium     |
| `input_elements`                                  | Showcasing the input elements provided by uproot                | Easy       |
| `many_fields`†                                    | Benchmark: insert many fields                                   | Easy       |
| `minimum_effort_game`                             | Minimum effort / weakest link game (Van Huyck et al., 1990)     | Easy       |
| `mpl`                                             | Multiple price list                                             | Medium     |
| `multilanguage`                                   | App with language switcher                                      | Easy       |
| `nato_alphabet`                                   | NATO phonetic alphabet real effort task (Gibson, 2025)          | Advanced   |
| `notifications`†                                  | Test notifications between players                              | Easy       |
| `observed_diary`                                  | Observed diary/surveillance game                                | Medium     |
| `payment_data`                                    | Collecting payment data                                         | Easy       |
| `ping`†                                           | WebSocket round-trip time benchmark                             | Easy       |
| `prisoners_dilemma_apply`                         | Standard prisoner's dilemma                                     | Medium     |
| `prisoners_dilemma_repeated`                      | Repeated prisoner's dilemma (history table and digest)          | Easy       |
| `prisoners_dilemma`                               | Standard prisoner's dilemma                                     | Easy       |
| `public_goods_game`                               | Standard public goods game                                      | Easy       |
| `quiz`                                            | Quiz/comprehension check                                        | Easy       |
| `randomize_apps`                                  | Randomizing app order                                           | Easy       |
| `randomize_pages_allow_back`                      | Randomizing page order and allow going back                     | Easy       |
| `randomize_pages`                                 | Randomizing page order                                          | Easy       |
| `read_settings`†                                  | Read session settings                                           | Easy       |
| `rounds_nested`                                   | Using nested rounds                                             | Easy       |
| `rounds`                                          | Using rounds (history table)                                    | Easy       |
| `stroop`                                          | Stroop task                                                     | Advanced   |
| `student_id`                                      | Have participants enter their Student ID                        | Easy       |
| `sumhunt`                                         | Real effort task about finding sums in matrices                 | Medium     |
| `survey`                                          | Survey with follow-up verification                              | Easy       |
| `timeout_multipage`                               | Timeout that spans multiple pages                               | Easy       |
| `travellers_dilemma`                              | Traveller's dilemma (Basu, 1994)                                | Easy       |
| `treatments_balanced`                             | Treatment assignment (more balanced/cycling)                    | Easy       |
| `treatments`                                      | Treatment assignment (basic)                                    | Easy       |
| `trigger_jserrors`†                               | Test JavaScript error handling                                  | Easy       |
| `trust_game`                                      | Trust game (Berg et al., 1995)                                  | Easy       |
| `twobytwo`                                        | Generic 2×2 game with simulator                                 | Medium     |
| `typography`                                      | Showcasing the default fonts used by uproot                     | Easy       |
| `ultimatum_game`                                  | Standard ultimatum game                                         | Easy       |
| `upload`                                          | Uploading files                                                 | Easy       |

†Apps primarily for internal testing and benchmarking, but useful as simple examples of individual uproot features.

## Other examples

| Directory      | Description            |
|----------------|------------------------|
| `progress_bar` | Automatic progress bar |
| `start_button` | Start button           |

## License

Everything in this repository is licensed under the **0BSD License** (Zero-Clause BSD).

### For users and developers

You are completely free to do anything with this code. No requirements, no attribution needed, no obligations of any kind. There is no warranty.

### For contributors

By contributing to this repository, your contributions are licensed under 0BSD, granting the same unlimited freedom to everyone.

### Full license

See [LICENSE](LICENSE) for the complete 0BSD license text.
