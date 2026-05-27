# bisection

Certainty-equivalent elicitation over mean-preserving spreads (Rothschild & Stiglitz, 1970).

## Design

Fix the mean at €50 and construct a chain of lotteries where each is a mean-preserving spread (MPS) of the previous:

| Lottery | Outcomes (50–50) | Mean |
|---------|------------------|------|
| L0      | €50 certain      | €50  |
| L1      | €47 or €53       | €50  |
| L2      | €40 or €60       | €50  |
| L3      | €25 or €75       | €50  |
| L4      | €0 or €100       | €50  |

For each lottery L1–L4, the certainty equivalent (CE) is elicited via a bisection procedure: in each of 5 steps, the participant chooses between a certain amount and the lottery. The certain amount adjusts based on the answer, converging on the CE. The search range for each lottery is bounded by its outcomes, so precision scales with the spread.

| Lottery | Search range | Precision (5 steps) |
|---------|-------------|---------------------|
| L1      | [47, 53]    | ±0.09               |
| L2      | [40, 60]    | ±0.31               |
| L3      | [25, 75]    | ±0.78               |
| L4      | [0, 100]    | ±1.56               |

The risk premium π = 50 − CE must be nonnegative and weakly increasing across the chain for any risk-averse expected-utility maximizer. The shape of π as a function of the spread traces out risk aversion nonparametrically — no functional form for u(·) is assumed.

**Claim.** Under expected utility with u continuous and strictly increasing: u is concave if and only if π(L) ≥ 0 for every lottery L, and π(G) ≥ π(F) whenever G is an MPS of F. The forward direction is Jensen's inequality plus Rothschild–Stiglitz (1970, Theorem 2). The reverse is by contrapositive: if u is not concave, a binary lottery violating Jensen gives π < 0.

## Loading

```python
load_config(uproot_server, config="bisection", apps=["bisection"])
```

## Configuration

All parameters are in `class C`:

- `MEAN` — common expected value of all lotteries (default: 50)
- `LOTTERIES` — list of (low, high) outcome pairs (default: the chain above)
- `BISECTION_STEPS` — questions per lottery (default: 5; increase for finer precision)

## Data

The `pipeline` function exports one row per (participant × lottery) with:

- `ce` — certainty equivalent
- `risk_premium` — π = MEAN − CE
- `step_1_certain` through `step_5_certain` — raw bisection choices (True = chose certain)
