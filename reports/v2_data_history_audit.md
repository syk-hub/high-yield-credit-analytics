# HIGH-YIELD CREDIT ANALYTICS V2
## Module 01 — Data History & Provenance Audit

### Objective

Module 01 establishes the data-history, provenance, access, and methodological
constraints governing High-Yield Credit Analytics V2 before any new regime,
predictive, or machine-learning analysis is undertaken.

The audit determines whether each market and macroeconomic series used in V1
has sufficient legitimate history for its intended V2 analytical purpose,
identifies artificial delivery or licensing restrictions, and documents
whether longer-history alternatives or complementary indicators are required.

A central objective is to prevent short or methodologically incompatible
series from supporting conclusions that exceed the available evidence.

### Scope

The audit covers the principal market and macroeconomic inputs inherited from
V1:

- ICE BofA US High Yield OAS
- ICE BofA US High Yield Effective Yield
- ICE BofA US High Yield Total Return Index
- Cboe VIX
- 10-Year Treasury Constant Maturity Rate
- Effective Federal Funds Rate
- U.S. unemployment rate
- U.S. recession indicator

The audit also evaluates the Federal Reserve Excess Bond Premium (EBP) as a
separate long-history credit-market indicator for V2.

For each series, the review considers data provenance, delivery source,
frequency, units, available history, missing observations, access restrictions,
licensing or redistribution considerations where relevant, and intended V2
analytical use.

Module 01 does not perform regime modeling, predictive modeling, machine
learning, or redesign of the V1 Power BI dashboard. Statistical analysis is
limited to diagnostics necessary to determine whether a proposed data series
is defensible for subsequent V2 research.


## V2 Data History & Provenance Decision Table

| Series | Identifier | Provider | Delivery Source | Frequency | Units | Available Start | History Restriction | V2 Use | Disposition |
|---|---|---|---|---|---|---|---|---|---|
| ICE BofA US HY OAS | BAMLH0A0HYM2 | ICE BofA | FRED | Daily | % | 2023-07-28 | Current FRED delivery limited to recent history | Contemporary HY spread / stress analysis | RETAIN — recent-period only |
| ICE BofA US HY Effective Yield | BAMLH0A0HYM2EY | ICE BofA | FRED | Daily | % | 2023-07-28 | Current FRED delivery limited to recent history | Contemporary HY yield conditions | RETAIN — recent-period only |
| ICE BofA US HY Total Return Index | BAMLHYH0A0HYM2TRIV | ICE BofA | FRED | Daily | Index | 2023-07-28 | Current FRED delivery limited to recent history | Contemporary HY performance / drawdown | RETAIN — recent-period only |
| Excess Bond Premium | — | Federal Reserve | Federal Reserve | Monthly | Percentage points | 1973-01-01 | No comparable recent-history truncation identified | Long-history credit-risk-premium / cycle research | RETAIN — distinct indicator; never splice to HY OAS |
| VIX | VIXCLS | Cboe | FRED | Daily | Index | 1990-01-02 | Long history available | Market risk / volatility / stress context | RETAIN — proprietary input |
| 10Y Treasury | DGS10 | Federal Reserve Board | FRED | Daily | % | 1962-01-02 | Long history available | Risk-free rate / macro-rate context | RETAIN |
| Effective Federal Funds Rate | EFFR | Federal Reserve Bank of New York | FRED | Daily | % | 2000-07-03 | Modern EFFR begins in 2000 | Monetary-policy context | RETAIN — modern-cycle use |
| Unemployment Rate | UNRATE | U.S. Bureau of Labor Statistics | FRED | Monthly | % | 1948-01-01 | No material history restriction; Oct. 2025 genuinely unavailable | Labor-market / macro-cycle context | RETAIN |
| Recession Indicator | USREC | NBER / FRED | FRED | Monthly | Binary | 1854-12-01 | Long history available | Historical recession labeling | RETAIN |



# V2 Data History Audit

## Finding 01 — ICE BofA series truncation is upstream of the V1 pipeline.

The V1 downloader requests `BAMLH0A0HYM2`, `BAMLH0A0HYM2EY`, and `BAMLHYH0A0HYM2TRIV` from FRED without specifying an observation-start parameter.

The July 2026 extraction nevertheless returns only approximately three years of ICE BofA history. Therefore, the observed truncation is not caused by an explicit date restriction in the project's Python downloader. External provenance and delivery restrictions require investigation.

## Finding 02 — FRED imposes a three-year observation window on ICE BofA series

FRED currently states that, beginning in April 2026, the ICE BofA US High Yield
Index Option-Adjusted Spread (`BAMLH0A0HYM2`) will include only three years of
observations. FRED directs users seeking additional history to the underlying
data source, ICE Data Indices, LLC.

The same restriction applies to other ICE BofA series used in V1, including the
HY effective-yield series. This confirms that the approximately July 2023 start
date observed in the July 2026 project extraction is a FRED delivery restriction,
not a Python/API date-configuration error.

Longer historical copies of these series may exist in third-party archives and
public repositories. Their existence does not establish redistribution rights.
Because ICE retains intellectual-property rights over its index data and places
restrictions on redistribution, third-party archived copies should not be treated
as an acceptable provenance solution for a public research portfolio without
separate authorization.

Disposition: retain the current FRED-delivered ICE BofA series as legitimate
recent-history data. Longer-history acquisition remains unresolved pending
evaluation of legitimate ICE access, historical-access mechanisms, and/or a
separately identified long-history credit proxy.

## Finding 03 — Direct ICE access is not presently required

ICE's direct data-access process appears oriented toward institutional and
commercial users and requests organizational information including company,
role, industry, corporate email, and business phone.

For the current public portfolio project, institutional ICE access will not
be pursued unless subsequent research establishes that the full proprietary
ICE history is necessary for a material analytical objective.

The project will retain the FRED-delivered ICE BofA series for analyses that
can be supported by the available three-year window.

Long-cycle and historical-stress research will require evaluation of a
separate, legitimately sourced long-history credit proxy. Any such proxy will
remain explicitly distinct from the ICE BofA US High Yield OAS series and will
not be spliced into the ICE series.

Provisional disposition: Path B, subject to proxy evaluation.

## Finding 04 — Federal Reserve Excess Bond Premium

The Federal Reserve Excess Bond Premium (EBP) is retained as a candidate
long-history credit indicator.

The EBP measures the component of corporate bond credit spreads that is not
directly attributable to expected default risk and is interpreted as a measure
of investor risk appetite or sentiment in corporate credit markets.

The Federal Reserve publishes an official monthly EBP series with history
beginning in 1997.

The EBP is not equivalent to the ICE BofA US High Yield Option-Adjusted
Spread. It differs in bond universe, construction, frequency, and economic
interpretation. It therefore will not be spliced with, relabeled as, or used
as a historical continuation of HY OAS.

Potential V2 use:
- historical credit-risk-appetite analysis
- recession and stress-cycle analysis
- conditional analysis involving credit sentiment
- comparison with contemporary HY OAS where overlapping data permit

Provisional disposition: KEEP as a distinct long-history credit indicator.

## Finding 05 — Moody's Baa–Treasury Spread (BAA10YM)

BAA10YM provides a very long history of U.S. corporate credit spreads,
beginning in April 1953.

The series is calculated by the Federal Reserve Bank of St. Louis as the
spread between the Moody's Seasoned Baa Corporate Bond Yield and the
10-Year Treasury Constant Maturity yield.

BAA10YM is not equivalent to ICE BofA US High Yield OAS. The underlying
corporate universe is Baa investment-grade credit, and Moody's notes that
the underlying instruments have maturities of 20 years and above.
Differences in credit quality, maturity structure, and spread construction
prevent treatment of BAA10YM as a historical continuation of HY OAS.

The Moody's component is proprietary and subject to copyright and
redistribution restrictions. Therefore, long historical availability through
FRED does not imply unrestricted redistribution or future commercial use.

Potential V2 use:
- long-cycle corporate credit-spread reference
- robustness comparison with other long-history credit indicators
- validation against contemporary ICE HY OAS during the overlapping period

Disposition:
RETAIN AS VALIDATION CANDIDATE, not primary historical HY series.

Future Product Consideration:
Weak relative to government/public-domain inputs because the underlying
Moody's data introduce third-party intellectual-property and licensing
dependencies.

## Finding 06 — Practitioner and Research Response to Limited ICE HY OAS History

There is no clean public dataset that should be treated as an interchangeable
long-history replacement for the ICE BofA US High Yield Option-Adjusted Spread.

When exact historical ICE HY OAS observations are required, practitioners
without institutional data access may rely on previously downloaded or archived
copies of the ICE/FRED series. Such copies may be useful for private research
or validation, but their availability does not establish redistribution rights
and they should not form the provenance foundation of the public V2 repository.

For longer-horizon credit-cycle research, the Gilchrist–Zakrajšek framework
and Federal Reserve Excess Bond Premium (EBP) provide a more defensible
research alternative.

EBP is not a historical continuation of HY OAS. It measures a different
economic object: the component of corporate bond spreads not explained by
expected default losses, providing information about credit-market risk
appetite and the pricing of risk.

### V2 Research Architecture

- **ICE BofA HY OAS:** HY-specific contemporary benchmark.
- **Federal Reserve EBP:** long-history corporate credit risk-premium /
  risk-appetite indicator.
- **BAA10YM:** secondary long-history corporate-spread robustness candidate.
- **Archived ICE observations:** potentially useful for private validation,
  but not approved as a public-repository data source.

The project will not splice EBP, BAA10YM, or another credit indicator onto
ICE HY OAS to manufacture a synthetic long-history HY OAS series.

Instead, the relationship between EBP and ICE HY OAS will be evaluated
empirically over their available overlapping period.

### Disposition

**EBP: PASS — proceed to empirical overlap validation.**

The purpose of validation is not to establish that EBP is an equivalent proxy
for HY OAS. It is to determine whether EBP has a sufficiently stable and
economically interpretable relationship with HY credit conditions to support
long-horizon credit-cycle research in V2.

### HY OAS Missing-Value Audit

The downloaded ICE BofA HY OAS series contains eight missing observations
between July 2023 and July 2026.

All eight occur on U.S. market holidays:

- Christmas Day
- New Year's Day
- Good Friday

The missing observations therefore represent expected market-calendar
missingness rather than unexplained data loss.

Disposition: retain missing values in the raw data and do not interpolate
or impute them. Frequency alignment will use valid market observations only.

### Frequency Alignment Decision

The Federal Reserve EBP is a monthly constructed credit-market measure.
Dates in the published EBP file identify the corresponding month and should
not be interpreted as point-in-time observations on the first calendar day.

For overlap validation, daily ICE BofA HY OAS will therefore be aggregated
to monthly frequency.

Primary specification:
- monthly mean of valid daily HY OAS observations

Robustness specification:
- final valid HY OAS observation of each month (month-end market observation)

The primary specification is intended to compare average credit conditions
during each month. The month-end specification will test whether conclusions
depend materially on the aggregation convention.

Partial overlap months will be excluded from formal validation. July 2023 is
partial because the available ICE history begins July 28, 2023. July 2026 is
partial because the current ICE snapshot ends July 24, 2026.

The initial complete-month overlap window is therefore August 2023 through
June 2026.

The short overlap window is sufficient for diagnostic comparison but is not
sufficient to establish that EBP and ICE HY OAS are structurally equivalent
across credit cycles.

### EBP / ICE HY OAS Overlap Validation

EBP was compared with ICE BofA US High Yield OAS over the complete
monthly overlap period from August 2023 through June 2026.

The validation sample contains 35 monthly observations.

#### Levels

Using monthly mean HY OAS:

- Pearson correlation: 0.794
- Spearman correlation: 0.763

Using month-end HY OAS:

- Pearson correlation: 0.793
- Spearman correlation: 0.746

The similarity of the monthly-mean and month-end results indicates that
the observed relationship is not materially dependent on the selected
HY OAS monthly aggregation convention.

#### Month-to-Month Changes

Using monthly mean HY OAS changes:

- Pearson correlation: 0.414
- Spearman correlation: 0.418
- Observations: 34

The substantially lower correlation in monthly changes indicates that EBP
and HY OAS share meaningful information about broad credit conditions but
do not capture identical short-horizon dynamics.

This is consistent with their different constructions and economic meanings.

### Validation Conclusion

The overlap evidence supports use of EBP as a distinct long-history
corporate credit-condition and credit-risk-premium indicator in V2.

It does not support treating EBP as an equivalent proxy, historical
continuation, or reconstructed history of ICE BofA HY OAS.

The validation window is short and does not contain multiple complete
credit cycles. Therefore, the observed relationship should be interpreted
as diagnostic evidence rather than proof of structural equivalence.

**Disposition: PASS for long-history credit-cycle research as a distinct
indicator. Do not splice with ICE HY OAS.**

## Finding 07 — ICE BofA HY Series Share the Same Delivery Constraint

The three ICE BofA high-yield series used in V1 were audited together:

- HY OAS (`BAMLH0A0HYM2`)
- HY Effective Yield (`BAMLH0A0HYM2EY`)
- HY Total Return Index (`BAMLHYH0A0HYM2TRIV`)

All three current FRED snapshots:

- begin on 2023-07-28
- end on 2026-07-24
- contain 793 observations
- contain no duplicate dates
- contain eight missing observations

The eight missing observations occur on the same U.S. market holidays
(Christmas Day, New Year's Day, and Good Friday) and therefore represent
expected market-calendar missingness rather than unexplained data loss.

The identical history cutoff across all three ICE BofA series supports the
conclusion that the short history is a common upstream FRED/ICE delivery
constraint rather than a project-specific Python configuration problem.

### Disposition

Retain all three ICE BofA series for recent-period V2 analysis.

Do not treat their current FRED histories as sufficient for long-cycle,
historical-stress, or multi-regime inference.

Do not impute market-holiday missing observations.

Long-history research will use separately identified indicators rather than
splicing alternative series into the ICE BofA histories.

## Finding 08 — VIX Provides Long History but Remains a Proprietary Index

The V1 volatility series is the Cboe Volatility Index (`VIXCLS`) delivered
through FRED.

The current project snapshot:

- begins on 1990-01-02
- ends on 2026-07-24
- contains 9,539 observations
- contains no duplicate dates
- contains 302 missing observations

The missing observations are consistent with expected market closures and
non-trading days rather than unexplained data loss. No interpolation or
imputation will be applied to the raw VIX series.

Unlike the ICE BofA high-yield series, VIX retains a long historical record
through FRED and is therefore suitable for multi-cycle V2 research.

### Disposition

Retain VIX for V2 research and historical stress analysis.

VIX should be treated as a third-party proprietary index input rather than
as foundational public-domain data.

For any future commercial FirstMetric product that depends materially on
VIX, licensing and derived-use rights should be reviewed separately.

**Disposition: PASS for V2 research; long history available; proprietary
input for future-product purposes.**

## Finding 09 — Treasury and Effective Federal Funds Rate

### 10-Year Treasury Constant Maturity Rate

The V1 Treasury series is the 10-Year Treasury Constant Maturity Rate
(`DGS10`), sourced from the Board of Governors of the Federal Reserve System
and delivered through FRED.

The current project snapshot:

- begins on 1962-01-02
- ends on 2026-07-24
- contains 16,844 observations
- contains no duplicate dates
- contains 719 missing daily observations

The missing observations are consistent with calendar and market/non-release
days rather than unexplained data loss.

FRED identifies the series as public-domain data with citation requested.

**Disposition: PASS.**
Retain as a long-history Treasury-rate input for V2 and as a strong candidate
for durable future-product infrastructure.

### Effective Federal Funds Rate

The V1 policy-rate series is the Effective Federal Funds Rate (`EFFR`),
sourced from the Federal Reserve Bank of New York and delivered through FRED.

The current project snapshot:

- begins on 2000-07-03
- ends on 2026-07-24
- contains 6,800 observations
- contains no duplicate dates
- contains 257 missing daily observations

The 2000 start matches the published history of the modern EFFR series and is
not an artificial recent-history restriction.

Longer historical federal-funds-rate series exist, but they should not be
silently treated as identical continuations of the modern EFFR methodology.

**Disposition: PASS for modern-cycle policy-rate analysis.**
If pre-2000 policy-rate history becomes necessary, evaluate and document a
separate historical federal-funds series before use.

## Finding 10 — Unemployment and Recession Indicators Provide Long Public History

### U.S. Unemployment Rate

The V1 unemployment series is the civilian unemployment rate (`UNRATE`),
produced by the U.S. Bureau of Labor Statistics and delivered through FRED.

The current project snapshot:

- begins on 1948-01-01
- ends on 2026-06-01
- contains 942 monthly observations
- contains no duplicate dates
- contains one missing observation: October 2025

The October 2025 observation is genuinely unavailable in the underlying
official data. Current Population Survey data were not collected for that
month because of the 2025 federal government shutdown and were not
subsequently collected retroactively.

The missing observation will therefore remain missing. It will not be
interpolated or otherwise reconstructed in the raw series.

**Disposition: PASS.**
Retain as a long-history macroeconomic input for V2.

### U.S. Recession Indicator

The V1 recession series is the NBER-based U.S. recession indicator (`USREC`)
delivered through FRED.

The current project snapshot:

- begins on 1854-12-01
- ends on 2026-06-01
- contains 2,059 monthly observations
- contains no duplicate dates
- contains no missing observations

The series provides substantially more history than required for the
credit-cycle research contemplated in V2.

**Disposition: PASS.**
Retain as the historical recession indicator for V2.


## V2 Data Architecture Decision

The data-history audit supports a two-layer credit research architecture
rather than construction of a single artificially continuous high-yield
credit series.

### Layer 1 — Contemporary High-Yield Market Analytics

The ICE BofA high-yield series will remain the primary measures for
contemporary high-yield market analysis:

- ICE BofA US High Yield OAS
- ICE BofA US High Yield Effective Yield
- ICE BofA US High Yield Total Return Index

These series provide direct high-yield market measures but currently have
only approximately three years of history through the project's FRED
delivery pipeline.

They may support recent-period descriptive, relative-value, spread,
performance, drawdown, and market-condition analysis.

They will not independently support claims requiring multiple historical
credit cycles.

### Layer 2 — Long-History Credit-Cycle Research

The Federal Reserve Excess Bond Premium will provide the principal
long-history credit-market indicator for V2 research extending back to 1973.

EBP captures information related to corporate credit risk premia and exhibits
a strong positive relationship with ICE BofA HY OAS over their available
overlap period.

EBP will nevertheless remain analytically distinct from HY OAS.

It will not be renamed, rescaled, backfilled, or spliced into the ICE BofA
HY OAS series.

Long-history macro and market context may additionally use:

- 10-Year Treasury yield
- Effective Federal Funds Rate where historically appropriate
- unemployment
- recession indicators
- VIX from 1990 onward

### Governing Principle

V2 will prefer separate, economically interpretable series with transparent
methodological boundaries over construction of a superficially continuous
dataset from non-equivalent sources.

Any future model or research conclusion must respect the historical window
and economic meaning of the variables used.

## Licensing / Productization Disposition

The V2 data architecture distinguishes research usability from future
commercial redistribution and product use.

### Public / Government Data

Federal Reserve-produced data and other government statistical series provide
the strongest candidates for durable research and future-product
infrastructure where the underlying source identifies the information as
public domain or otherwise permits reuse with appropriate attribution.

These series should nevertheless retain explicit source and provenance
metadata.

### Proprietary Third-Party Indices

The ICE BofA high-yield indices and Cboe VIX are proprietary third-party
indices.

Their availability through FRED does not transfer commercial redistribution
rights to downstream users. FRED explicitly states that third-party
proprietary series remain subject to the rights and restrictions of the
underlying data owner.

Accordingly, use of these series in V2 research does not imply that their raw
observations may later be redistributed, embedded, or exposed in a commercial
FirstMetric product.

Any commercial implementation materially dependent on ICE BofA or Cboe data
will require a separate review of licensing and derived-data rights with the
underlying provider.

### FRED as Delivery Infrastructure

FRED is treated as a research delivery source rather than assumed to be a
future commercial production-data backend.

Future FirstMetric architecture should distinguish:

1. the underlying economic data provider,
2. the service through which the research project retrieved the data,
3. rights to store or redistribute the underlying observations, and
4. rights associated with any proprietary derived analytics.

Production data sourcing and licensing will therefore be reconsidered before
commercial deployment rather than inferred from research-stage FRED access.

### Derived Analytics

FirstMetric may eventually create proprietary scores, signals, classifications,
models, or indices from permitted inputs.

Ownership of a proprietary methodology does not automatically confer the
right to redistribute restricted source data or derivatives that effectively
reproduce proprietary third-party datasets.

Commercialization of derived analytics will therefore require review of both
the proprietary methodology and the rights associated with its underlying
inputs.

**Disposition:** V2 research may proceed using the audited series within their
documented research roles. Commercial product rights are not inferred from
research access.

### Research-to-Commercial Data Strategy

V2 does not attempt to acquire institutional data licenses before the
analytical and commercial value of the research has been established.

The project will initially use defensible research-accessible data to develop,
test, and validate analytical methods. If subsequent results demonstrate that
longer or higher-quality proprietary data would materially improve a
commercially viable FirstMetric product, institutional data access may then be
licensed directly from the relevant provider.

Accordingly, current data-access limitations are treated as research design
constraints rather than reasons to incur premature commercial data costs.

## Module 01 Conclusion

The audit establishes that the principal limitation of the V1 data
architecture is concentrated in the ICE BofA high-yield series currently
delivered through FRED, whose available project history begins in July 2023.

This limitation does not justify constructing an artificial long-history
high-yield series from non-equivalent data.

V2 will therefore use a two-layer research architecture:

1. **Contemporary HY layer:** ICE BofA HY OAS, effective yield, and total
   return index for direct recent-period high-yield market analysis.

2. **Long-history credit-cycle layer:** Federal Reserve EBP and associated
   long-history market and macroeconomic variables for multi-cycle research.

EBP and ICE BofA HY OAS remain distinct economic and statistical measures.
They will not be spliced or represented as a single continuous series.

The remaining long-history V1 inputs are sufficient for their currently
intended research roles, subject to the individual limitations documented
above.

Future statistical methods must respect the effective sample available for
the variables involved. In particular, the approximately three-year ICE BofA
history cannot independently support multi-cycle regime inference or complex
predictive modeling.

Research access to proprietary third-party data does not establish future
commercial redistribution rights. If V2 research demonstrates sufficient
analytical and commercial value, institutional data licensing may be evaluated
during a later productization stage.

**Module 01 disposition: COMPLETE.**

V2 may proceed to research design without altering the frozen V1 dashboard or
constructing synthetic historical ICE BofA series.