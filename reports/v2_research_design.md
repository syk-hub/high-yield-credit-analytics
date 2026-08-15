# High-Yield Credit Analytics V2
## Module 02 — Economic Construct & Research Design

### Candidate Economic Object

**Time-varying credit-market risk-bearing capacity**

Credit-market risk-bearing capacity refers to the willingness and ability of
investors and financial intermediaries to absorb corporate credit risk at a
given required level of compensation.

The construct is not directly observable.

Observable credit spreads may reflect multiple components, including expected
credit losses, compensation for bearing systematic credit risk, liquidity and
market frictions, and other pricing effects.

The research will investigate whether variation in risk-bearing capacity
constitutes an economically distinct state variable capable of explaining
variation in corporate credit risk premia and their behavior during periods
of market stress.

EBP, HY OAS, VIX, and other available variables are potential measurements,
outcomes, controls, or empirical implications of the underlying mechanism.
They are not assumed ex ante to constitute the latent economic object itself.

### Candidate Research Question

> Does variation in credit-market risk-bearing capacity constitute a distinct
> state variable that helps explain the time variation and stress behavior of
> corporate credit risk premia?

### Status

**Candidate construct — not yet adopted.**

The construct must survive theoretical scrutiny and comparison with competing
economic explanations before empirical modeling begins.

## Candidate Empirical Framework

### Economic Mechanism

Observed high-yield credit conditions reflect multiple interacting mechanisms:

- expected borrower default risk;
- macroeconomic conditions;
- market uncertainty;
- liquidity conditions; and
- intermediary risk-bearing capacity.

Intermediary risk-bearing capacity is not independent of macroeconomic and
market shocks. Adverse shocks may weaken intermediary balance sheets, tighten
funding constraints, or change which investors are willing and able to absorb
credit risk.

The empirical problem is therefore not to treat intermediary capacity and
macroeconomic conditions as mutually exclusive explanations, but to determine
whether observable market data contain information associated with changes in
risk-bearing capacity beyond conventional measures of borrower fundamentals
and macroeconomic conditions.

### Empirical Target

The primary empirical target is the condition and evolution of the U.S.
high-yield credit market, measured principally through ICE BofA High Yield
Option-Adjusted Spread (HY OAS).

V2 will investigate whether observable market and macroeconomic variables
contain incremental information for explaining or forecasting changes in
high-yield credit conditions.

The initial empirical design will distinguish among three broad information
sets:

1. **Credit and financial-sector conditions**
   - Excess Bond Premium (EBP)
   - other validated credit-market measures where available

2. **Market and funding conditions**
   - VIX
   - interest-rate and monetary-policy variables
   - additional liquidity or funding measures if justified by subsequent
     research

3. **Macroeconomic conditions**
   - unemployment
   - recession state
   - additional macroeconomic controls only where theoretically justified

The purpose is not initially to construct an "intermediary capacity index."
Instead, the analysis will determine what incremental information these
different information sets provide about high-yield credit conditions and
whether the resulting empirical patterns are consistent with established
intermediary risk-bearing-capacity mechanisms.

### Candidate Empirical Hypotheses

The following hypotheses are preliminary and are intended to translate the
existing theoretical literature into testable implications for V2.

#### H1 — Credit-Risk-Premium Information

EBP should contain information about high-yield credit conditions beyond
macroeconomic variables that primarily capture borrower fundamentals or the
business cycle.

If EBP retains explanatory or forecasting power after controlling for
unemployment, recession state, and interest-rate conditions, this would be
consistent with the interpretation that credit-market risk compensation
contains information beyond expected default deterioration alone.

#### H2 — Market-Stress Interaction

The relationship between credit-risk-premium measures and HY OAS may be
state-dependent.

Changes in EBP or other credit-market indicators may have larger effects on
HY OAS during periods of elevated market stress, tighter funding conditions,
or reduced intermediary risk-bearing capacity.

This would be consistent with intermediary models in which constraints become
more important during adverse states.

#### H3 — Incremental Information Beyond General Market Uncertainty

Credit-market variables should contain information about HY OAS beyond broad
market uncertainty measures such as VIX.

If EBP or related credit indicators add explanatory or forecasting power after
conditioning on VIX, this would suggest that they capture information more
specific to credit-market conditions than generic risk sentiment alone.

#### H4 — Contemporary Validation Rather Than Historical Substitution

Long-history variables such as EBP may help characterize credit-cycle
conditions, but they should not be assumed to reconstruct historical HY OAS.

Any predictive or explanatory relationship between EBP and HY OAS must be
evaluated over their actual overlap period and interpreted as evidence of
related economic information rather than structural equivalence.

### Candidate Variable Map

| Variable | Role in V2 | Economic Interpretation | Initial Expected Relationship with HY OAS | Frequency / Sample Constraint |
|---|---|---|---|---|
| HY OAS | Primary outcome | Market compensation for high-yield credit risk | — | Daily; current local history begins 2023-07 |
| EBP | Credit risk-premium measure | Compensation beyond estimated expected-default component | Positive | Monthly; overlap with current HY OAS history begins 2023-08 |
| VIX | Market uncertainty / stress | Broad market-implied uncertainty and risk sentiment | Positive | Daily |
| 10Y Treasury Yield | Rates / macro-financial control | Risk-free rate and broader monetary/financial conditions | Ambiguous; regime-dependent | Daily |
| EFFR | Monetary-policy control | Short-term policy/funding-rate environment | Ambiguous; potentially lagged | Daily |
| Unemployment Rate | Macro / borrower-fundamentals control | Labor-market deterioration and business-cycle conditions | Positive | Monthly |
| Recession Flag | Macro regime control | NBER recession state | Positive | Monthly |

### Initial Modeling Principle

Variables will not be included merely because they are available. Each variable
must have a defensible economic role in the empirical design.

The initial analysis should favor parsimonious specifications that allow the
incremental contribution of each information set to be evaluated before more
complex models are introduced.

Mixed-frequency series will require an explicit alignment rule before modeling.
No interpolation or transformation should be performed solely to increase the
number of observations.

### Sample-History Constraint

The current local ICE BofA HY OAS history provides only 35 complete monthly
observations overlapping with EBP (August 2023 through June 2026).

This sample is sufficient for preliminary diagnostics but is too short for a
multivariable empirical specification with credible statistical inference.

Before formal modeling, V2 must determine whether to:

1. obtain a longer legally and methodologically defensible HY OAS history;
2. use a longer-history credit-spread measure for research development while
   preserving HY OAS as a separate contemporary validation target; or
3. restrict the analysis to the contemporary period and materially narrow the
   claims and model complexity.

   ### Long-History Research Target Decision

The Federal Reserve EBP dataset also contains the Gilchrist-Zakrajšek
corporate credit spread (`gz_spread`) from 1973 onward.

For initial long-history empirical research, V2 will evaluate the GZ spread
as the primary corporate-credit pricing outcome rather than attempting to
extend ICE BofA HY OAS with a non-equivalent proxy.

This creates a three-part architecture:

1. **GZ spread** — long-history corporate credit-spread outcome;
2. **EBP** — long-history excess credit-risk-premium component within the
   Gilchrist-Zakrajšek framework;
3. **ICE BofA HY OAS** — contemporary high-yield benchmark used for
   recent-period validation and HY-specific interpretation.

The GZ spread will not be labeled as high-yield OAS. Results obtained using
the GZ spread concern broad corporate credit pricing unless separately
validated for the high-yield market.

Other long-history series such as Moody's Baa corporate yields may be
evaluated later as robustness measures but will not be introduced merely to
increase sample length.

### Nested Empirical Samples

To preserve historical information, V2 will use nested empirical samples
rather than forcing all variables into a single common window.

#### Sample A — Core Credit Sample

Period: approximately 1973–2026

Variables:

- GZ corporate credit spread
- Excess Bond Premium
- model-implied recession probability

Purpose:

Establish the long-history relationship among observed corporate credit
spreads, expected-default conditions, and the excess credit-risk premium.

#### Sample B — Macro-Control Sample

Period: approximately 1973–2026, subject to aligned availability

Adds:

- unemployment
- recession indicator
- 10-Year Treasury yield

Purpose:

Evaluate whether EBP contains information beyond conventional macroeconomic
and rates conditions.

#### Sample C — Market-Stress Sample

Period: approximately 1990–2026

Adds:

- VIX

Purpose:

Test whether credit-risk-premium information remains distinct from broad
market uncertainty and stress.

#### Sample D — Modern Policy Sample

Period: approximately 2000–2026

Adds:

- Effective Federal Funds Rate

Purpose:

Evaluate the incremental role of modern monetary-policy conditions without
discarding earlier history from the core specifications.

### Sample Construction Principle

Later-starting controls will not determine the historical window for all V2
analysis. Each specification must use the longest defensible sample consistent
with the variables required for that specific test.