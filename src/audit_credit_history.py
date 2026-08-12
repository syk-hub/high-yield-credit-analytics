"""Audit long-history credit data used in Version 2 research.

Current scope:
- Federal Reserve Excess Bond Premium (EBP)
- ICE BofA US High Yield OAS overlap validation

This script is for provenance, history, frequency, missingness,
and later overlap-validation work. It does not perform regime
classification, predictive modeling, or machine learning.
"""

from datetime import date
from pathlib import Path

import pandas as pd


# ---------------------------------------------------------
# 1. Define project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# 2. Audit metadata
# ---------------------------------------------------------

EXTRACTION_DATE = date.today().isoformat()

EBP_METADATA = {
    "series_name": "Excess Bond Premium",
    "provider": "Federal Reserve Board",
    "frequency": "Monthly",
    "intended_v2_use": "Long-history corporate credit risk-premium indicator",
    "hy_oas_equivalent": False,
}

# ---------------------------------------------------------
# 3. Download official Federal Reserve EBP data
# ---------------------------------------------------------

EBP_URL = (
    "https://www.federalreserve.gov/"
    "econres/notes/feds-notes/ebp_csv.csv"
)

import io
import requests

# ---------------------------------------------------------
# 3. Download official Federal Reserve EBP data
# ---------------------------------------------------------

EBP_URL = (
    "https://www.federalreserve.gov/"
    "econres/notes/feds-notes/ebp_csv.csv"
)

print("Downloading Federal Reserve Excess Bond Premium data...")

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

response = requests.get(
    EBP_URL,
    headers=headers,
    timeout=30,
)

response.raise_for_status()

ebp_raw = pd.read_csv(
    io.StringIO(response.text)
)

print()
print("EBP download complete.")
print(f"Rows: {len(ebp_raw):,}")
print()
print("Columns:")
print(ebp_raw.columns.tolist())
print()
print("First five rows:")
print(ebp_raw.head())
print()
print("Last five rows:")
print(ebp_raw.tail())

# ---------------------------------------------------------
# 4. Save raw EBP snapshot
# ---------------------------------------------------------

ebp_snapshot_file = (
    RAW_DATA_DIR
    / f"fed_ebp_snapshot_{EXTRACTION_DATE}.csv"
)

ebp_raw.to_csv(
    ebp_snapshot_file,
    index=False,
)

print()
print(f"Raw EBP snapshot saved to: {ebp_snapshot_file}")

# ---------------------------------------------------------
# 5. Audit EBP history and data quality
# ---------------------------------------------------------

ebp_audit = ebp_raw.copy()

ebp_audit["date"] = pd.to_datetime(
    ebp_audit["date"]
)

numeric_columns = [
    "gz_spread",
    "ebp",
    "est_prob",
]

for column in numeric_columns:
    ebp_audit[column] = pd.to_numeric(
        ebp_audit[column],
        errors="coerce",
    )

print()
print("=" * 60)
print("EBP DATA HISTORY AUDIT")
print("=" * 60)

print(f"First observation: {ebp_audit['date'].min().date()}")
print(f"Latest observation: {ebp_audit['date'].max().date()}")
print(f"Total observations: {len(ebp_audit):,}")
print(f"Duplicate dates: {ebp_audit['date'].duplicated().sum()}")

print()
print("Missing values:")
print(ebp_audit.isna().sum())

# ---------------------------------------------------------
# 6. Load existing ICE BofA HY OAS snapshot
# ---------------------------------------------------------

HY_OAS_FILE = (
    RAW_DATA_DIR
    / "fred_BAMLH0A0HYM2_snapshot_2026-07-28.csv"
)

hy_oas = pd.read_csv(HY_OAS_FILE)

hy_oas["Date"] = pd.to_datetime(
    hy_oas["Date"]
)

hy_oas["HY_OAS_PERCENT"] = pd.to_numeric(
    hy_oas["HY_OAS_PERCENT"],
    errors="coerce",
)

print()
print("=" * 60)
print("ICE BOFA HY OAS HISTORY AUDIT")
print("=" * 60)

print(f"First observation: {hy_oas['Date'].min().date()}")
print(f"Latest observation: {hy_oas['Date'].max().date()}")
print(f"Total observations: {len(hy_oas):,}")
print(f"Duplicate dates: {hy_oas['Date'].duplicated().sum()}")

print()
print("Missing values:")
print(hy_oas.isna().sum())

# ---------------------------------------------------------
# 7. Inspect missing HY OAS observations
# ---------------------------------------------------------

missing_hy_oas = hy_oas[
    hy_oas["HY_OAS_PERCENT"].isna()
]

print()
print("HY OAS missing observations:")
print(missing_hy_oas)

# ---------------------------------------------------------
# 8. Align HY OAS to monthly EBP frequency
# ---------------------------------------------------------

# Keep valid HY OAS market observations only.
hy_oas_valid = hy_oas.dropna(
    subset=["HY_OAS_PERCENT"]
).copy()

# Assign each daily observation to its calendar month.
hy_oas_valid["month"] = (
    hy_oas_valid["Date"].dt.to_period("M")
)

# Primary specification:
# average of valid daily HY OAS observations within each month.
hy_oas_monthly_mean = (
    hy_oas_valid
    .groupby("month", as_index=False)
    ["HY_OAS_PERCENT"]
    .mean()
    .rename(
        columns={
            "HY_OAS_PERCENT": "HY_OAS_MONTHLY_MEAN"
        }
    )
)

# Robustness specification:
# final valid market observation within each month.
hy_oas_monthly_end = (
    hy_oas_valid
    .sort_values("Date")
    .groupby("month", as_index=False)
    .last()[["month", "Date", "HY_OAS_PERCENT"]]
    .rename(
        columns={
            "Date": "HY_OAS_MONTH_END_DATE",
            "HY_OAS_PERCENT": "HY_OAS_MONTH_END",
        }
    )
)

# Prepare EBP month identifier.
ebp_audit["month"] = (
    ebp_audit["date"].dt.to_period("M")
)

# Combine EBP with both HY OAS monthly specifications.
overlap = (
    ebp_audit[
        ["month", "date", "ebp", "gz_spread", "est_prob"]
    ]
    .merge(
        hy_oas_monthly_mean,
        on="month",
        how="inner",
    )
    .merge(
        hy_oas_monthly_end,
        on="month",
        how="inner",
    )
)

# Restrict formal validation to complete overlap months.
overlap = overlap[
    (overlap["month"] >= pd.Period("2023-08", freq="M"))
    & (overlap["month"] <= pd.Period("2026-06", freq="M"))
].copy()

print()
print("=" * 60)
print("EBP / HY OAS MONTHLY OVERLAP")
print("=" * 60)

print(f"First complete month: {overlap['month'].min()}")
print(f"Last complete month: {overlap['month'].max()}")
print(f"Complete overlapping months: {len(overlap)}")

print()
print("First five aligned observations:")
print(overlap.head())

print()
print("Last five aligned observations:")
print(overlap.tail())

print()
print("Missing values in overlap dataset:")
print(overlap.isna().sum())

# ---------------------------------------------------------
# 9. Initial EBP / HY OAS overlap diagnostics
# ---------------------------------------------------------

pearson_mean = overlap[
    ["ebp", "HY_OAS_MONTHLY_MEAN"]
].corr(method="pearson").iloc[0, 1]

spearman_mean = overlap[
    ["ebp", "HY_OAS_MONTHLY_MEAN"]
].corr(method="spearman").iloc[0, 1]

pearson_end = overlap[
    ["ebp", "HY_OAS_MONTH_END"]
].corr(method="pearson").iloc[0, 1]

spearman_end = overlap[
    ["ebp", "HY_OAS_MONTH_END"]
].corr(method="spearman").iloc[0, 1]

print()
print("=" * 60)
print("INITIAL EBP / HY OAS DIAGNOSTICS")
print("=" * 60)

print("Monthly mean HY OAS:")
print(f"Pearson correlation:  {pearson_mean:.3f}")
print(f"Spearman correlation: {spearman_mean:.3f}")

print()
print("Month-end HY OAS:")
print(f"Pearson correlation:  {pearson_end:.3f}")
print(f"Spearman correlation: {spearman_end:.3f}")

# ---------------------------------------------------------
# 10. Month-to-month change diagnostics
# ---------------------------------------------------------

overlap["EBP_CHANGE"] = overlap["ebp"].diff()

overlap["HY_OAS_MEAN_CHANGE"] = (
    overlap["HY_OAS_MONTHLY_MEAN"].diff()
)

change_sample = overlap.dropna(
    subset=["EBP_CHANGE", "HY_OAS_MEAN_CHANGE"]
)

pearson_change = change_sample[
    ["EBP_CHANGE", "HY_OAS_MEAN_CHANGE"]
].corr(method="pearson").iloc[0, 1]

spearman_change = change_sample[
    ["EBP_CHANGE", "HY_OAS_MEAN_CHANGE"]
].corr(method="spearman").iloc[0, 1]

print()
print("=" * 60)
print("MONTH-TO-MONTH CHANGE DIAGNOSTICS")
print("=" * 60)

print(f"Observations: {len(change_sample)}")
print(f"Pearson correlation:  {pearson_change:.3f}")
print(f"Spearman correlation: {spearman_change:.3f}")

# ---------------------------------------------------------
# 11. Audit remaining ICE BofA HY series
# ---------------------------------------------------------

ICE_SERIES_FILES = {
    "HY_EFFECTIVE_YIELD": (
        RAW_DATA_DIR
        / "fred_BAMLH0A0HYM2EY_snapshot_2026-07-28.csv"
    ),
    "HY_TOTAL_RETURN_INDEX": (
        RAW_DATA_DIR
        / "fred_BAMLHYH0A0HYM2TRIV_snapshot_2026-07-28.csv"
    ),
}

for series_name, file_path in ICE_SERIES_FILES.items():

    data = pd.read_csv(file_path)

    data["Date"] = pd.to_datetime(
        data["Date"]
    )

    data[series_name] = pd.to_numeric(
        data[series_name],
        errors="coerce",
    )

    print()
    print("=" * 60)
    print(f"{series_name} HISTORY AUDIT")
    print("=" * 60)

    print(f"First observation: {data['Date'].min().date()}")
    print(f"Latest observation: {data['Date'].max().date()}")
    print(f"Total observations: {len(data):,}")
    print(f"Duplicate dates: {data['Date'].duplicated().sum()}")

    print()
    print("Missing values:")
    print(data.isna().sum())

    missing_rows = data[
        data[series_name].isna()
    ]

    print()
    print("Missing observation dates:")
    print(
        missing_rows["Date"]
        .dt.date
        .tolist()
    )

    # ---------------------------------------------------------
# 12. Audit VIX history
# ---------------------------------------------------------

VIX_FILE = (
    RAW_DATA_DIR
    / "fred_VIXCLS_snapshot_2026-07-28.csv"
)

vix = pd.read_csv(VIX_FILE)

vix["Date"] = pd.to_datetime(
    vix["Date"]
)

vix["VIX"] = pd.to_numeric(
    vix["VIX"],
    errors="coerce",
)

print()
print("=" * 60)
print("VIX HISTORY AUDIT")
print("=" * 60)

print(f"First observation: {vix['Date'].min().date()}")
print(f"Latest observation: {vix['Date'].max().date()}")
print(f"Total observations: {len(vix):,}")
print(f"Duplicate dates: {vix['Date'].duplicated().sum()}")

print()
print("Missing values:")
print(vix.isna().sum())

print()
print(
    f"Missing VIX observations: "
    f"{vix['VIX'].isna().sum():,}"
)

# ---------------------------------------------------------
# 13. Audit Treasury and policy-rate series
# ---------------------------------------------------------

RATE_SERIES_FILES = {
    "TREASURY_10Y": (
        RAW_DATA_DIR
        / "fred_DGS10_snapshot_2026-07-28.csv"
    ),
    "EFFR": (
        RAW_DATA_DIR
        / "fred_EFFR_snapshot_2026-07-28.csv"
    ),
}

for series_name, file_path in RATE_SERIES_FILES.items():

    data = pd.read_csv(file_path)

    data["Date"] = pd.to_datetime(
        data["Date"]
    )

    data[series_name] = pd.to_numeric(
        data[series_name],
        errors="coerce",
    )

    print()
    print("=" * 60)
    print(f"{series_name} HISTORY AUDIT")
    print("=" * 60)

    print(f"First observation: {data['Date'].min().date()}")
    print(f"Latest observation: {data['Date'].max().date()}")
    print(f"Total observations: {len(data):,}")
    print(f"Duplicate dates: {data['Date'].duplicated().sum()}")
    print(f"Missing observations: {data[series_name].isna().sum():,}")

# ---------------------------------------------------------
# 14. Audit macroeconomic series
# ---------------------------------------------------------

MACRO_SERIES_FILES = {
    "UNEMPLOYMENT_RATE": (
        RAW_DATA_DIR
        / "fred_UNRATE_snapshot_2026-07-28.csv"
    ),
    "RECESSION_FLAG": (
        RAW_DATA_DIR
        / "fred_USREC_snapshot_2026-07-28.csv"
    ),
}

for series_name, file_path in MACRO_SERIES_FILES.items():

    data = pd.read_csv(file_path)

    data["Date"] = pd.to_datetime(
        data["Date"]
    )

    data[series_name] = pd.to_numeric(
        data[series_name],
        errors="coerce",
    )

    print()
    print("=" * 60)
    print(f"{series_name} HISTORY AUDIT")
    print("=" * 60)

    print(f"First observation: {data['Date'].min().date()}")
    print(f"Latest observation: {data['Date'].max().date()}")
    print(f"Total observations: {len(data):,}")
    print(f"Duplicate dates: {data['Date'].duplicated().sum()}")
    print(
        f"Missing observations: "
        f"{data[series_name].isna().sum():,}"
    )

    unemployment_file = (
    RAW_DATA_DIR
    / "fred_UNRATE_snapshot_2026-07-28.csv"
)

unemployment_check = pd.read_csv(unemployment_file)

unemployment_check["Date"] = pd.to_datetime(
    unemployment_check["Date"]
)

print()
print("Missing unemployment observation:")
print(
    unemployment_check.loc[
        unemployment_check["UNEMPLOYMENT_RATE"].isna()
    ]
)