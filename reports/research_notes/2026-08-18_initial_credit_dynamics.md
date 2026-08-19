# Initial Credit Dynamics

**Date:** 2026-08-18\
**Project:** `high-yield-credit-analytics` V2\
**Status:** Working research note --- dealer/intermediary conditions
investigation

## Research objective

V2 is testing mechanisms associated with movements in the Excess Bond
Premium (EBP): risk sentiment/uncertainty, interest-rate/macro
conditions, and dealer/intermediary conditions. Prior work found a
strong contemporaneous EBP/VIX relationship, little incremental
contribution from the 10-year Treasury change, and little incremental
contribution from corporate securities fails beyond VIX.

The 2026-08-18 work returned to the more economically direct dealer
variable: **primary dealers' net positions in below-investment-grade
corporate securities**. No composite intermediary-capacity measure is
being constructed at this stage.

## HY dealer net-position construction

NY Fed Primary Dealer Statistics were previously acquired and audited
across reporting periods.

**Apr 2013--Dec 2014:** direct below-investment-grade corporate
net-position series `PDPOSCSBND-BEL`.

**Jan 2015 onward:** the below-investment-grade position concept is
reported in four maturity buckets:

-   `PDPOSCSBND-BELL13`
-   `PDPOSCSBND-BELG13`
-   `PDPOSCSBND-BELG5L10`
-   `PDPOSCSBND-BELG10`

The post-2015 total is reconstructed as:

`HY_DEALER_NET_POSITION_MILLIONS = sum(four maturity buckets)`

This is **not** Securities In minus Securities Out. Securities In/Out
belong to the separate financing/repo branch. The HY series represents
dealers' reported/reconstructed net position in below-investment-grade
corporate securities. Negative observations are retained because dealers
can be net short.

## Standardized weekly history

Four reporting-period datasets were standardized and concatenated while
retaining provenance labels:

-   Apr 2013--Dec 2014: 92 observations
-   Jan 2015--Dec 2021: 365 observations
-   Jan 2022--Jun 2024: 130 observations
-   Jul 2024 onward: 110 observations

The resulting weekly series contains:

-   **697 observations**
-   **2013-04-03 through 2026-08-05**
-   **0 missing values**
-   **0 duplicate dates**

The `REPORTING_REGIME` labels refer to NY Fed reporting/data-provenance
periods, not economic or market regimes.

## Monthly construction

HY dealer net position is a **stock/inventory measure as of the
reporting date**. The baseline monthly transformation therefore uses the
**last weekly observation in each calendar month**, rather than the
monthly mean used for cumulative weekly fails.

Initial aggregation produced 161 calendar months from Apr 2013 through
Aug 2026:

-   104 months with 4 weekly observations
-   56 months with 5 weekly observations
-   1 month with 1 weekly observation

The one-observation month was Aug 2026. The Aug 5 observation is a valid
weekly stock observation but not a month-end proxy for the incomplete
month, so Aug 2026 was excluded.

The saved monthly dataset contains **160 complete months, Apr 2013--Jul
2026**.

## Monthly level diagnostics

Monthly month-end HY dealer net position:

-   N = 160
-   mean = 3,183.43m
-   standard deviation = 2,204.69m
-   minimum = -3,525m
-   median = 3,035.5m
-   maximum = 8,283m

Autocorrelation:

-   lag 1 = **0.7514**
-   lag 3 = **0.6880**
-   lag 6 = **0.5799**
-   lag 12 = **0.2812**

ADF test:

-   statistic = **-2.8485**
-   p = **0.051676**

The level series is persistent and the unit-root evidence is borderline.
A p-value of .0517 should not be treated as substantively different from
a value just below .05. The level series was therefore not used as the
baseline against `ΔEBP`.

A log transformation is inappropriate because net positions can
legitimately be negative.

## Monthly change diagnostics

The baseline transformation is:

`D_HY_DEALER_POSITION = Δ(month-end HY dealer net position)`

Diagnostics:

-   N = 159
-   mean = -23.67m
-   standard deviation = 1,554.66m
-   minimum = -5,622m
-   median = 131m
-   maximum = 5,234m

Autocorrelation:

-   lag 1 = **-0.4172**
-   lag 3 = **0.0880**
-   lag 6 = **0.0959**
-   lag 12 = **0.1154**

ADF test:

-   statistic = **-13.5958**
-   p \< **0.001**

First differencing clearly removes the persistence problem. Monthly
changes in HY dealer net position are therefore the baseline
inventory/risk-absorption variable. The substantial negative lag-1
autocorrelation indicates short-run reversal and is relevant to later
timing tests.

## Common-sample EBP / VIX / HY dealer-position diagnostics

After month-end alignment with the existing EBP/VIX dataset, the common
sample contains **159 observations from May 2013 through Jul 2026**.

Contemporaneous correlations:

                                 ΔEBP      ΔVIX   ΔHY Dealer Position
  ------------------------- --------- --------- ---------------------
  **ΔEBP**                     1.0000    0.4964               -0.1325
  **ΔVIX**                     0.4964    1.0000               -0.2182
  **ΔHY Dealer Position**     -0.1325   -0.2182                1.0000

The raw signs are economically coherent with an
inventory/risk-absorption interpretation: months with rising EBP or VIX
tend to coincide with reductions in dealer HY net positions. These
correlations are modest and are not interpreted causally.

## Common-sample HAC comparison

Two contemporaneous HAC models with three lags were estimated on the
same 159-month sample.

### VIX-only benchmark

`ΔEBP ~ ΔVIX`

-   N = **159**
-   `ΔVIX` coefficient = **0.022405**
-   `ΔVIX` p = **0.000526**
-   R² = **0.246383**

### VIX + HY dealer position

`ΔEBP ~ ΔVIX + ΔHY Dealer Position`

-   `ΔVIX` coefficient = **0.022155**
-   `ΔVIX` p = **0.000877**
-   `ΔHY Dealer Position` coefficient = **-0.00000342**
-   `ΔHY Dealer Position` p = **0.680141**
-   R² = **0.246995**

Incremental R² from adding the dealer-position variable:

**0.000612**

Monthly changes in HY dealer net positions therefore add only about
**0.06 percentage points** of contemporaneous explanatory power beyond
VIX in this baseline specification. The modest raw negative
EBP/dealer-position correlation largely disappears as an independent
signal after controlling for VIX.

## Intermediary evidence to date

Two distinct NY Fed intermediary-condition candidates have now been
tested.

### Corporate securities fails

Working interpretation: **settlement/intermediation stress or market
friction**.

Baseline result:

-   weak unconditional relationship with `ΔEBP`;
-   HAC coefficient not significant after controlling for `ΔVIX` (p =
    .121);
-   incremental common-sample R² ≈ **0.0080**.

### HY dealer net positions

Working interpretation: **dealer inventory / risk absorption in
below-investment-grade corporate credit**.

Baseline result:

-   modest negative raw correlation with `ΔEBP` (-0.1325);
-   HAC coefficient not significant after controlling for `ΔVIX` (p =
    .680);
-   incremental common-sample R² ≈ **0.0006**.

Neither variable currently provides convincing incremental
contemporaneous monthly explanatory power for `ΔEBP` beyond `ΔVIX`.

## Current interpretation

The evidence does **not** establish that intermediary conditions are
irrelevant to EBP. The tests so far are narrower: linear,
contemporaneous, monthly, based on first differences, and limited to
observable primary-dealer measures.

Intermediary effects could operate through levels, nonlinear stress
states, interactions, lag structures, other intermediaries, or variables
not represented by the current NY Fed measures. At the same time, the
negative baseline results should be respected rather than forcing these
variables into an intermediary-capacity composite.

A plausible emerging pattern is that broad risk stress captured by VIX
co-moves with several market-intermediation responses: VIX rises as EBP
rises, corporate fails tend to increase with VIX, and HY dealer net
positions tend to decline with VIX. The dealer variables tested so far,
however, provide little additional contemporaneous monthly information
for EBP after VIX is included.

## Next research question

Before closing the intermediary branch, consider one theoretically
motivated dynamic test:

> **Do changes in HY dealer positions lead EBP, respond to EBP, or
> primarily move contemporaneously with broader risk conditions?**

A limited lead/lag diagnostic is preferable to indiscriminately adding
more variables or specifications. If timing contains no meaningful
additional signal, the intermediary branch can be closed as a documented
negative baseline result rather than constructing an unsupported
composite.
