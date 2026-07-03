# rerandomization

Load this app using

```python
load_config(uproot_server, config="rerandomization", apps=["rerandomization"])
```

This example shows treatment assignment by rerandomization after collecting
baseline covariates.

Players first answer a short survey with age and prior economics coursework.
They then reach a session-level wait page. The wait page waits for everyone in
the session to arrive. Once all session participants are present, it assigns
every player to a treatment arm using the rerandomization algorithm.

The algorithm is based on the Euclidean rerandomization approach from Schindl
and Branson's paper, ["A Unified Framework for Rerandomization using Quadratic
Forms"](https://arxiv.org/abs/2403.12815). It standardizes the covariates,
randomly proposes balanced-size assignments, and accepts the first assignment
whose Euclidean covariate imbalance is below a Monte Carlo threshold.

For two treatment arms, the implementation uses the paper's Euclidean balance
metric. The helper module also includes a transparent extension to more than two
treatment arms: it uses an ANOVA-style between-arm sum of squares so that all
arm means are balanced symmetrically. That multi-arm extension is implemented
for practical use in uproot examples, but it is not a separate multi-arm result
proved in the paper.

If rerandomization cannot produce an accepted assignment within the configured
iteration limit, the app falls back to a simple shuffled assignment with the
same arm sizes.
