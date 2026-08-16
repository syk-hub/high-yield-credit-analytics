---

## Dynamic EBP Diagnostics — 2026-08-15

### Objective

Determine whether the apparent relationship between EBP and VIX reflects:

1. persistence in the level of EBP,
2. contemporaneous co-movement in market stress, or
3. genuine leading information about subsequent EBP movements.

### EBP Persistence and Stationarity

For the 1990-01 to 2026-07 market-stress sample:

- Observations: 439
- Mean EBP: 0.0372
- Standard deviation: 0.5911

EBP is highly persistent:

- lag 1 autocorrelation: 0.9226
- lag 3: 0.7807
- lag 6: 0.5456
- lag 12: 0.2262

An Augmented Dickey-Fuller test strongly rejects the unit-root null:

- ADF statistic: -4.8039
- p-value: 0.0001
- AIC-selected lag length: 4

Interpretation:

EBP is highly persistent but does not appear to behave as a unit-root process
over this sample. High persistence alone therefore does not justify
automatically differencing the series.

### One-Month-Ahead EBP Level Models

Three nested models were estimated using HAC standard errors.

#### Model 1: EBP(t+1) ~ EBP(t)

- EBP coefficient: 0.9229
- p-value: < 0.001
- R-squared: 0.851
- Durbin-Watson: 2.085

Current EBP alone explains most of the variation in next month's EBP level.

#### Model 2: EBP(t+1) ~ VIX(t)

- VIX coefficient: 0.0488
- p-value: < 0.001
- R-squared: 0.370
- Durbin-Watson: 0.395

VIX appears predictive when considered alone, but the very low
Durbin-Watson statistic indicates substantial omitted time-series structure.

#### Model 3: EBP(t+1) ~ EBP(t) + VIX(t)

- EBP coefficient: 0.9298
- p-value: < 0.001
- VIX coefficient: -0.0008
- VIX p-value: 0.713
- R-squared: 0.851
- Durbin-Watson: 2.089

Once current EBP is included, VIX contributes essentially no incremental
one-month-ahead information about the EBP level.

Adding VIX also fails to improve R-squared and slightly worsens AIC relative
to the persistence-only model.

### EBP Changes

Monthly EBP changes exhibit very little persistence:

- lag 1 autocorrelation: -0.0834
- lag 3: -0.0573
- lag 6: -0.0283
- lag 12: -0.0496

ADF strongly rejects a unit root in Delta EBP:

- ADF statistic: -9.3517
- p-value: < 0.001

The contemporaneous correlation between monthly changes is:

    Corr(Delta EBP, Delta VIX) = 0.4850

### Contemporaneous Change Model

Model:

    Delta EBP(t) ~ Delta VIX(t)

Results:

- Delta VIX coefficient: 0.0276
- p-value: < 0.001
- R-squared: 0.235
- Durbin-Watson: 2.424

Changes in broad equity-market stress are therefore meaningfully associated
with contemporaneous changes in excess credit compensation.

However, approximately 76.5% of Delta EBP variation remains outside this
one-variable contemporaneous specification.

This unexplained variation should not yet be attributed to intermediary
capacity. It may reflect credit fundamentals, liquidity, monetary
conditions, other financial-state variables, nonlinear crisis effects,
measurement error, or other mechanisms.

### Leading Change Test

Model:

    Delta EBP(t+1) ~ Delta VIX(t)

Results:

- Delta VIX coefficient: 0.0042
- p-value: 0.230
- R-squared: 0.005
- Durbin-Watson: 2.232

The contemporaneous relationship between changes in VIX and EBP does not
translate into meaningful one-month-ahead predictive power in this simple
specification.

### Preliminary Interpretation

The evidence currently distinguishes two functions:

**State measurement**

Market stress variables may help characterize contemporaneous changes in
credit-market conditions.

**State forecasting**

VIX alone provides little evidence of incremental one-month-ahead predictive
information once EBP persistence or timing is handled appropriately.

This distinction should be maintained throughout subsequent research and
eventual product design.

### Research Implication

The empirical target should not be a high-R-squared forecast of the persistent
EBP level.

A more demanding research problem is to explain or anticipate innovations in
excess credit compensation:

    Delta EBP(t)

or economically meaningful transitions into unusually stressed credit states.

Future variables should be admitted incrementally and based on an economic
mechanism rather than through a kitchen-sink specification.

The next variable should therefore be chosen according to the hypothesis it
tests: broad macroeconomic conditions, rates/monetary conditions, liquidity,
or a more direct proxy for intermediary risk-bearing capacity.