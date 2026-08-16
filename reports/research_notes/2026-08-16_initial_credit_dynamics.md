# Initial Credit Dynamics

**Date:** 2026-08-16\
**Project:** `high-yield-credit-analytics` V2
**Status:** Working research note --- intermediary conditions
investigation in progress

## Research objective

V2 is investigating mechanisms associated with movements in the Federal
Reserve's Excess Bond Premium (EBP), with particular attention to three
candidate channels:

1.  risk sentiment / uncertainty;
2.  interest-rate / macro conditions; and
3.  dealer/intermediary conditions.

The current work is exploratory and diagnostic. Contemporaneous
relationships are not being interpreted as causal, and reporting-regime
changes are being preserved rather than forcing structurally different
series into artificial continuity.

## EBP diagnostics

Monthly changes in EBP (`ΔEBP`) were examined over 438 observations.

-   Mean `ΔEBP`: -0.0013
-   Standard deviation: 0.2327
-   Autocorrelation:
    -   lag 1: -0.0834
    -   lag 3: -0.0573
    -   lag 6: -0.0283
    -   lag 12: -0.0496
-   ADF statistic: -9.3517
-   ADF p-value: approximately 0

These diagnostics support working with changes in EBP for the current
mechanism analysis.

## Risk sentiment / uncertainty

The contemporaneous correlation between `ΔEBP` and `ΔVIX` is **0.4850**.

A HAC regression,

`ΔEBP ~ ΔVIX`

produced:

-   `ΔVIX` coefficient: **0.0276**
-   p-value: **\< .001**
-   R²: **0.235**

A simple predictive regression,

`ΔEBP(t+1) ~ ΔVIX(t)`

produced:

-   coefficient: **0.0042**
-   p-value: **.230**
-   R²: **.005**

The current interpretation is that changes in VIX and EBP have a
substantial contemporaneous relationship, but `ΔVIX(t)` does not
meaningfully predict `ΔEBP(t+1)` in this simple monthly specification.

## Treasury-rate diagnostic

The observed correlations were:

-   `corr(ΔEBP, Δ10Y Treasury) = -0.1251`
-   `corr(ΔVIX, Δ10Y Treasury) = -0.1264`

A HAC regression,

`ΔEBP ~ ΔVIX + Δ10Y`

produced:

-   `ΔVIX`: **0.0272**, p \< .001
-   `Δ10Y`: **-0.0695**, p = .139
-   R²: **0.239**

Adding the 10-year Treasury change therefore increased explanatory power
only marginally relative to the VIX-only specification.

## Dealer/intermediary conditions

The next mechanism under investigation is dealer/intermediary
conditions. The working concept is broader than a single "balance-sheet
capacity" variable. Candidate measures currently represent different
dimensions of intermediation:

-   **HY dealer net positions:** dealer inventory / risk absorption in
    below-investment-grade corporate bonds.
-   **Corporate fails:** potential settlement/intermediation stress or
    market frictions.
-   **Corporate repo financing:** financing/balance-sheet activity,
    subject to significant post-2021 public-data limitations.

No composite intermediary-capacity index has been constructed.
Individual measures will be evaluated before determining whether a
common factor or composite is economically and empirically defensible.

## HY dealer net positions

NY Fed Primary Dealer Statistics were collected with reporting regimes
explicitly preserved.

### 2013--2014

Direct below-investment-grade corporate net-position series:

`PDPOSCSBND-BEL`

-   92 weekly observations
-   2013-04-03 through 2014-12-31

### 2015 onward

Below-investment-grade positions are reported in four maturity buckets:

-   `PDPOSCSBND-BELL13`
-   `PDPOSCSBND-BELG13`
-   `PDPOSCSBND-BELG5L10`
-   `PDPOSCSBND-BELG10`

The working total is reconstructed as:

`HY_DEALER_NET_POSITION_MILLIONS = sum(four maturity buckets)`

No dates were missing any of the four required buckets.

Reconstructed samples:

-   2015--2021: 365 observations
-   2022--Jun 2024: 130 observations
-   Jul 2024 onward: 110 observations through 2026-08-05

The 2014/2015 reporting boundary was inspected rather than assumed
continuous:

-   2014-12-31: 5,712m
-   2015-01-07: 5,428m

The numerical transition appears plausible, but the reporting boundary
remains documented.

## Corporate repo financing

For the earlier NY Fed reporting regimes, the relevant concepts were
defined from FR 2004 reporting definitions:

-   **Repo:** Securities Out → Repurchase Agreements
-   **Reverse repo:** Securities In → Reverse Repurchase Agreements

The analysis does not sum all Securities In/Out financing categories.

Derived measures are:

`GROSS_CORP_REPO_MILLIONS = repo + reverse_repo`

`NET_CORP_REPO_BORROWING_MILLIONS = repo - reverse_repo`

### 2013--2014

Official aggregate corporate series were used:

-   Reverse repo: `PDSIRRA-CD`
-   Repo: `PDSORA-CD`

The maturity fields were not added to the aggregate because `-CD` is
itself the aggregate series.

There are 92 weekly observations.

Example, 2014-12-31:

-   repo: 40,845m
-   reverse repo: 9,155m
-   gross: 50,000m
-   net borrowing: 31,690m

### 2015--2021

The same aggregate concepts and series IDs continued.

-   365 observations
-   2015-01-07 through 2021-12-29

Example, 2021-12-29:

-   repo: 41,936m
-   reverse repo: 10,504m
-   gross: 52,440m
-   net borrowing: 31,432m

The 2014/2015 boundary was inspected and appeared numerically plausible.

## 2022 corporate repo reporting change

Beginning in January 2022, corporate repo and reverse-repo reporting
becomes substantially more granular. Each side is decomposed into:

-   Uncleared Bilateral
-   Cleared Bilateral
-   GCF & Tri-Party

The component structure includes Specified, General, Sponsored where
applicable, and maturity categories. Twenty-one component series exist
on each of the repo and reverse-repo sides.

The six top combined NY Fed API endpoints for Jan 2022--Jun 2024 were
inspected.

### Structural validation

All six groups cover:

-   **130 weekly dates**
-   **2022-01-05 through 2024-06-26**

Requested component counts were present on every date:

-   Uncleared Bilateral: 6 components
-   Cleared Bilateral: 9 components
-   GCF & Tri-Party: 6 components

There were:

-   0 duplicate series/date rows
-   0 dates with structurally incomplete component sets

### Disclosure suppression

The API and published NY Fed tables contain `*` values in required
components. These are distinct from explicitly reported `$0`
observations and therefore were not treated as zero.

Suppression was found in multiple categories, including General
uncleared-bilateral components and selected GCF/Tri-Party components.

A full observability diagnostic across all six endpoint groups found:

    Suppressed components per date   Number of dates
  -------------------------------- -----------------
                                 2                 7
                                 3                29
                                 4                27
                                 5                36
                                 6                23
                                 7                 8

**Fully observable dates: 0 / 130.**

Accordingly, an exact bottom-up corporate repo or reverse-repo total
cannot be reconstructed for Jan 2022--Jun 2024 from the public component
data without imposing assumptions on suppressed observations.

### July 2024 onward

Manual inspection of the Jul 2024+ NY Fed reporting regime shows that
the three-category structure remains in place:

-   Uncleared Bilateral
-   Cleared Bilateral
-   GCF & Tri-Party

Disclosure suppression (`*`) also persists. For example, General
Overnight & Continuing observations within Uncleared Bilateral can be
suppressed while corresponding Specified observations are reported
numerically.

### Provenance decision

For post-2021 corporate repo financing:

-   do **not** replace `*` with zero;
-   do **not** impute suppressed observations at this stage;
-   do **not** construct a false exact aggregate;
-   do **not** splice a reconstructed post-2021 series onto the pre-2022
    aggregate history.

The exact 2013--2021 corporate financing history remains potentially
useful as a historical diagnostic or robustness measure, but it is not
currently suitable as a continuous full-sample intermediary variable
through 2026.

## Corporate fails: next candidate

A cursory inspection of NY Fed Corporate Debt fails data indicates that
both:

-   Fails to Receive
-   Fails to Deliver

appear to be available beginning in 2001. Initial inspection of the
beginning and end of the available date range did not reveal `*`
suppression or obvious missing observations.

This has **not yet undergone the formal provenance and completeness
audit** applied to the other dealer series.

Economically, corporate fails should initially be treated as a candidate
measure of **settlement/intermediation stress or market frictions**, not
as a pure balance-sheet-capacity measure. Fails to Receive and Fails to
Deliver should remain separate until their definitions, reporting
history, correlation, distributions, and behavior during stress periods
have been examined.

## Current working interpretation

The intermediary investigation is therefore evolving from a narrow
"balance-sheet capacity" concept toward a broader **dealer/intermediary
conditions** mechanism.

The current candidate dimensions are:

  -----------------------------------------------------------------------
  Measure                 Candidate               Current status
                          interpretation          
  ----------------------- ----------------------- -----------------------
  HY dealer net positions Dealer inventory /      Reconstructed;
                          credit-risk absorption  reporting boundaries
                                                  documented

  Corporate repo          Financing /             Exact through 2021;
  financing               balance-sheet activity  post-2021 exact
                                                  reconstruction blocked
                                                  by suppression

  Corporate fails         Settlement /            Promising; provenance
                          intermediation stress   audit still required
                          and frictions           
  -----------------------------------------------------------------------

A composite intermediary measure is **not yet justified**. The
individual variables should first demonstrate coherent economic behavior
and useful relationships with EBP. Only then should a standardized
composite, PCA-derived factor, or other latent intermediary-conditions
measure be considered.

## Next research step

Audit the NY Fed Corporate Debt Fails to Receive and Fails to Deliver
series beginning in 2001:

1.  identify exact series IDs and reporting regimes;
2.  verify date coverage and frequency;
3.  test for missing and disclosure-suppressed observations;
4.  document definition/reporting changes;
5.  preserve Fails to Receive and Fails to Deliver separately for
    initial diagnostics.

No intermediary composite should be constructed before this audit and
the subsequent individual-series analysis are complete.
