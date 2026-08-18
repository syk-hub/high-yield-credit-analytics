from pathlib import Path
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller

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
