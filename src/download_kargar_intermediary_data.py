from pathlib import Path
import os

import pandas as pd
import requests
from dotenv import load_dotenv


# ------------------------------------------------------------
# Paths / environment
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"

RAW_DIR.mkdir(parents=True, exist_ok=True)

load_dotenv(PROJECT_ROOT / ".env")

FRED_API_KEY = os.getenv("FRED_API_KEY")

if not FRED_API_KEY:
    raise ValueError("FRED_API_KEY not found in .env")


# ------------------------------------------------------------
# Kargar-style intermediary wealth-share inputs
# ------------------------------------------------------------

SERIES = {
    "BD_ASSETS": "BOGZ1FL664090005Q",
    "BD_LIABILITIES": "BOGZ1FL664190005Q",
    "BD_MISC_LIABILITIES": "BOGZ1FL663190005Q",
    "BANK_ASSETS": "BOGZ1FL764090005Q",
    "BANK_LIABILITIES": "BOGZ1FL764190005Q",
    "BANK_MISC_LIABILITIES": "BOGZ1FL763193005Q",
}


def download_fred_series(series_id):

    url = "https://api.stlouisfed.org/fred/series/observations"

    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
    }

    response = requests.get(
        url,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    observations = response.json()["observations"]

    df = pd.DataFrame(observations)

    df["date"] = pd.to_datetime(df["date"])

    df["value"] = pd.to_numeric(
        df["value"],
        errors="coerce",
    )

    return df[
        [
            "date",
            "value",
        ]
    ]


print()
print("=" * 60)
print("KARGAR INTERMEDIARY INPUTS - FRED INSPECTION")
print("=" * 60)

for label, series_id in SERIES.items():

    df = download_fred_series(series_id)

    print()
    print(label)
    print("-" * 60)

    print(f"Series ID: {series_id}")
    print(f"Rows: {len(df):,}")

    print(
        f"Date range: "
        f"{df['date'].min().date()} "
        f"to {df['date'].max().date()}"
    )

    print(
        f"Missing/non-numeric values: "
        f"{df['value'].isna().sum()}"
    )

    print()
    print("First five:")
    print(df.head().to_string(index=False))

    print()
    print("Last five:")
    print(df.tail().to_string(index=False))

    # ------------------------------------------------------------
# Kargar inputs - common-date completeness check
# ------------------------------------------------------------

frames = []

for label, series_id in SERIES.items():

    df = download_fred_series(series_id).rename(
        columns={"value": label}
    )

    frames.append(df)

kargar_inputs = frames[0]

for df in frames[1:]:

    kargar_inputs = kargar_inputs.merge(
        df,
        on="date",
        how="outer",
        validate="one_to_one",
    )

kargar_inputs = (
    kargar_inputs
    .sort_values("date")
    .reset_index(drop=True)
)

input_columns = list(SERIES.keys())

kargar_inputs["N_MISSING"] = (
    kargar_inputs[input_columns]
    .isna()
    .sum(axis=1)
)

print()
print("=" * 60)
print("KARGAR INPUTS - COMMON-DATE COMPLETENESS")
print("=" * 60)

print()
print(f"Total quarters: {len(kargar_inputs):,}")

print()
print("Missing series per quarter:")
print(
    kargar_inputs["N_MISSING"]
    .value_counts()
    .sort_index()
)

print()
print("Quarters with any missing inputs:")
print(
    kargar_inputs.loc[
        kargar_inputs["N_MISSING"] > 0,
        ["date", "N_MISSING"],
    ].to_string(index=False)
)

complete_inputs = (
    kargar_inputs[
        kargar_inputs["N_MISSING"] == 0
    ]
    .copy()
)

print()
print(f"Fully observed quarters: {len(complete_inputs):,}")

print(
    f"Complete-data range: "
    f"{complete_inputs['date'].min().date()} "
    f"to {complete_inputs['date'].max().date()}"
)

print()
print("First five complete quarters:")
print(
    complete_inputs[
        ["date"] + input_columns
    ]
    .head()
    .to_string(index=False)
)
# ------------------------------------------------------------
# Kargar-style intermediary wealth share
# ------------------------------------------------------------

kargar_constructed = (
    kargar_inputs[
        kargar_inputs["N_MISSING"] == 0
    ]
    .copy()
)

kargar_constructed["BD_EQUITY"] = (
    kargar_constructed["BD_ASSETS"]
    - (
        kargar_constructed["BD_LIABILITIES"]
        - kargar_constructed["BD_MISC_LIABILITIES"]
    )
)

kargar_constructed["BANK_EQUITY"] = (
    kargar_constructed["BANK_ASSETS"]
    - (
        kargar_constructed["BANK_LIABILITIES"]
        - kargar_constructed["BANK_MISC_LIABILITIES"]
    )
)

kargar_constructed["BD_WEALTH_SHARE"] = (
    kargar_constructed["BD_EQUITY"]
    / (
        kargar_constructed["BD_EQUITY"]
        + kargar_constructed["BANK_EQUITY"]
    )
)

print()
print("=" * 60)
print("KARGAR-STYLE INTERMEDIARY WEALTH SHARE")
print("=" * 60)

print()
print("Equity / wealth-share summary:")
print(
    kargar_constructed[
        [
            "BD_EQUITY",
            "BANK_EQUITY",
            "BD_WEALTH_SHARE",
        ]
    ].describe()
)

print()
print("Non-positive equity observations:")
print(
    "Broker-dealer:",
    (kargar_constructed["BD_EQUITY"] <= 0).sum()
)
print(
    "Commercial bank:",
    (kargar_constructed["BANK_EQUITY"] <= 0).sum()
)

print()
print("First five:")
print(
    kargar_constructed[
        [
            "date",
            "BD_EQUITY",
            "BANK_EQUITY",
            "BD_WEALTH_SHARE",
        ]
    ]
    .head()
    .to_string(index=False)
)

print()
print("Last ten:")
print(
    kargar_constructed[
        [
            "date",
            "BD_EQUITY",
            "BANK_EQUITY",
            "BD_WEALTH_SHARE",
        ]
    ]
    .tail(10)
    .to_string(index=False)
)

# ------------------------------------------------------------
# Kargar wealth share - modern sample inspection
# ------------------------------------------------------------

kargar_modern = (
    kargar_constructed[
        kargar_constructed["date"] >= "1990-01-01"
    ]
    .copy()
)

wealth_share = kargar_modern["BD_WEALTH_SHARE"]

print()
print("=" * 60)
print("KARGAR WEALTH SHARE - MODERN SAMPLE DIAGNOSTICS")
print("=" * 60)

print()
print(f"Observations: {len(kargar_modern):,}")

print(
    f"Date range: "
    f"{kargar_modern['date'].min().date()} "
    f"to {kargar_modern['date'].max().date()}"
)

print()
print("Wealth-share summary:")
print(wealth_share.describe())

print()
print("Autocorrelation:")
for lag in [1, 2, 4, 8]:
    print(
        f"lag {lag}: "
        f"{wealth_share.autocorr(lag=lag):.4f}"
    )

print()
print("Selected observations:")
selected_years = [
    1990,
    2000,
    2007,
    2009,
    2015,
    2020,
    2024,
    2026,
]

print(
    kargar_modern[
        kargar_modern["date"].dt.year.isin(selected_years)
    ][
        [
            "date",
            "BD_EQUITY",
            "BANK_EQUITY",
            "BD_WEALTH_SHARE",
        ]
    ].to_string(index=False)
)

# ------------------------------------------------------------
# Save Kargar-style intermediary dataset
# ------------------------------------------------------------

output_columns = [
    "date",
    "BD_ASSETS",
    "BD_LIABILITIES",
    "BD_MISC_LIABILITIES",
    "BANK_ASSETS",
    "BANK_LIABILITIES",
    "BANK_MISC_LIABILITIES",
    "BD_EQUITY",
    "BANK_EQUITY",
    "BD_WEALTH_SHARE",
]

output_file = (
    RAW_DIR
    / "fred_kargar_intermediary_wealth_share_quarterly.csv"
)

kargar_constructed[
    output_columns
].to_csv(
    output_file,
    index=False,
)

print()
print("=" * 60)
print("KARGAR INTERMEDIARY DATASET - SAVED")
print("=" * 60)

print()
print(f"Saved: {output_file}")
print(f"Rows: {len(kargar_constructed):,}")