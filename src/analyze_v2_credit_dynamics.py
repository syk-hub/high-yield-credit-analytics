from pathlib import Path
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

SAMPLE_B_FILE = (
    PROCESSED_DIR
    / "v2_macro_credit_monthly.csv"
)

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"

FAILS_MONTHLY_PATH = (
    RAW_DIR / "nyfed_corporate_fails_monthly.csv"
)

fails_monthly = pd.read_csv(
    FAILS_MONTHLY_PATH,
    parse_dates=["As Of Date"],
)

HY_DEALER_MONTHLY_PATH = (
    RAW_DIR / "nyfed_hy_dealer_positions_monthly.csv"
)

hy_dealer_monthly = pd.read_csv(
    HY_DEALER_MONTHLY_PATH,
    parse_dates=["As Of Date"],
)

KARGAR_INTERMEDIARY_PATH = (
    RAW_DIR
    / "fred_kargar_intermediary_wealth_share_quarterly.csv"
)

# ------------------------------------------------------------
# Load research dataset
# ------------------------------------------------------------

data = pd.read_csv(SAMPLE_B_FILE)

data["date"] = pd.to_datetime(
    data["date"]
)

data["default_related_component"] = (
    data["gz_spread"] - data["ebp"]
)

data = data.rename(
    columns={
        "est_prob": "recession_probability"
    }
)


# ------------------------------------------------------------
# Initial GZ spread decomposition diagnostics
# ------------------------------------------------------------

print()
print("=" * 60)
print("GZ SPREAD DECOMPOSITION")
print("=" * 60)

print(
    data[
        [
        "gz_spread",
        "default_related_component",
        "ebp",
        "recession_probability",
        ]
    ].describe()
)

print()
print("Component correlations:")
print(
    data[
        [
        "gz_spread",
        "default_related_component",
        "ebp",
        "recession_probability",
        ]
    ].corr()
)

# ------------------------------------------------------------
# Recession-state comparison
# ------------------------------------------------------------

state_summary = (
    data
    .groupby("RECESSION_FLAG")
    [
        [
            "gz_spread",
            "default_related_component",
            "ebp",
        ]
    ]
    .agg(["mean", "median", "std", "count"])
)

print()
print("=" * 60)
print("CREDIT SPREAD COMPONENTS BY RECESSION STATE")
print("=" * 60)

print(state_summary)

# ------------------------------------------------------------
# Recession episodes
# ------------------------------------------------------------

recession_data = data.loc[
    data["RECESSION_FLAG"] == 1
].copy()

recession_data["recession_start"] = (
    recession_data["date"]
    .diff()
    .dt.days
    .gt(40)
    .cumsum()
)

episode_summary = (
    recession_data
    .groupby("recession_start")
    .agg(
        start_date=("date", "min"),
        end_date=("date", "max"),
        months=("date", "count"),
        mean_gz_spread=("gz_spread", "mean"),
        mean_default_related=(
            "default_related_component",
            "mean",
        ),
        mean_ebp=("ebp", "mean"),
        max_ebp=("ebp", "max"),
    )
)

episode_summary["ebp_fraction_of_spread"] = (
    episode_summary["mean_ebp"]
    / episode_summary["mean_gz_spread"]
)

episode_summary["default_fraction_of_spread"] = (
    episode_summary["mean_default_related"]
    / episode_summary["mean_gz_spread"]
)

print()
print("=" * 60)
print("CREDIT COMPONENTS BY RECESSION EPISODE")
print("=" * 60)

print(episode_summary.to_string(index=False))

SAMPLE_C_FILE = (
    PROCESSED_DIR
    / "v2_market_stress_monthly.csv"
)

market_data = pd.read_csv(SAMPLE_C_FILE)

market_data["date"] = pd.to_datetime(
    market_data["date"]
)

print()
print("=" * 60)
print("EBP / VIX MARKET-STRESS DIAGNOSTICS")
print("=" * 60)

print(
    market_data[
        [
            "ebp",
            "VIX",
            "gz_spread",
        ]
    ].corr()
)

# ------------------------------------------------------------
# Incremental information test: EBP versus VIX
# ------------------------------------------------------------

reg_data = market_data[
    ["gz_spread", "ebp", "VIX"]
].dropna()

X = reg_data[
    ["ebp", "VIX"]
]

X = sm.add_constant(X)

model = sm.OLS(
    reg_data["gz_spread"],
    X,
).fit(
    cov_type="HAC",
    cov_kwds={"maxlags": 3},
)

print()
print("=" * 60)
print("GZ SPREAD ~ EBP + VIX")
print("=" * 60)

print(model.summary())

# ------------------------------------------------------------
# EBP time-series diagnostics
# ------------------------------------------------------------

ebp_series = market_data["ebp"].dropna()

print()
print("=" * 60)
print("EBP TIME-SERIES DIAGNOSTICS")
print("=" * 60)

print(f"Observations: {len(ebp_series):,}")
print(f"Mean: {ebp_series.mean():.4f}")
print(f"Std. dev.: {ebp_series.std():.4f}")

print()
print("Autocorrelation:")
for lag in [1, 3, 6, 12]:
    print(
        f"Lag {lag:>2}: "
        f"{ebp_series.autocorr(lag=lag):.4f}"
    )

adf_result = adfuller(
    ebp_series,
    autolag="AIC",
)

print()
print("Augmented Dickey-Fuller test:")
print(f"ADF statistic: {adf_result[0]:.4f}")
print(f"p-value: {adf_result[1]:.4f}")
print(f"Lags used: {adf_result[2]}")
print(f"Observations used: {adf_result[3]}")

# ------------------------------------------------------------
# One-month-ahead EBP forecasting diagnostics
# ------------------------------------------------------------

forecast_data = market_data[
    ["date", "ebp", "VIX"]
].copy()

# Target: next month's EBP
forecast_data["ebp_next"] = (
    forecast_data["ebp"].shift(-1)
)

forecast_data = forecast_data.dropna()


def fit_hac_model(y, X):
    X = sm.add_constant(X)

    return sm.OLS(
        y,
        X,
    ).fit(
        cov_type="HAC",
        cov_kwds={"maxlags": 3},
    )


# Model 1: persistence only
model_1 = fit_hac_model(
    forecast_data["ebp_next"],
    forecast_data[["ebp"]],
)

# Model 2: VIX only
model_2 = fit_hac_model(
    forecast_data["ebp_next"],
    forecast_data[["VIX"]],
)

# Model 3: persistence + VIX
model_3 = fit_hac_model(
    forecast_data["ebp_next"],
    forecast_data[["ebp", "VIX"]],
)


print()
print("=" * 60)
print("ONE-MONTH-AHEAD EBP MODELS")
print("=" * 60)

print()
print("MODEL 1 — EBP(t+1) ~ EBP(t)")
print(model_1.summary())

print()
print("MODEL 2 — EBP(t+1) ~ VIX(t)")
print(model_2.summary())

print()
print("MODEL 3 — EBP(t+1) ~ EBP(t) + VIX(t)")
print(model_3.summary())

# ------------------------------------------------------------
# EBP change diagnostics
# ------------------------------------------------------------

change_data = market_data[
    ["date", "ebp", "VIX"]
].copy()

change_data["delta_ebp"] = (
    change_data["ebp"].diff()
)

change_data["delta_vix"] = (
    change_data["VIX"].diff()
)

change_data = change_data.dropna()

delta_ebp = change_data["delta_ebp"]

print()
print("=" * 60)
print("DELTA EBP TIME-SERIES DIAGNOSTICS")
print("=" * 60)

print(f"Observations: {len(delta_ebp):,}")
print(f"Mean: {delta_ebp.mean():.4f}")
print(f"Std. dev.: {delta_ebp.std():.4f}")

print()
print("Autocorrelation:")
for lag in [1, 3, 6, 12]:
    print(
        f"Lag {lag:>2}: "
        f"{delta_ebp.autocorr(lag=lag):.4f}"
    )

print()
print("Correlation of monthly changes:")
print(
    change_data[
        ["delta_ebp", "delta_vix"]
    ].corr()
)

adf_delta = adfuller(
    delta_ebp,
    autolag="AIC",
)

print()
print("ADF test — Delta EBP:")
print(f"ADF statistic: {adf_delta[0]:.4f}")
print(f"p-value: {adf_delta[1]:.4f}")
print(f"Lags used: {adf_delta[2]}")

# ------------------------------------------------------------
# Contemporaneous EBP-change model
# ------------------------------------------------------------

X_change = sm.add_constant(
    change_data[["delta_vix"]]
)

change_model = sm.OLS(
    change_data["delta_ebp"],
    X_change,
).fit(
    cov_type="HAC",
    cov_kwds={"maxlags": 3},
)

print()
print("=" * 60)
print("DELTA EBP ~ DELTA VIX")
print("=" * 60)

print(change_model.summary())

# ------------------------------------------------------------
# One-month-ahead EBP-change test
# ------------------------------------------------------------

lead_change_data = change_data[
    ["delta_ebp", "delta_vix"]
].copy()

# Target: next month's change in EBP
lead_change_data["delta_ebp_next"] = (
    lead_change_data["delta_ebp"].shift(-1)
)

lead_change_data = lead_change_data.dropna()

X_lead = sm.add_constant(
    lead_change_data[["delta_vix"]]
)

lead_change_model = sm.OLS(
    lead_change_data["delta_ebp_next"],
    X_lead,
).fit(
    cov_type="HAC",
    cov_kwds={"maxlags": 3},
)

print()
print("=" * 60)
print("DELTA EBP(t+1) ~ DELTA VIX(t)")
print("=" * 60)

print(lead_change_model.summary())


# ------------------------------------------------------------
# 10Y TREASURY / EBP CHANGE DIAGNOSTICS
# ------------------------------------------------------------

change_data = market_data[
    [
        "date",
        "ebp",
        "VIX",
        "TREASURY_10Y",
    ]
].copy()

change_data["delta_ebp"] = (
    change_data["ebp"].diff()
)

change_data["delta_vix"] = (
    change_data["VIX"].diff()
)

change_data["delta_treasury_10y"] = (
    change_data["TREASURY_10Y"].diff()
)

change_data = change_data.dropna()

print()
print("=" * 60)
print("10Y TREASURY / EBP CHANGE DIAGNOSTICS")
print("=" * 60)

print("Correlation matrix:")
print(
    change_data[
        [
            "delta_ebp",
            "delta_vix",
            "delta_treasury_10y",
        ]
    ].corr()
)

print()
print("10Y Treasury monthly-change autocorrelation:")
for lag in [1, 3, 6, 12]:
    print(
        f"Lag {lag:>2}: "
        f"{change_data['delta_treasury_10y'].autocorr(lag=lag):.4f}"
    )

    # ------------------------------------------------------------
# EBP changes: VIX + 10Y Treasury
# ------------------------------------------------------------

X_vix_treasury = sm.add_constant(
    change_data[
        [
            "delta_vix",
            "delta_treasury_10y",
        ]
    ]
)

vix_treasury_model = sm.OLS(
    change_data["delta_ebp"],
    X_vix_treasury,
).fit(
    cov_type="HAC",
    cov_kwds={"maxlags": 3},
)

print()
print("=" * 60)
print("DELTA EBP ~ DELTA VIX + DELTA 10Y")
print("=" * 60)

print(vix_treasury_model.summary())

# ------------------------------------------------------------
# Corporate fails — monthly level diagnostics
# ------------------------------------------------------------

fails_series = (
    fails_monthly[
        "MONTHLY_MEAN_FAILS_TO_DELIVER_MILLIONS"
    ]
    .dropna()
)

print()
print("=" * 60)
print("CORPORATE FAILS - MONTHLY LEVEL DIAGNOSTICS")
print("=" * 60)

print()
print(f"Observations: {len(fails_series):,}")

print()
print("Summary:")
print(fails_series.describe())

print()
print("Autocorrelation:")
for lag in [1, 3, 6, 12]:
    print(
        f"lag {lag}: "
        f"{fails_series.autocorr(lag=lag):.4f}"
    )

from statsmodels.tsa.stattools import adfuller

adf_result = adfuller(
    fails_series,
    autolag="AIC",
)

print()
print(f"ADF statistic: {adf_result[0]:.4f}")
print(f"ADF p-value: {adf_result[1]:.6f}")

# ------------------------------------------------------------
# Corporate fails - monthly change diagnostics
# ------------------------------------------------------------

fails_monthly["D_FAILS_DELIVER"] = (
    fails_monthly[
        "MONTHLY_MEAN_FAILS_TO_DELIVER_MILLIONS"
    ]
    .diff()
)

d_fails = (
    fails_monthly["D_FAILS_DELIVER"]
    .dropna()
)

print()
print("=" * 60)
print("CORPORATE FAILS - MONTHLY CHANGE DIAGNOSTICS")
print("=" * 60)

print()
print(f"Observations: {len(d_fails):,}")

print()
print("Summary:")
print(d_fails.describe())

print()
print("Autocorrelation:")
for lag in [1, 3, 6, 12]:
    print(
        f"lag {lag}: "
        f"{d_fails.autocorr(lag=lag):.4f}"
    )

adf_d_fails = adfuller(
    d_fails,
    autolag="AIC",
)

print()
print(f"ADF statistic: {adf_d_fails[0]:.4f}")
print(f"ADF p-value: {adf_d_fails[1]:.6f}")

# ------------------------------------------------------------
# Merge monthly corporate fails with EBP / VIX data
# ------------------------------------------------------------

fails_for_merge = fails_monthly[
    [
        "As Of Date",
        "D_FAILS_DELIVER",
    ]
].copy()

fails_for_merge = fails_for_merge.rename(
    columns={
        "As Of Date": "date",
    }
)

# Normalize both to month-end timestamps
change_data["date"] = (
    pd.to_datetime(change_data["date"])
    .dt.to_period("M")
    .dt.to_timestamp("M")
)

fails_for_merge["date"] = (
    pd.to_datetime(fails_for_merge["date"])
    .dt.to_period("M")
    .dt.to_timestamp("M")
)

intermediary_data = change_data.merge(
    fails_for_merge,
    on="date",
    how="inner",
    validate="one_to_one",
)

intermediary_data = intermediary_data.dropna(
    subset=[
        "delta_ebp",
        "delta_vix",
        "D_FAILS_DELIVER",
    ]
)

print()
print("=" * 60)
print("EBP / VIX / CORPORATE FAILS - MERGE CHECK")
print("=" * 60)

print()
print(f"Observations: {len(intermediary_data):,}")

print(
    f"Date range: "
    f"{intermediary_data['date'].min().date()} "
    f"to {intermediary_data['date'].max().date()}"
)

print()
print("Missing values:")
print(
    intermediary_data[
        [
            "delta_ebp",
            "delta_vix",
            "D_FAILS_DELIVER",
        ]
    ].isna().sum()
)

print()
print("Correlation matrix:")
print(
    intermediary_data[
        [
            "delta_ebp",
            "delta_vix",
            "D_FAILS_DELIVER",
        ]
    ].corr()
)

# ------------------------------------------------------------
# EBP ~ VIX + corporate fails
# HAC regression on common sample
# ------------------------------------------------------------

X_intermediary = intermediary_data[
    [
        "delta_vix",
        "D_FAILS_DELIVER",
    ]
]

X_intermediary = sm.add_constant(
    X_intermediary
)

y_intermediary = intermediary_data[
    "delta_ebp"
]

model_intermediary = sm.OLS(
    y_intermediary,
    X_intermediary,
).fit(
    cov_type="HAC",
    cov_kwds={"maxlags": 3},
)

print()
print("=" * 60)
print("HAC REGRESSION: DELTA EBP ~ DELTA VIX + DELTA FAILS")
print("=" * 60)

print()
print(model_intermediary.summary())

# ------------------------------------------------------------
# Common-sample benchmark: EBP ~ VIX only
# ------------------------------------------------------------

X_vix_common = sm.add_constant(
    intermediary_data[["delta_vix"]]
)

y_vix_common = intermediary_data["delta_ebp"]

model_vix_common = sm.OLS(
    y_vix_common,
    X_vix_common,
).fit(
    cov_type="HAC",
    cov_kwds={"maxlags": 3},
)

print()
print("=" * 60)
print("COMMON-SAMPLE HAC BENCHMARK: DELTA EBP ~ DELTA VIX")
print("=" * 60)

print()
print(f"Observations: {int(model_vix_common.nobs)}")
print(f"Delta VIX coefficient: {model_vix_common.params['delta_vix']:.6f}")
print(f"Delta VIX p-value: {model_vix_common.pvalues['delta_vix']:.6f}")
print(f"R-squared: {model_vix_common.rsquared:.6f}")

print()
print("Incremental R-squared from adding Delta Fails:")
print(
    f"{model_intermediary.rsquared - model_vix_common.rsquared:.6f}"
)

# ------------------------------------------------------------
# HY dealer net positions - monthly level diagnostics
# ------------------------------------------------------------

hy_position_series = (
    hy_dealer_monthly[
        "HY_DEALER_NET_POSITION_MILLIONS"
    ]
    .dropna()
)

print()
print("=" * 60)
print("HY DEALER NET POSITIONS - MONTHLY LEVEL DIAGNOSTICS")
print("=" * 60)

print()
print(f"Observations: {len(hy_position_series):,}")

print()
print("Summary:")
print(hy_position_series.describe())

print()
print("Autocorrelation:")
for lag in [1, 3, 6, 12]:
    print(
        f"lag {lag}: "
        f"{hy_position_series.autocorr(lag=lag):.4f}"
    )

adf_hy = adfuller(
    hy_position_series,
    autolag="AIC",
)

print()
print(f"ADF statistic: {adf_hy[0]:.4f}")
print(f"ADF p-value: {adf_hy[1]:.6f}")

# ------------------------------------------------------------
# HY dealer net positions - monthly change diagnostics
# ------------------------------------------------------------

hy_dealer_monthly["D_HY_DEALER_POSITION"] = (
    hy_dealer_monthly[
        "HY_DEALER_NET_POSITION_MILLIONS"
    ]
    .diff()
)

d_hy_position = (
    hy_dealer_monthly["D_HY_DEALER_POSITION"]
    .dropna()
)

print()
print("=" * 60)
print("HY DEALER NET POSITIONS - MONTHLY CHANGE DIAGNOSTICS")
print("=" * 60)

print()
print(f"Observations: {len(d_hy_position):,}")

print()
print("Summary:")
print(d_hy_position.describe())

print()
print("Autocorrelation:")
for lag in [1, 3, 6, 12]:
    print(
        f"lag {lag}: "
        f"{d_hy_position.autocorr(lag=lag):.4f}"
    )

adf_d_hy = adfuller(
    d_hy_position,
    autolag="AIC",
)

print()
print(f"ADF statistic: {adf_d_hy[0]:.4f}")
print(f"ADF p-value: {adf_d_hy[1]:.6f}")

# ------------------------------------------------------------
# Merge HY dealer positions with EBP / VIX data
# ------------------------------------------------------------

hy_for_merge = hy_dealer_monthly[
    [
        "As Of Date",
        "D_HY_DEALER_POSITION",
    ]
].copy()

hy_for_merge = hy_for_merge.rename(
    columns={"As Of Date": "date"}
)

hy_for_merge["date"] = (
    pd.to_datetime(hy_for_merge["date"])
    .dt.to_period("M")
    .dt.to_timestamp("M")
)

hy_intermediary_data = change_data.merge(
    hy_for_merge,
    on="date",
    how="inner",
    validate="one_to_one",
)

hy_intermediary_data = hy_intermediary_data.dropna(
    subset=[
        "delta_ebp",
        "delta_vix",
        "D_HY_DEALER_POSITION",
    ]
)

print()
print("=" * 60)
print("EBP / VIX / HY DEALER POSITIONS - MERGE CHECK")
print("=" * 60)

print()
print(f"Observations: {len(hy_intermediary_data):,}")

print(
    f"Date range: "
    f"{hy_intermediary_data['date'].min().date()} "
    f"to {hy_intermediary_data['date'].max().date()}"
)

print()
print("Correlation matrix:")
print(
    hy_intermediary_data[
        [
            "delta_ebp",
            "delta_vix",
            "D_HY_DEALER_POSITION",
        ]
    ].corr()
)

# ------------------------------------------------------------
# HY dealer positions - common-sample HAC comparison
# ------------------------------------------------------------

y_hy = hy_intermediary_data["delta_ebp"]

# VIX-only benchmark
X_hy_vix = sm.add_constant(
    hy_intermediary_data[["delta_vix"]]
)

model_hy_vix = sm.OLS(
    y_hy,
    X_hy_vix,
).fit(
    cov_type="HAC",
    cov_kwds={"maxlags": 3},
)

# VIX + HY dealer position
X_hy_full = sm.add_constant(
    hy_intermediary_data[
        [
            "delta_vix",
            "D_HY_DEALER_POSITION",
        ]
    ]
)

model_hy_full = sm.OLS(
    y_hy,
    X_hy_full,
).fit(
    cov_type="HAC",
    cov_kwds={"maxlags": 3},
)

print()
print("=" * 60)
print("HY DEALER POSITIONS - COMMON-SAMPLE HAC COMPARISON")
print("=" * 60)

print()
print("VIX ONLY")
print(f"N: {int(model_hy_vix.nobs)}")
print(
    f"Delta VIX coefficient: "
    f"{model_hy_vix.params['delta_vix']:.6f}"
)
print(
    f"Delta VIX p-value: "
    f"{model_hy_vix.pvalues['delta_vix']:.6f}"
)
print(f"R-squared: {model_hy_vix.rsquared:.6f}")

print()
print("VIX + HY DEALER POSITION")
print(
    f"Delta VIX coefficient: "
    f"{model_hy_full.params['delta_vix']:.6f}"
)
print(
    f"Delta VIX p-value: "
    f"{model_hy_full.pvalues['delta_vix']:.6f}"
)
print(
    f"Delta HY position coefficient: "
    f"{model_hy_full.params['D_HY_DEALER_POSITION']:.8f}"
)
print(
    f"Delta HY position p-value: "
    f"{model_hy_full.pvalues['D_HY_DEALER_POSITION']:.6f}"
)
print(f"R-squared: {model_hy_full.rsquared:.6f}")

print()
print(
    "Incremental R-squared from HY dealer position: "
    f"{model_hy_full.rsquared - model_hy_vix.rsquared:.6f}"
)

# ------------------------------------------------------------
# Kargar-style intermediary wealth share - load
# ------------------------------------------------------------

kargar_data = pd.read_csv(
    KARGAR_INTERMEDIARY_PATH,
    parse_dates=["date"],
)

print()
print("=" * 60)
print("KARGAR INTERMEDIARY WEALTH SHARE - ANALYSIS LOAD CHECK")
print("=" * 60)

print()
print(f"Observations: {len(kargar_data):,}")

print(
    f"Date range: "
    f"{kargar_data['date'].min().date()} "
    f"to {kargar_data['date'].max().date()}"
)

print()
print("Missing values:")
print(
    kargar_data[
        [
            "BD_EQUITY",
            "BANK_EQUITY",
            "BD_WEALTH_SHARE",
        ]
    ].isna().sum()
)

print()
print("Last five:")
print(
    kargar_data[
        [
            "date",
            "BD_EQUITY",
            "BANK_EQUITY",
            "BD_WEALTH_SHARE",
        ]
    ]
    .tail()
    .to_string(index=False)
)

# ------------------------------------------------------------
# Quarterly EBP / VIX construction for Kargar-style test
# ------------------------------------------------------------

quarterly_market = (
    market_data[
        [
            "date",
            "ebp",
            "VIX",
        ]
    ]
    .copy()
)

quarterly_market["quarter"] = (
    quarterly_market["date"]
    .dt.to_period("Q")
)

quarterly_market = (
    quarterly_market
    .groupby(
        "quarter",
        as_index=False,
    )
    .agg(
        EBP_QUARTER_END=("ebp", "last"),
        VIX_QUARTER_MEAN=("VIX", "mean"),
        MONTHS_IN_QUARTER=("date", "count"),
    )
)

quarterly_market["date"] = (
    quarterly_market["quarter"]
    .dt.to_timestamp(how="end")
    .dt.normalize()
)

quarterly_market["D_EBP_QUARTERLY"] = (
    quarterly_market["EBP_QUARTER_END"]
    .diff()
)

quarterly_market["D_VIX_QUARTERLY"] = (
    quarterly_market["VIX_QUARTER_MEAN"]
    .diff()
)

print()
print("=" * 60)
print("QUARTERLY EBP / VIX - CONSTRUCTION CHECK")
print("=" * 60)

print()
print(f"Quarters: {len(quarterly_market):,}")

print(
    f"Date range: "
    f"{quarterly_market['date'].min().date()} "
    f"to {quarterly_market['date'].max().date()}"
)

print()
print("Months per quarter:")
print(
    quarterly_market["MONTHS_IN_QUARTER"]
    .value_counts()
    .sort_index()
)

print()
print("Last five:")
print(
    quarterly_market[
        [
            "date",
            "EBP_QUARTER_END",
            "VIX_QUARTER_MEAN",
            "D_EBP_QUARTERLY",
            "D_VIX_QUARTERLY",
            "MONTHS_IN_QUARTER",
        ]
    ]
    .tail()
    .to_string(index=False)
)

quarterly_market_complete = (
    quarterly_market[
        quarterly_market["MONTHS_IN_QUARTER"] == 3
    ]
    .copy()
)

print()
print("=" * 60)
print("QUARTERLY MARKET DATA - COMPLETE QUARTERS")
print("=" * 60)

print()
print(f"Complete quarters: {len(quarterly_market_complete):,}")

print(
    f"Date range: "
    f"{quarterly_market_complete['date'].min().date()} "
    f"to {quarterly_market_complete['date'].max().date()}"
)

print()
print("Last five:")
print(
    quarterly_market_complete[
        [
            "date",
            "EBP_QUARTER_END",
            "VIX_QUARTER_MEAN",
            "D_EBP_QUARTERLY",
            "D_VIX_QUARTERLY",
        ]
    ]
    .tail()
    .to_string(index=False)
)

# ------------------------------------------------------------
# Align Kargar wealth share with quarterly EBP / VIX
# ------------------------------------------------------------

kargar_for_merge = kargar_data[
    [
        "date",
        "BD_WEALTH_SHARE",
    ]
].copy()

# FRED Financial Accounts dates are quarter-start labels.
# Convert both datasets to a common quarterly Period key.
kargar_for_merge["quarter"] = (
    kargar_for_merge["date"]
    .dt.to_period("Q")
)

market_for_merge = (
    quarterly_market_complete[
        [
            "date",
            "EBP_QUARTER_END",
            "VIX_QUARTER_MEAN",
            "D_EBP_QUARTERLY",
            "D_VIX_QUARTERLY",
        ]
    ]
    .copy()
)

market_for_merge["quarter"] = (
    market_for_merge["date"]
    .dt.to_period("Q")
)

kargar_ebp = market_for_merge.merge(
    kargar_for_merge[
        [
            "quarter",
            "BD_WEALTH_SHARE",
        ]
    ],
    on="quarter",
    how="inner",
    validate="one_to_one",
)

print()
print("=" * 60)
print("KARGAR WEALTH SHARE / EBP - QUARTERLY MERGE CHECK")
print("=" * 60)

print()
print(f"Observations: {len(kargar_ebp):,}")

print(
    f"Quarter range: "
    f"{kargar_ebp['quarter'].min()} "
    f"to {kargar_ebp['quarter'].max()}"
)

print()
print("Missing values:")
print(
    kargar_ebp[
        [
            "EBP_QUARTER_END",
            "VIX_QUARTER_MEAN",
            "D_EBP_QUARTERLY",
            "D_VIX_QUARTERLY",
            "BD_WEALTH_SHARE",
        ]
    ].isna().sum()
)

print()
print("Last five:")
print(
    kargar_ebp[
        [
            "quarter",
            "EBP_QUARTER_END",
            "VIX_QUARTER_MEAN",
            "BD_WEALTH_SHARE",
        ]
    ]
    .tail()
    .to_string(index=False)
)

# ------------------------------------------------------------
# Kargar wealth share / EBP - level diagnostics
# ------------------------------------------------------------

kargar_level = kargar_ebp[
    [
        "quarter",
        "EBP_QUARTER_END",
        "VIX_QUARTER_MEAN",
        "BD_WEALTH_SHARE",
    ]
].dropna().copy()

print()
print("=" * 60)
print("KARGAR WEALTH SHARE / EBP - LEVEL DIAGNOSTICS")
print("=" * 60)

print()
print(f"Observations: {len(kargar_level):,}")

print()
print("Correlation matrix:")
print(
    kargar_level[
        [
            "EBP_QUARTER_END",
            "VIX_QUARTER_MEAN",
            "BD_WEALTH_SHARE",
        ]
    ].corr()
)

print()
print("EBP autocorrelation:")
for lag in [1, 2, 4]:
    print(
        f"lag {lag}: "
        f"{kargar_level['EBP_QUARTER_END'].autocorr(lag=lag):.4f}"
    )

print()
print("BD wealth-share autocorrelation:")
for lag in [1, 2, 4]:
    print(
        f"lag {lag}: "
        f"{kargar_level['BD_WEALTH_SHARE'].autocorr(lag=lag):.4f}"
    )

adf_ebp_q = adfuller(
    kargar_level["EBP_QUARTER_END"],
    autolag="AIC",
)

adf_bd_share = adfuller(
    kargar_level["BD_WEALTH_SHARE"],
    autolag="AIC",
)

print()
print("ADF tests:")
print(
    f"Quarter-end EBP: "
    f"stat={adf_ebp_q[0]:.4f}, "
    f"p={adf_ebp_q[1]:.6f}"
)

print(
    f"BD wealth share: "
    f"stat={adf_bd_share[0]:.4f}, "
    f"p={adf_bd_share[1]:.6f}"
)

# ------------------------------------------------------------
# Kargar-inspired predictive test
# BD wealth share(t) -> Delta EBP(t+1)
# ------------------------------------------------------------

kargar_predictive = kargar_ebp[
    [
        "quarter",
        "BD_WEALTH_SHARE",
        "VIX_QUARTER_MEAN",
        "D_EBP_QUARTERLY",
    ]
].copy()

# Next quarter's change in EBP
kargar_predictive["D_EBP_NEXT_Q"] = (
    kargar_predictive["D_EBP_QUARTERLY"]
    .shift(-1)
)

kargar_predictive = kargar_predictive.dropna(
    subset=[
        "BD_WEALTH_SHARE",
        "VIX_QUARTER_MEAN",
        "D_EBP_NEXT_Q",
    ]
)

y_pred = kargar_predictive["D_EBP_NEXT_Q"]

# Model 1: BD wealth share only
X_bd = sm.add_constant(
    kargar_predictive[
        ["BD_WEALTH_SHARE"]
    ]
)

model_bd_pred = sm.OLS(
    y_pred,
    X_bd,
).fit(
    cov_type="HAC",
    cov_kwds={"maxlags": 4},
)

# Model 2: VIX only
X_vix_q = sm.add_constant(
    kargar_predictive[
        ["VIX_QUARTER_MEAN"]
    ]
)

model_vix_pred = sm.OLS(
    y_pred,
    X_vix_q,
).fit(
    cov_type="HAC",
    cov_kwds={"maxlags": 4},
)

# Model 3: VIX + BD wealth share
X_bd_vix = sm.add_constant(
    kargar_predictive[
        [
            "VIX_QUARTER_MEAN",
            "BD_WEALTH_SHARE",
        ]
    ]
)

model_bd_vix_pred = sm.OLS(
    y_pred,
    X_bd_vix,
).fit(
    cov_type="HAC",
    cov_kwds={"maxlags": 4},
)

print()
print("=" * 60)
print("KARGAR-INSPIRED PREDICTIVE TEST")
print("BD WEALTH SHARE(t) -> DELTA EBP(t+1)")
print("=" * 60)

print()
print(f"Observations: {len(kargar_predictive):,}")

print()
print("BD WEALTH SHARE ONLY")
print(
    f"BD share coefficient: "
    f"{model_bd_pred.params['BD_WEALTH_SHARE']:.6f}"
)
print(
    f"BD share p-value: "
    f"{model_bd_pred.pvalues['BD_WEALTH_SHARE']:.6f}"
)
print(
    f"R-squared: "
    f"{model_bd_pred.rsquared:.6f}"
)

print()
print("VIX ONLY")
print(
    f"VIX coefficient: "
    f"{model_vix_pred.params['VIX_QUARTER_MEAN']:.6f}"
)
print(
    f"VIX p-value: "
    f"{model_vix_pred.pvalues['VIX_QUARTER_MEAN']:.6f}"
)
print(
    f"R-squared: "
    f"{model_vix_pred.rsquared:.6f}"
)

print()
print("VIX + BD WEALTH SHARE")
print(
    f"VIX coefficient: "
    f"{model_bd_vix_pred.params['VIX_QUARTER_MEAN']:.6f}"
)
print(
    f"VIX p-value: "
    f"{model_bd_vix_pred.pvalues['VIX_QUARTER_MEAN']:.6f}"
)
print(
    f"BD share coefficient: "
    f"{model_bd_vix_pred.params['BD_WEALTH_SHARE']:.6f}"
)
print(
    f"BD share p-value: "
    f"{model_bd_vix_pred.pvalues['BD_WEALTH_SHARE']:.6f}"
)
print(
    f"R-squared: "
    f"{model_bd_vix_pred.rsquared:.6f}"
)

print()
print(
    "Incremental R-squared from BD wealth share: "
    f"{model_bd_vix_pred.rsquared - model_vix_pred.rsquared:.6f}"
)
# ------------------------------------------------------------
# Kargar robustness test:
# Delta BD wealth share(t) -> Delta EBP(t+1)
# ------------------------------------------------------------

kargar_robust = kargar_ebp[
    [
        "quarter",
        "BD_WEALTH_SHARE",
        "VIX_QUARTER_MEAN",
        "D_EBP_QUARTERLY",
    ]
].copy()

kargar_robust["D_BD_WEALTH_SHARE"] = (
    kargar_robust["BD_WEALTH_SHARE"].diff()
)

kargar_robust["D_EBP_NEXT_Q"] = (
    kargar_robust["D_EBP_QUARTERLY"].shift(-1)
)

kargar_robust = kargar_robust.dropna(
    subset=[
        "D_BD_WEALTH_SHARE",
        "VIX_QUARTER_MEAN",
        "D_EBP_NEXT_Q",
    ]
)

# Stationarity check
adf_d_bd = adfuller(
    kargar_robust["D_BD_WEALTH_SHARE"],
    autolag="AIC",
)

print()
print("=" * 60)
print("DELTA BD WEALTH SHARE - ROBUSTNESS TEST")
print("=" * 60)

print()
print(f"Observations: {len(kargar_robust):,}")

print()
print(
    f"ADF statistic: {adf_d_bd[0]:.4f}"
)
print(
    f"ADF p-value: {adf_d_bd[1]:.6f}"
)

# Predictive regression
y_robust = kargar_robust["D_EBP_NEXT_Q"]

X_robust = sm.add_constant(
    kargar_robust[
        [
            "VIX_QUARTER_MEAN",
            "D_BD_WEALTH_SHARE",
        ]
    ]
)

model_robust = sm.OLS(
    y_robust,
    X_robust,
).fit(
    cov_type="HAC",
    cov_kwds={"maxlags": 4},
)

print()
print("VIX + DELTA BD WEALTH SHARE")

print(
    f"VIX coefficient: "
    f"{model_robust.params['VIX_QUARTER_MEAN']:.6f}"
)

print(
    f"VIX p-value: "
    f"{model_robust.pvalues['VIX_QUARTER_MEAN']:.6f}"
)

print(
    f"Delta BD share coefficient: "
    f"{model_robust.params['D_BD_WEALTH_SHARE']:.6f}"
)

print(
    f"Delta BD share p-value: "
    f"{model_robust.pvalues['D_BD_WEALTH_SHARE']:.6f}"
)

print(
    f"R-squared: "
    f"{model_robust.rsquared:.6f}"
)

# ------------------------------------------------------------
# V2 mechanism summary
# ------------------------------------------------------------

print()
print("=" * 60)
print("V2 CREDIT DYNAMICS - MECHANISM SUMMARY")
print("=" * 60)

print()
print("MONTHLY CONTEMPORANEOUS RESULTS")

print(
    "VIX-only full-sample R-squared: "
    f"{change_model.rsquared:.6f}"
)

print(
    "VIX + 10Y full-sample R-squared: "
    f"{vix_treasury_model.rsquared:.6f}"
)

print(
    "Incremental R-squared from 10Y: "
    f"{vix_treasury_model.rsquared - change_model.rsquared:.6f}"
)

print()
print("COMMON-SAMPLE INTERMEDIARY RESULTS")

print(
    "Fails incremental R-squared: "
    f"{model_intermediary.rsquared - model_vix_common.rsquared:.6f}"
)

print(
    "HY dealer position incremental R-squared: "
    f"{model_hy_full.rsquared - model_hy_vix.rsquared:.6f}"
)

print()
print("QUARTERLY KARGAR-INSPIRED RESULT")

print(
    "BD wealth-share level incremental R-squared: "
    f"{model_bd_vix_pred.rsquared - model_vix_pred.rsquared:.6f}"
)

print(
    "BD wealth-share level p-value: "
    f"{model_bd_vix_pred.pvalues['BD_WEALTH_SHARE']:.6f}"
)

print(
    "Delta BD wealth-share robustness p-value: "
    f"{model_robust.pvalues['D_BD_WEALTH_SHARE']:.6f}"
)

print()
print("PREDICTIVE VIX RESULT")

print(
    "Monthly Delta VIX(t) -> Delta EBP(t+1) R-squared: "
    f"{lead_change_model.rsquared:.6f}"
)

# ------------------------------------------------------------
# V2 mechanism comparison table
# ------------------------------------------------------------

mechanism_summary = pd.DataFrame(
    [
        {
            "MODEL": "Monthly: Delta EBP ~ Delta VIX",
            "FREQUENCY": "Monthly",
            "N": int(change_model.nobs),
            "FOCAL_VARIABLE": "Delta VIX",
            "FOCAL_COEFFICIENT": change_model.params["delta_vix"],
            "FOCAL_P_VALUE": change_model.pvalues["delta_vix"],
            "R_SQUARED": change_model.rsquared,
            "INCREMENTAL_R_SQUARED": pd.NA,
            "INTERPRETATION": (
                "Strong contemporaneous association; "
                "not evidence of forecasting."
            ),
        },
        {
            "MODEL": "Monthly: Delta EBP ~ Delta VIX + Delta 10Y",
            "FREQUENCY": "Monthly",
            "N": int(vix_treasury_model.nobs),
            "FOCAL_VARIABLE": "Delta 10Y Treasury",
            "FOCAL_COEFFICIENT": (
                vix_treasury_model.params["delta_treasury_10y"]
            ),
            "FOCAL_P_VALUE": (
                vix_treasury_model.pvalues["delta_treasury_10y"]
            ),
            "R_SQUARED": vix_treasury_model.rsquared,
            "INCREMENTAL_R_SQUARED": (
                vix_treasury_model.rsquared
                - change_model.rsquared
            ),
            "INTERPRETATION": (
                "Little incremental explanatory power beyond Delta VIX."
            ),
        },
        {
            "MODEL": "Monthly: Delta EBP ~ Delta VIX + Delta Fails",
            "FREQUENCY": "Monthly",
            "N": int(model_intermediary.nobs),
            "FOCAL_VARIABLE": "Delta Corporate Fails to Deliver",
            "FOCAL_COEFFICIENT": (
                model_intermediary.params["D_FAILS_DELIVER"]
            ),
            "FOCAL_P_VALUE": (
                model_intermediary.pvalues["D_FAILS_DELIVER"]
            ),
            "R_SQUARED": model_intermediary.rsquared,
            "INCREMENTAL_R_SQUARED": (
                model_intermediary.rsquared
                - model_vix_common.rsquared
            ),
            "INTERPRETATION": (
                "Weak incremental settlement/intermediation signal."
            ),
        },
        {
            "MODEL": (
                "Monthly: Delta EBP ~ Delta VIX "
                "+ Delta HY Dealer Position"
            ),
            "FREQUENCY": "Monthly",
            "N": int(model_hy_full.nobs),
            "FOCAL_VARIABLE": "Delta HY Dealer Net Position",
            "FOCAL_COEFFICIENT": (
                model_hy_full.params["D_HY_DEALER_POSITION"]
            ),
            "FOCAL_P_VALUE": (
                model_hy_full.pvalues["D_HY_DEALER_POSITION"]
            ),
            "R_SQUARED": model_hy_full.rsquared,
            "INCREMENTAL_R_SQUARED": (
                model_hy_full.rsquared
                - model_hy_vix.rsquared
            ),
            "INTERPRETATION": (
                "Dealer inventory adds essentially no information "
                "beyond Delta VIX."
            ),
        },
        {
            "MODEL": (
                "Quarterly: Delta EBP(t+1) ~ VIX(t) "
                "+ BD Wealth Share(t)"
            ),
            "FREQUENCY": "Quarterly",
            "N": int(model_bd_vix_pred.nobs),
            "FOCAL_VARIABLE": "BD Wealth Share",
            "FOCAL_COEFFICIENT": (
                model_bd_vix_pred.params["BD_WEALTH_SHARE"]
            ),
            "FOCAL_P_VALUE": (
                model_bd_vix_pred.pvalues["BD_WEALTH_SHARE"]
            ),
            "R_SQUARED": model_bd_vix_pred.rsquared,
            "INCREMENTAL_R_SQUARED": (
                model_bd_vix_pred.rsquared
                - model_vix_pred.rsquared
            ),
            "INTERPRETATION": (
                "Suggestive predictive level result; "
                "highly persistent predictor."
            ),
        },
        {
            "MODEL": (
                "Quarterly robustness: Delta EBP(t+1) ~ VIX(t) "
                "+ Delta BD Wealth Share(t)"
            ),
            "FREQUENCY": "Quarterly",
            "N": int(model_robust.nobs),
            "FOCAL_VARIABLE": "Delta BD Wealth Share",
            "FOCAL_COEFFICIENT": (
                model_robust.params["D_BD_WEALTH_SHARE"]
            ),
            "FOCAL_P_VALUE": (
                model_robust.pvalues["D_BD_WEALTH_SHARE"]
            ),
            "R_SQUARED": model_robust.rsquared,
            "INCREMENTAL_R_SQUARED": pd.NA,
            "INTERPRETATION": (
                "Stationary robustness test does not confirm "
                "the level result."
            ),
        },
        {
            "MODEL": "Monthly predictive: Delta EBP(t+1) ~ Delta VIX(t)",
            "FREQUENCY": "Monthly",
            "N": int(lead_change_model.nobs),
            "FOCAL_VARIABLE": "Lagged Delta VIX",
            "FOCAL_COEFFICIENT": (
                lead_change_model.params["delta_vix"]
            ),
            "FOCAL_P_VALUE": (
                lead_change_model.pvalues["delta_vix"]
            ),
            "R_SQUARED": lead_change_model.rsquared,
            "INCREMENTAL_R_SQUARED": pd.NA,
            "INTERPRETATION": (
                "Little next-month predictive power."
            ),
        },
    ]
)

print()
print("=" * 60)
print("V2 MECHANISM COMPARISON TABLE")
print("=" * 60)

print()
print(
    mechanism_summary[
        [
            "MODEL",
            "N",
            "FOCAL_VARIABLE",
            "FOCAL_COEFFICIENT",
            "FOCAL_P_VALUE",
            "R_SQUARED",
            "INCREMENTAL_R_SQUARED",
        ]
    ].to_string(index=False)
)

MECHANISM_SUMMARY_PATH = (
    PROJECT_ROOT
    / "reports"
    / "tables"
    / "v2_mechanism_comparison.csv"
)

MECHANISM_SUMMARY_PATH.parent.mkdir(
    parents=True,
    exist_ok=True,
)

mechanism_summary.to_csv(
    MECHANISM_SUMMARY_PATH,
    index=False,
)

print()
print(f"Saved: {MECHANISM_SUMMARY_PATH}")

# ------------------------------------------------------------
# Figure 1: Monthly Delta EBP vs Delta VIX
# ------------------------------------------------------------

import matplotlib.pyplot as plt

fig, ax = plt.subplots(
    figsize=(9, 6)
)

ax.scatter(
    change_data["delta_vix"],
    change_data["delta_ebp"],
    alpha=0.55,
    s=24,
)

# Regression line
x_line = np.linspace(
    change_data["delta_vix"].min(),
    change_data["delta_vix"].max(),
    100,
)

y_line = (
    change_model.params["const"]
    + change_model.params["delta_vix"] * x_line
)

ax.plot(
    x_line,
    y_line,
    linewidth=2,
)

ax.axhline(
    0,
    linewidth=0.8,
    alpha=0.5,
)

ax.axvline(
    0,
    linewidth=0.8,
    alpha=0.5,
)

ax.set_title(
    "Credit Risk Repricing and Changes in Market Uncertainty"
)

ax.set_xlabel(
    "Monthly Change in VIX"
)

ax.set_ylabel(
    "Monthly Change in Excess Bond Premium"
)

ax.text(
    0.03,
    0.95,
    (
        f"HAC coefficient = "
        f"{change_model.params['delta_vix']:.3f}\n"
        f"p < 0.001\n"
        f"R² = {change_model.rsquared:.3f}\n"
        f"N = {int(change_model.nobs)}"
    ),
    transform=ax.transAxes,
    verticalalignment="top",
)

fig.tight_layout()

FIGURE_DIR = (
    PROJECT_ROOT
    / "reports"
    / "figures"
)

FIGURE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

figure_1_path = (
    FIGURE_DIR
    / "v2_delta_ebp_vs_delta_vix.png"
)

fig.savefig(
    figure_1_path,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)

print()
print(f"Saved Figure 1: {figure_1_path}")

# ------------------------------------------------------------
# Figure 2: Incremental explanatory power
# ------------------------------------------------------------

mechanism_plot = pd.DataFrame(
    {
        "Mechanism": [
            "10Y Treasury\nchange",
            "Corporate\nfails",
            "HY dealer\nposition",
            "BD wealth\nshare*",
        ],
        "Incremental_R2": [
            (
                vix_treasury_model.rsquared
                - change_model.rsquared
            ),
            (
                model_intermediary.rsquared
                - model_vix_common.rsquared
            ),
            (
                model_hy_full.rsquared
                - model_hy_vix.rsquared
            ),
            (
                model_bd_vix_pred.rsquared
                - model_vix_pred.rsquared
            ),
        ],
    }
)

fig, ax = plt.subplots(
    figsize=(9, 5.5)
)

bars = ax.bar(
    mechanism_plot["Mechanism"],
    mechanism_plot["Incremental_R2"],
)

ax.set_title(
    "Incremental Explanatory Power Beyond the VIX Benchmark"
)

ax.set_ylabel(
    "Incremental R²"
)

ax.set_ylim(
    0,
    mechanism_plot["Incremental_R2"].max() * 1.25,
)

for bar, value in zip(
    bars,
    mechanism_plot["Incremental_R2"],
):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.001,
        f"{value:.3f}",
        ha="center",
        va="bottom",
    )

ax.text(
    0.99,
    0.95,
    (
        "* Quarterly predictive BD wealth-share level.\n"
        "  Significant in levels but not robust to\n"
        "  stationary first-difference specification."
    ),
    transform=ax.transAxes,
    ha="right",
    va="top",
    fontsize=9,
)

fig.tight_layout()

figure_2_path = (
    FIGURE_DIR
    / "v2_incremental_mechanism_r2.png"
)

fig.savefig(
    figure_2_path,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)

print()
print(f"Saved Figure 2: {figure_2_path}")

# ------------------------------------------------------------
# Figure 3: Broker-dealer wealth share through time
# ------------------------------------------------------------

kargar_plot = kargar_data[
    kargar_data["date"] >= "1990-01-01"
].copy()

fig, ax = plt.subplots(
    figsize=(10, 5.5)
)

ax.plot(
    kargar_plot["date"],
    kargar_plot["BD_WEALTH_SHARE"],
    linewidth=1.8,
)

ax.set_title(
    "Broker-Dealer Share of Intermediary Equity"
)

ax.set_xlabel(
    "Year"
)

ax.set_ylabel(
    "Broker-Dealer Wealth Share"
)

# Financial crisis reference
ax.axvspan(
    pd.Timestamp("2007-12-01"),
    pd.Timestamp("2009-06-30"),
    alpha=0.12,
)

# COVID shock reference
ax.axvspan(
    pd.Timestamp("2020-02-01"),
    pd.Timestamp("2020-06-30"),
    alpha=0.12,
)

ax.text(
    pd.Timestamp("2008-09-01"),
    0.25,
    "Global\nFinancial Crisis",
    ha="center",
    fontsize=9,
)

ax.text(
    pd.Timestamp("2020-04-01"),
    0.25,
    "COVID",
    ha="center",
    fontsize=9,
)

fig.tight_layout()

figure_3_path = (
    FIGURE_DIR
    / "v2_bd_wealth_share.png"
)

fig.savefig(
    figure_3_path,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)

print()
print(f"Saved Figure 3: {figure_3_path}")