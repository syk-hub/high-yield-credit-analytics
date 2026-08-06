# High-Yield Credit Analytics

A credit-market analytics project for monitoring U.S. high-yield credit conditions, spread behavior, market stress, and macroeconomic context.

The project combines a reproducible Python/FRED data pipeline with derived credit-risk metrics and a three-page Power BI monitoring dashboard.

## Dashboard

### Credit Market Overview

![Credit Market Overview](images/01_credit_market_overview.png)

Tracks current high-yield credit conditions through option-adjusted spreads (OAS), yield, volatility, spread momentum, total-return drawdown, and a rules-based credit regime indicator.

### Market Stress & Performance

![Market Stress & Performance](images/02_market_stress_performance.png)

Examines high-yield total-return performance, drawdowns, and the relationship between market volatility and HY credit spreads.

### Macro & Credit Context

![Macro & Credit Context](images/03_macro_credit_context.png)

Places recent credit conditions within a broader macroeconomic context using monthly HY spreads, the effective federal funds rate, and U.S. unemployment.

## Analytical Framework

The project focuses on several dimensions of high-yield credit risk:

- **Spread level:** current HY option-adjusted spread and its position within the available sample distribution
- **Spread momentum:** 1-month and 3-month changes in OAS
- **Credit regime:** rules-based classification of spread conditions
- **Market stress:** VIX and the relationship between volatility and HY spreads
- **Performance risk:** high-yield total-return index behavior and drawdown
- **Macro context:** monetary-policy and labor-market conditions

Percentile statistics and regime classifications are interpreted relative to the available project sample rather than as full-cycle historical estimates.

## Data

Primary market and macroeconomic series are sourced from the Federal Reserve Economic Data (FRED) database.

The pipeline integrates daily and monthly series covering:

- U.S. high-yield option-adjusted spreads
- U.S. high-yield effective yield
- high-yield total-return performance
- CBOE VIX
- Effective Federal Funds Rate
- U.S. unemployment rate

Raw source data can be regenerated using the download scripts and is therefore excluded from version control.

## Methodology

Python scripts handle data retrieval, cleaning, alignment, and construction of derived analytical fields used by the dashboard.

Derived measures include:

- OAS expressed in basis points
- 1-month and 3-month spread changes
- sample OAS percentile
- rules-based credit regime
- high-yield total-return drawdown
- spread widening and tightening diagnostics

Power BI is used for the presentation layer, including DAX measures, current-condition KPIs, historical visualizations, and cross-filtering between market observations and dashboard metrics.

## Repository Structure

```text
high-yield-credit-analytics/
├── data/
│   └── processed/        # Clean analytical datasets
├── images/               # Dashboard screenshots
├── powerbi/              # Power BI report
├── reports/              # Research/report outputs
├── src/                  # Data pipeline and analytical scripts
├── .gitignore
├── README.md
└── requirements.txt
```

## Technology

**Python** · **pandas** · **FRED API** · **Power BI** · **DAX** · **Git/GitHub**

## Project Status

**Version 1 complete:** reproducible market-data pipeline, derived high-yield credit diagnostics, and three-page Power BI dashboard.

Potential future development includes deeper credit-risk modeling, additional stress indicators, and expanded historical analysis.
