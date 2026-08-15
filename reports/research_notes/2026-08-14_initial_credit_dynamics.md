# Initial Credit Dynamics — 2026-08-14

## Purpose

Begin empirical analysis of the long-history Gilchrist-Zakrajšek credit
dataset and determine whether excess credit-risk compensation behaves
differently from default-related credit conditions and broad market stress.

This is an exploratory research note. Results below are descriptive or
preliminary and should not yet be interpreted causally.

---

## Data Architecture Established

### Sample A — Core Credit Sample

Period: 1973-01 to 2026-07  
Observations: 643 monthly observations

Variables:

- GZ corporate credit spread (`gz_spread`)
- Excess Bond Premium (`ebp`)
- model-implied recession probability (`est_prob` in raw source)

No missing observations were found in the three source variables.

### Sample B — Macro Credit Sample

Added:

- unemployment rate
- NBER recession indicator
- monthly mean 10-Year Treasury yield

The original 643 GZ observations were retained.

Known missing observations:

- unemployment: 2025-10 and 2026-07
- recession indicator: 2026-07
- 10-Year Treasury: no missing monthly observations

The July 2026 macro gaps reflect an endpoint/vintage mismatch.
The October 2025 unemployment observation is an internal source-series
missing observation.

### Sample C — Market Stress Sample

Period: 1990-01 to 2026-07  
Observations: 439 monthly observations

Added:

- monthly mean VIX

VIX contains no missing monthly observations within Sample C.

---

## Important Semantic Correction

The raw Federal Reserve variable `est_prob` was initially interpreted as an
estimated default probability.

This was incorrect.

`est_prob` represents a model-implied U.S. recession probability associated
with the Federal Reserve EBP update.

The raw source file remains unchanged. Downstream analysis refers to this
variable as `recession_probability`.

The spread decomposition used in exploratory analysis is:

    default_related_component = gz_spread - ebp

This is a spread component and should not be confused with a probability of
default.

---

## Initial Spread Decomposition

Full-sample means:

- GZ spread: 1.737
- default-related component: 1.672
- EBP: 0.065

Selected correlations:

- Corr(GZ spread, default-related component): 0.815
- Corr(GZ spread, EBP): 0.744
- Corr(default-related component, EBP): 0.218

The relatively low correlation between EBP and the default-related component
suggests that the two components contain substantially different variation.

---

## Recession-State Result

Average GZ spread:

- non-recession months: 1.627
- recession months: 2.593

Average default-related component:

- non-recession: 1.659
- recession: 1.778

Average EBP:

- non-recession: -0.032
- recession: 0.815

Approximately 88% of the difference between mean recession and non-recession
GZ spreads is mechanically attributable to the difference in mean EBP.

This is a decomposition of sample means, not a causal estimate.

---

## Recession-Episode Heterogeneity

The EBP fraction of the average GZ spread varies substantially across
recessions:

| Recession | EBP fraction |
|---|---:|
| 1973–75 | 30.6% |
| 1980 | 1.8% |
| 1981–82 | 36.3% |
| 1990–91 | 14.3% |
| 2001 | 26.1% |
| 2008–09 | 36.6% |
| 2020 | 27.5% |

The recession indicator alone therefore does not characterize the magnitude
of excess credit compensation.

A central empirical question is what observable financial and macroeconomic
states help explain this heterogeneity.

---

## EBP and Broad Market Stress

Sample C correlations:

- Corr(EBP, VIX): 0.666
- Corr(GZ spread, EBP): 0.839
- Corr(GZ spread, VIX): 0.690

EBP and VIX therefore share substantial variation but are not empirically
identical.

An exploratory contemporaneous regression was estimated:

    GZ spread ~ EBP + VIX

using HAC standard errors with three lags.

Results:

- EBP coefficient: 1.118
- VIX coefficient: 0.0309
- R²: 0.736
- both coefficients statistically significant

This regression is diagnostic rather than a candidate final specification.
EBP is mechanically embedded in the GZ spread decomposition, and the
Durbin-Watson statistic (0.166) indicates substantial residual serial
correlation.

---

## Emerging Research Direction

The empirical object of interest should increasingly become EBP rather than
the level of the GZ spread.

The developing question is:

> What observable market and macro-financial states explain variation in
> excess credit compensation, and can those states help identify periods in
> which credit-market risk-bearing conditions become unusually restrictive?

The current evidence does not identify intermediary capacity.

Instead, it establishes three preliminary facts worth investigating:

1. excess credit compensation behaves differently from the default-related
   spread component;
2. its importance varies substantially across recession episodes; and
3. EBP overlaps with, but is not equivalent to, broad market stress measured
   by VIX.

---

## Next Empirical Steps

1. Treat EBP as the primary variable to explain.
2. Examine persistence and time-series properties before further levels
   regressions.
3. Compare levels, changes, and lagged specifications.
4. Determine whether VIX retains explanatory or predictive information for
   EBP.
5. Add macro/rates variables incrementally rather than using a kitchen-sink
   specification.
6. Distinguish contemporaneous explanation from genuine out-of-sample
   forecasting.
7. Delay intermediary-capacity interpretation until empirical evidence can
   distinguish that mechanism from general risk aversion or market stress.