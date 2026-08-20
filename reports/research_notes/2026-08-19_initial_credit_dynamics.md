# Initial Credit Dynamics

**Date:** 2026-08-19\
**Project:** `high-yield-credit-analytics` V2\
**Status:** Working research note --- intermediary-capacity branch
closure

## Research objective

V2 has been testing whether movements in the Excess Bond Premium (EBP)
are associated with risk sentiment/uncertainty, interest-rate/macro
conditions, and dealer/intermediary conditions.

Prior work established a substantial contemporaneous relationship
between monthly changes in EBP and VIX. Changes in the 10-year Treasury
yield added little incremental explanatory power. Corporate securities
fails and below-investment-grade dealer net positions were subsequently
tested as intermediary measures; neither provided convincing incremental
contemporaneous monthly explanatory power for `ΔEBP` beyond `ΔVIX`.

On 2026-08-19, the intermediary-capacity branch received one final
literature-motivated test using a Kargar-inspired broker-dealer
wealth-share construction. This is not a replication of Kargar's full
heterogeneous intermediary factor (HIFac). It is a bounded test of
whether a more structural balance-sheet measure performs better than the
NY Fed operational/dealer-position proxies.

## Kargar-inspired intermediary construction

The V2 state variable is:

`BD_WEALTH_SHARE = BD_EQUITY / (BD_EQUITY + BANK_EQUITY)`

Six quarterly Federal Reserve Financial Accounts series were downloaded
from FRED.

### Securities brokers and dealers

-   `BOGZ1FL664090005Q` --- total financial assets
-   `BOGZ1FL664190005Q` --- total liabilities
-   `BOGZ1FL663190005Q` --- miscellaneous liabilities

### Commercial banking

-   `BOGZ1FL764090005Q` --- total financial assets
-   `BOGZ1FL764190005Q` --- total liabilities
-   `BOGZ1FL763193005Q` --- miscellaneous liabilities

The equity measures are constructed as:

`BD_EQUITY = BD_ASSETS - (BD_LIABILITIES - BD_MISC_LIABILITIES)`

`BANK_EQUITY = BANK_ASSETS - (BANK_LIABILITIES - BANK_MISC_LIABILITIES)`

The derived dataset retains all six source components, both constructed
equity measures, and the final wealth-share variable so that the
provenance chain remains auditable.

This measure is conceptually distinct from HY dealer net positions
(inventory/risk absorption), corporate securities fails
(settlement/intermediation friction), and corporate repo financing
(financing activity).

## Input coverage and missingness

Each of the six FRED inputs initially contained 322 dated observations
from 1945 Q4 through 2026 Q1, with 18 missing/non-numeric observations.

The missingness pattern was identical across all six inputs:

-   304 dates had all six inputs;
-   18 dates had all six inputs missing.

The missing quarters occur during 1946--1951. These historical gaps were
not interpolated.

The resulting constructed dataset contains 304 fully observed dates.
Both constructed broker-dealer equity and commercial-bank equity remain
positive throughout the retained observations.

## Wealth-share sanity check

Across the full constructed history:

-   mean BD wealth share = **0.2300**
-   standard deviation = **0.1789**
-   minimum = **0.0177**
-   median = **0.2314**
-   maximum = **0.5770**

Because the 1945--2026 history contains substantial structural change,
the full-history distribution is not treated as a homogeneous economic
sample.

For the modern 1990 Q1--2026 Q1 sample:

-   N = **145**
-   mean = **0.4008**
-   standard deviation = **0.0775**
-   minimum = **0.2253**
-   median = **0.4094**
-   maximum = **0.5770**

Quarterly autocorrelation:

-   lag 1 = **0.9563**
-   lag 2 = **0.9191**
-   lag 4 = **0.8500**
-   lag 8 = **0.6773**

Selected observations:

-   1990 Q1 = **0.2308**
-   2000 Q1 = **0.5002**
-   2007 Q2 = **0.5770**
-   2009 Q1 = **0.3528**
-   2020 Q1 = **0.3328**
-   2024 Q1 = **0.4281**
-   2026 Q1 = **0.4291**

The sharp decline between the pre-crisis 2007 peak and 2009 is
qualitatively consistent with a substantial contraction in the relative
broker-dealer balance-sheet/equity footprint around the financial
crisis.

## Quarterly EBP/VIX construction and alignment

The Financial Accounts variable is quarterly and was not forward-filled
into monthly observations.

The existing monthly market data were converted to quarterly frequency:

-   EBP: last monthly EBP observation within each quarter;
-   VIX: mean monthly VIX within each quarter.

Quarter-to-quarter changes were then calculated.

The initial market construction contained 147 calendar quarters from
1990 Q1 through 2026 Q3. The final quarter contained only one monthly
observation and was excluded. This left **146 complete market quarters
through 2026 Q2**.

The Financial Accounts observations use quarter-start date labels, while
the market series uses quarter-end labels. The datasets were therefore
aligned using calendar-quarter `Period` keys rather than raw dates.

The common Kargar/market sample contains:

-   **145 quarters**
-   **1990 Q1--2026 Q1**

## Level diagnostics

Contemporaneous correlations on the 145-quarter common sample:

  Variable pair                   Correlation
  ----------------------------- -------------
  EBP level / VIX mean             **0.6662**
  EBP level / BD wealth share     **-0.0277**
  VIX mean / BD wealth share       **0.0564**

Quarter-end EBP autocorrelation:

-   lag 1 = **0.7808**
-   lag 2 = **0.5402**
-   lag 4 = **0.2395**

BD wealth-share autocorrelation:

-   lag 1 = **0.9563**
-   lag 2 = **0.9191**
-   lag 4 = **0.8500**

ADF tests:

-   quarter-end EBP: statistic = **-4.6716**, p = **0.000095**
-   BD wealth share: statistic = **-2.4646**, p = **0.124319**

Quarter-end EBP rejects the unit-root null in this sample. The
broker-dealer wealth-share level does not and is extremely persistent.

The contemporaneous level correlation between EBP and BD wealth share is
essentially zero. The primary V2 test was therefore predictive rather
than a naive contemporaneous level-on-level regression.

## Kargar-inspired predictive test

The predictive specification asks whether broker-dealer wealth share at
quarter `t` predicts the change in EBP over the following quarter:

`ΔEBP(t+1) ~ BD_WEALTH_SHARE(t)`

A VIX benchmark and combined model were estimated using HAC standard
errors with four lags.

### BD wealth share only

N = **144**

-   coefficient = **0.925219**
-   p = **0.023625**
-   R² = **0.032471**

### VIX only

-   VIX coefficient = **-0.020869**
-   p = **0.000366**
-   R² = **0.129653**

### VIX + BD wealth share

-   VIX coefficient = **-0.021522**
-   VIX p = **0.000129**
-   BD wealth-share coefficient = **1.032154**
-   BD wealth-share p = **0.014671**
-   R² = **0.169936**

Incremental R² from adding BD wealth share:

**0.040283**

The level wealth-share variable is statistically significant in this
predictive specification and raises in-sample explanatory power by
approximately **4.0 percentage points** beyond the VIX benchmark. This
is materially stronger than the earlier corporate-fails and
HY-dealer-position results.

However, the extreme persistence and failed ADF stationarity test of the
wealth-share level require caution.

## Stationary robustness test

A deliberately limited robustness test replaced the highly persistent
wealth-share level with its quarterly first difference:

`ΔBD_WEALTH_SHARE(t)`

Stationarity diagnostics:

-   N = **143**
-   ADF statistic = **-12.8921**
-   ADF p \< **0.001**

The predictive robustness specification was:

`ΔEBP(t+1) ~ VIX(t) + ΔBD_WEALTH_SHARE(t)`

Results:

-   VIX coefficient = **-0.021444**
-   VIX p = **0.001554**
-   ΔBD wealth-share coefficient = **-0.967584**
-   ΔBD wealth-share p = **0.630130**
-   R² = **0.131781**

The predictive signal does not survive the stationary transformation.
The intermediary coefficient also changes sign relative to the level
specification.

Accordingly, the significant level result is treated as **suggestive
rather than robust evidence**.

## Intermediary evidence across V2

Three conceptually distinct intermediary measures have now been
evaluated.

### 1. Corporate securities fails

Interpretation: settlement/intermediation stress or market friction.

Baseline result:

-   weak unconditional relationship with `ΔEBP`;
-   insignificant after controlling for `ΔVIX` (`p = .121`);
-   incremental common-sample R² ≈ **0.0080**.

### 2. HY dealer net positions

Interpretation: dealer inventory / risk absorption in
below-investment-grade corporate credit.

Baseline result:

-   raw correlation with `ΔEBP` = **-0.1325**;
-   insignificant after controlling for `ΔVIX` (`p = .680`);
-   incremental common-sample R² ≈ **0.0006**.

### 3. Kargar-style broker-dealer wealth share

Interpretation: relative structural intermediary risk-bearing capacity /
balance-sheet composition.

Predictive level result:

-   significant after controlling for VIX (`p = .0147`);
-   incremental R² ≈ **0.0403**.

Robustness result:

-   wealth-share level is extremely persistent and fails the ADF
    stationarity test (`p = .1243`);
-   first-differenced wealth share is stationary;
-   predictive coefficient on the stationary change is insignificant
    (`p = .6301`);
-   coefficient changes sign.

The Kargar-inspired measure is therefore more empirically interesting
than the operational NY Fed dealer proxies, but current V2 evidence does
not support treating it as a robust predictor of subsequent EBP changes.

## Research decision: close intermediary-capacity branch

The intermediary-capacity search is closed.

V2 will **not**:

-   construct an intermediary-capacity composite;
-   add further intermediary variables in search of significance;
-   attempt a full HIFac replication;
-   impute suppressed post-2021 corporate repo components;
-   continue specification mining after the failed stationary robustness
    test.

The appropriate conclusion is:

> Observable intermediary measures show different relationships with
> credit conditions depending on what aspect of intermediation they
> capture. Settlement fails and HY dealer inventory provide little
> incremental contemporaneous monthly information for EBP beyond VIX. A
> Kargar-inspired relative broker-dealer wealth measure produces a
> materially stronger predictive level result, but that result is not
> robust to a stationary transformation of the highly persistent
> predictor. The evidence is therefore suggestive, not sufficient to
> support a standalone intermediary-capacity factor in V2.

## Methodological takeaway

The Kargar-inspired exercise produces a useful V2 research-quality
result even though the robustness test fails.

A statistically significant coefficient was not accepted automatically.
The predictor's time-series properties were examined, extreme
persistence was identified, and a stationary transformation was used as
a bounded robustness test. When the result disappeared, the
interpretation was downgraded rather than preserved through additional
specification searching.

This is consistent with the V2 standard: provenance, economic
interpretation, statistical diagnostics, and negative results take
precedence over manufacturing a preferred narrative.

## Current stopping point

The intermediary-capacity branch is complete.

The next V2 work should focus on the smallest remaining set of analyses
and documentation required to produce a coherent final research product.
New mechanism branches should not be opened unless necessary to the
final V2 argument.
