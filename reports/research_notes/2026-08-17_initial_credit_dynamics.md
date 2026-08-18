# Initial Credit Dynamics

**Date:** 2026-08-17\
**Project:** `high-yield-credit-analytics` V2\
**Status:** Working research note --- intermediary conditions
investigation

## Research objective

V2 is investigating mechanisms associated with movements in the Excess
Bond Premium (EBP): risk sentiment/uncertainty, interest-rate/macro
conditions, and dealer/intermediary conditions. The intermediary branch
is being developed from individually defensible measures rather than
assuming in advance that a composite intermediary-capacity index is
appropriate.

## Corporate securities fails: provenance audit

NY Fed Primary Dealer Statistics for Corporate Securities Fails to
Receive and Fails to Deliver were audited across five reporting regimes.

-   **Jul 2001--Mar 2013:** Fails to Receive `PDFASCFRA`; Fails to
    Deliver `PDFASCFDA`; 613 weekly observations.
-   **Apr 2013--Dec 2014:** Fails to Receive `PDFTR-CS`; Fails to
    Deliver `PDFTD-CS`; 92 observations.
-   **2015--2021:** `PDFTR-CS` / `PDFTD-CS`; 365 observations.
-   **Jan 2022--Jun 2024:** `PDFTR-CS` / `PDFTD-CS`; 130 observations.
-   **Jul 2024 onward:** `PDFTR-CS` / `PDFTD-CS`; 110 observations
    through 2026-08-05.

The standardized historical dataset contains **1,310 weekly observations
from 2001-07-04 through 2026-08-05**, with zero missing values, zero
duplicate dates, both measures present on every date, and no
disclosure-suppressed `*` observations.

## Definition and 2013 reporting boundary

NY Fed documentation defines Delivery Fails as trades that fail to
settle on schedule. Every fail has two parties: one fails to receive the
security and one fails to deliver it. Fails may arise from outright
purchase/sale transactions or financing transactions such as securities
borrowing and lending. Fails data are cumulative weekly aggregates for
the primary dealer community and are reported at the amount that was to
be paid or received on the scheduled settlement date.

The NY Fed provides an umbrella definition rather than separate
definitions by historical reporting regime.

The March/April 2013 series-ID boundary was inspected numerically. On
2013-03-27, Fails to Deliver were 14,254m and Fails to Receive were
11,255m. On 2013-04-03, the new-ID series reported Fails to Deliver of
14,232m and Fails to Receive of 8,733m.

The evidence supports treating the economic concepts as continuous while
explicitly preserving April 2013 as a reporting/series-ID provenance
boundary.

## Receive versus Deliver relationship

Across the full weekly sample, the level correlation between Fails to
Receive and Fails to Deliver is **0.9514**. The mean Deliver/Receive
ratio is 1.3252 and the median is 1.3165.

The two measures remain strongly related in weekly changes:

**corr(ΔFails Receive, ΔFails Deliver) = 0.8372**

They therefore appear to capture closely related manifestations of the
same settlement/intermediation environment. They should not
automatically be entered together into a regression or summed into a
total-fails measure.

Fails to Deliver was selected as the initial primary candidate; Fails to
Receive remains available as a robustness alternative.

## Economic interpretation

Corporate fails are not being treated as a pure measure of dealer
balance-sheet capacity. The working interpretation is
**settlement/intermediation stress or market friction**. This
distinction matters for any later intermediary-conditions factor or
composite.

## Monthly construction

Because NY Fed fails are cumulative weekly aggregates rather than
point-in-time stocks, the initial monthly transformation uses the **mean
weekly Fails to Deliver during each month**.

The raw aggregation produced 302 calendar months from Jul 2001 through
Aug 2026: 196 months with four weekly observations, 105 with five, and
one incomplete month (Aug 2026) with one observation. The incomplete
month was excluded.

The saved monthly dataset therefore contains **301 complete months, Jul
2001--Jul 2026**.

## Monthly level diagnostics

Monthly mean Fails to Deliver:

-   N = 301
-   mean = 25,592.19m
-   standard deviation = 9,986.88m
-   minimum = 10,413.75m
-   median = 23,507.25m
-   maximum = 81,829.80m

Autocorrelation: lag 1 = 0.8453; lag 3 = 0.7217; lag 6 = 0.5866; lag 12
= 0.4244.

ADF statistic = **-1.9625**, p = **0.303240**.

The level series is highly persistent, and the ADF test does not reject
a unit root. The raw level was therefore not used directly against
`ΔEBP`.

## Monthly change diagnostics

Monthly Fails to Deliver was first-differenced:

`D_FAILS_DELIVER = Δ(monthly mean Fails to Deliver)`

-   N = 300
-   mean = 40.22m
-   standard deviation = 5,554.32m
-   median = -379.50m
-   minimum = -26,737.05m
-   maximum = 18,401.25m

Autocorrelation: lag 1 = -0.2251; lag 3 = 0.0122; lag 6 = -0.0930; lag
12 = 0.1983.

ADF statistic = **-5.5965**, p = **0.000001**.

Differencing substantially reduces persistence and strongly rejects a
unit root. `D_FAILS_DELIVER` is therefore the baseline fails variable
for the current monthly EBP analysis.

## Common-sample EBP / VIX / fails diagnostics

After month-end alignment with the EBP/VIX dataset, the common sample
contains **300 observations from Aug 2001--Jul 2026**, with zero missing
values.

Contemporaneous correlations:

                           ΔEBP     ΔVIX   ΔFails Deliver
  -------------------- -------- -------- ----------------
  **ΔEBP**               1.0000   0.5334           0.0537
  **ΔVIX**               0.5334   1.0000           0.2628
  **ΔFails Deliver**     0.0537   0.2628           1.0000

Corporate fails therefore have almost no unconditional contemporaneous
correlation with `ΔEBP`, although they have a modest positive
relationship with `ΔVIX`. The common-sample ΔEBP/ΔVIX correlation of
0.5334 should not be compared directly with the earlier full-sample
estimate of 0.4850 because the sample is shorter.

## HAC regression: ΔEBP \~ ΔVIX + ΔFails

A contemporaneous HAC regression with three lags was estimated on the
300-month common sample:

`ΔEBP ~ ΔVIX + ΔFails to Deliver`

Results:

-   `ΔVIX` coefficient = **0.0328**, p \< .001
-   `ΔFails Deliver` coefficient = **-4.516e-06**, p = **.121**
-   R² = **0.293**

The fails coefficient is not statistically significant at conventional
levels. The unconditional fails/EBP correlation is slightly positive,
while the coefficient becomes negative after controlling for VIX. This
is consistent with corporate fails sharing some stress variation with
VIX without providing a clear independent positive contemporaneous EBP
signal.

## Common-sample VIX benchmark

To avoid comparing models estimated on different samples, the VIX-only
model was re-estimated on the same 300 observations:

`ΔEBP ~ ΔVIX`

-   N = 300
-   `ΔVIX` coefficient = **0.031412**, p \< .001
-   R² = **0.284505**

Adding `ΔFails Deliver` raises R² by only **0.008034**.

Thus corporate fails add approximately **0.8 percentage points of
contemporaneous explanatory power** beyond VIX in this baseline
specification, while their individual HAC coefficient remains
statistically insignificant.

## Current interpretation

The emerging mechanism evidence is:

-   **Risk sentiment / uncertainty:** strong contemporaneous
    relationship with EBP through VIX.
-   **Interest-rate conditions:** Δ10Y previously added little
    explanatory power after controlling for ΔVIX.
-   **Settlement/intermediation stress:** Corporate Fails to Deliver are
    somewhat associated with VIX but provide little incremental
    contemporaneous explanatory power for ΔEBP.

This is a legitimate negative result. Corporate fails should not be
included in an intermediary composite merely because a clean historical
series is available.

Potential nonlinear, crisis-specific, maximum-fails, or lagged
specifications may later be considered as robustness tests, but they are
not required to rescue the baseline result.

## Next research step

Return to the more economically direct intermediary candidate: **NY Fed
below-investment-grade dealer net positions**.

Next sequence:

1.  transform weekly HY dealer net positions to an appropriate monthly
    measure;
2.  test monthly level stationarity/persistence;
3.  select a defensible transformation;
4.  examine its contemporaneous relationship with `ΔEBP`;
5.  estimate its incremental explanatory contribution relative to
    `ΔVIX`.

No intermediary composite should be constructed until the individual
candidate measures have been evaluated.
