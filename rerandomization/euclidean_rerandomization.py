"""Euclidean rerandomization for multi-arm experiments.

Implements the Euclidean rerandomization scheme (A = I_d) from Schindl &
Branson, "A Unified Framework for Rerandomization using Quadratic Forms."
See here for the working paper: https://arxiv.org/abs/2403.12815
Covariates are standardized to unit variance, then treatment is randomly
assigned until the Euclidean balance metric falls below a finite-randomization
threshold chosen to match a given acceptance probability alpha.

For K = 2, the balance metric is the paper's exact Euclidean quadratic
form:

    Q = n * || X_bar_1 - X_bar_0 ||^2

Generalized to K > 2 treatment arms via the between-group sum of squares:

    Q = sum_k  n_k * || X_bar_k - X_bar ||^2

Equivalently, this is the weighted pairwise-distance criterion:

    Q = (1 / n) * sum_{i < j} n_i n_j * || X_bar_i - X_bar_j ||^2

Thus the multi-arm statistic balances all treatment-arm mean differences
symmetrically, with larger arms receiving proportionally larger weight.  This
is an ANOVA-style Euclidean extension of the paper's two-arm criterion, not a
separate multi-arm result proved in the paper.

When K = 2, the between-group form reduces to

    (n_0 n_1 / n) * || X_bar_1 - X_bar_0 ||^2

which is p(1-p) times the paper's n * ||X_bar_1 - X_bar_0||^2 metric.  That
constant factor does not affect accept/reject decisions if the threshold is
calibrated to the same statistic; the implementation still uses the paper's
exact scaling for the explicit two-arm path.

Reference implementation: the authors provide R replication code at
https://github.com/kyleschindl/rerandomization-quadratic-forms
(R/replication_functions.R).  This Python module is a clean, zero-dependency
implementation of the core Euclidean rerandomization algorithm (A = I_d), with
an additional multi-arm extension not covered in the paper or R code.

This file is released under the CC0 license:
https://creativecommons.org/publicdomain/zero/1.0/deed.en
"""

import math
import random


def _col_means_and_stds(X: list[list[float]]) -> tuple[list[float], list[float]]:
    n = len(X)
    d = len(X[0])
    means = [0.0] * d
    for row in X:
        for j in range(d):
            means[j] += row[j]
    means = [m / n for m in means]

    variances = [0.0] * d
    for row in X:
        for j in range(d):
            diff = row[j] - means[j]
            variances[j] += diff * diff
    stds = [math.sqrt(v / (n - 1)) if v > 0 else 0.0 for v in variances]
    return means, stds


def _standardize(X: list[list[float]]) -> list[list[float]]:
    means, stds = _col_means_and_stds(X)
    out = []
    for row in X:
        out.append(
            [
                (row[j] - means[j]) / stds[j] if stds[j] > 0 else 0.0
                for j in range(len(row))
            ]
        )
    return out


def _two_arm_balance_metric(
    X: list[list[float]],
    assignment: list[str],
    treatments: list[str],
) -> float:
    """Paper metric: Q_I(sqrt(n) tau_X) = n ||Xbar_1 - Xbar_0||^2."""
    n = len(X)
    d = len(X[0])
    group_sums = {t: [0.0] * d for t in treatments}
    group_n = {t: 0 for t in treatments}
    for i, t in enumerate(assignment):
        group_n[t] += 1
        for j in range(d):
            group_sums[t][j] += X[i][j]

    first, second = treatments
    q = 0.0
    for j in range(d):
        diff = (
            group_sums[first][j] / group_n[first]
            - group_sums[second][j] / group_n[second]
        )
        q += diff * diff
    return n * q


def _balance_metric(
    X: list[list[float]],
    assignment: list[str],
    treatments: list[str],
) -> float:
    """Euclidean balance metric on standardized covariates."""
    if len(treatments) == 2:
        return _two_arm_balance_metric(X, assignment, treatments)

    # Multi-arm extension: the between-group sum of squares is zero exactly
    # when all arm means match.  Algebraically,
    #   sum_k n_k ||m_k - m||^2
    # = (1/n) sum_{i<j} n_i n_j ||m_i - m_j||^2,
    # so this penalizes every pairwise arm-mean difference with natural
    # sample-size weights.  For K = 2 this is p(1-p) times the paper metric;
    # the two-arm branch above keeps the paper's exact scaling.
    n = len(X)
    d = len(X[0])

    overall = [0.0] * d
    for row in X:
        for j in range(d):
            overall[j] += row[j]
    overall = [s / n for s in overall]

    group_sums = {t: [0.0] * d for t in treatments}
    group_n = {t: 0 for t in treatments}
    for i, t in enumerate(assignment):
        group_n[t] += 1
        for j in range(d):
            group_sums[t][j] += X[i][j]

    q = 0.0
    for t in treatments:
        nk = group_n[t]
        if nk == 0:
            continue
        for j in range(d):
            diff = group_sums[t][j] / nk - overall[j]
            q += nk * diff * diff
    return q


def _random_assignment(
    n: int,
    group_sizes: list[int],
    treatments: list[str],
    rng: random.Random,
) -> list[str]:
    pool = []
    for t, size in zip(treatments, group_sizes):
        pool.extend([t] * size)
    rng.shuffle(pool)
    return pool


def _empirical_quantile(
    values: list[float],
    alpha: float,
) -> float:
    """R's default type-7 sample quantile."""
    values = sorted(values)
    if len(values) == 1:
        return values[0]
    h = (len(values) - 1) * alpha
    lo = math.floor(h)
    hi = math.ceil(h)
    if lo == hi:
        return values[lo]
    return values[lo] + (h - lo) * (values[hi] - values[lo])


def _finite_randomization_threshold(
    X: list[list[float]],
    group_sizes: list[int],
    treatments: list[str],
    alpha: float,
    n_mc: int,
    rng: random.Random,
) -> float:
    qs = [
        _balance_metric(
            X,
            _random_assignment(
                len(X),
                group_sizes,
                treatments,
                rng,
            ),
            treatments,
        )
        for _ in range(n_mc)
    ]
    return _empirical_quantile(qs, alpha)


def _threshold(
    X: list[list[float]],
    group_sizes: list[int],
    treatments: list[str],
    alpha: float,
    n_mc: int,
    rng: random.Random,
) -> float:
    return _finite_randomization_threshold(X, group_sizes, treatments, alpha, n_mc, rng)


def _validated_covariates(covariates: list[list[float]]) -> list[list[float]]:
    n = len(covariates)
    if n < 2:
        raise ValueError("need at least two units")
    d = len(covariates[0])
    if d < 1:
        raise ValueError("need at least one covariate")

    X = []
    for i, row in enumerate(covariates):
        if len(row) != d:
            raise ValueError("all covariate rows must have the same length")
        clean_row = []
        for j, value in enumerate(row):
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"covariate ({i}, {j}) is not numeric")
            value = float(value)
            if not math.isfinite(value):
                raise ValueError(f"covariate ({i}, {j}) is not finite")
            clean_row.append(value)
        X.append(clean_row)
    return X


def assign(
    covariates: list[list[float]],
    group_sizes: dict[str, int] | list[int],
    treatments: list[str] | None = None,
    alpha: float = 0.01,
    max_iterations: int | None = None,
    n_mc: int = 10000,
    rng_seed: int | None = None,
) -> list[str]:
    """Assign units to treatments via Euclidean rerandomization.

    Parameters
    ----------
    covariates : list[list[float]]
        n x d matrix of covariate values (one row per unit).
    group_sizes : dict[str, int] or list[int]
        If a dict, maps treatment name -> arm size.  If a list,
        pair it with *treatments* to name the arms.  Must sum to n.
    treatments : list[str] or None
        Arm labels when *group_sizes* is a list.  Ignored when
        *group_sizes* is a dict.
    alpha : float
        Acceptance probability (fraction of random assignments accepted).
        Smaller means stricter balance.  Default 0.01.
    max_iterations : int or None
        Safety cap on rerandomization attempts.  None = no cap (the
        expected number of iterations is 1/alpha).
    n_mc : int
        Monte-Carlo finite randomizations used to estimate the acceptance
        threshold.
    rng_seed : int or None
        Seed for the isolated random.Random instance.  If None, the
        instance is initialized without a fixed seed.

    Returns
    -------
    list[str]
        Treatment label for each unit (length n).
    """
    rng = random.Random(rng_seed)

    if isinstance(group_sizes, dict):
        treatments = list(group_sizes.keys())
        sizes = [group_sizes[t] for t in treatments]
    else:
        sizes = list(group_sizes)
        if treatments is None:
            raise ValueError("treatments must be provided when group_sizes is a list")
        treatments = list(treatments)

    X_raw = _validated_covariates(covariates)
    n = len(X_raw)

    if n_mc < 1:
        raise ValueError("n_mc must be at least 1")
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha must be between 0 and 1")
    if max_iterations is not None and max_iterations < 1:
        raise ValueError("max_iterations must be at least 1")
    if len(sizes) != len(treatments):
        raise ValueError("group_sizes and treatments must have the same length")
    if len(set(treatments)) != len(treatments):
        raise ValueError("treatment labels must be unique")
    if any(isinstance(s, bool) or not isinstance(s, int) for s in sizes):
        raise ValueError("every arm size must be an integer")
    if sum(sizes) != n:
        raise ValueError(f"group sizes sum to {sum(sizes)}, but there are {n} units")
    if len(sizes) < 2:
        raise ValueError("need at least two treatment arms")
    if any(s < 1 for s in sizes):
        raise ValueError("every arm must contain at least one unit")

    X = _standardize(X_raw)
    a = _threshold(X, sizes, treatments, alpha, n_mc, rng)

    attempts = 0
    last_q = None
    while max_iterations is None or attempts < max_iterations:
        w = _random_assignment(n, sizes, treatments, rng)
        attempts += 1
        last_q = _balance_metric(X, w, treatments)
        if last_q <= a:
            return w

    raise RuntimeError(
        "failed to find an acceptable assignment after "
        f"{max_iterations} iterations; last balance metric was {last_q:.6g}, "
        f"threshold was {a:.6g}"
    )
