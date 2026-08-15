from pathlib import Path

import pandas as pd

import statsmodels.api as sm


# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

SAMPLE_B_FILE = (
    PROCESSED_DIR
    / "v2_macro_credit_monthly.csv"
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