from pathlib import Path
from io import StringIO

import pandas as pd
import requests


# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"

RAW_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# NY Fed Primary Dealer series
# ------------------------------------------------------------

HY_NET_POSITION_URL = (
    "https://markets.newyorkfed.org/api/pd/get/SBN2013/"
    "timeseries/PDPOSCSBND-BEL.csv"
)

HY_NET_POSITION_2015_URL = (
    "https://markets.newyorkfed.org/api/pd/get/SBN2015/timeseries/"
    "PDPOSCSBND-BELL13_PDPOSCSBND-BELG13_"
    "PDPOSCSBND-BELG5L10_PDPOSCSBND-BELG10.csv"
)

HY_NET_POSITION_2022_URL = (
    "https://markets.newyorkfed.org/api/pd/get/SBN2022/timeseries/"
    "PDPOSCSBND-BELL13_PDPOSCSBND-BELG13_"
    "PDPOSCSBND-BELG5L10_PDPOSCSBND-BELG10.csv"
)

HY_NET_POSITION_2024_URL = (
    "https://markets.newyorkfed.org/api/pd/get/SBN2024/timeseries/"
    "PDPOSCSBND-BELL13_PDPOSCSBND-BELG13_"
    "PDPOSCSBND-BELG5L10_PDPOSCSBND-BELG10.csv"
)

CORP_REVERSE_REPO_2013_URL = (
    "https://markets.newyorkfed.org/api/pd/get/SBN2013/timeseries/"
    "PDSIRRA-CD_PDSIRRA-CDTAL30_PDSIRRA-CDTAG30.csv"
)

CORP_REPO_2013_URL = (
    "https://markets.newyorkfed.org/api/pd/get/SBN2013/timeseries/"
    "PDSORA-CD_PDSORA-CDTAL30_PDSORA-CDTAG30.csv"
)

print("Downloading NY Fed HY dealer net-position data...")

response = requests.get(
    HY_NET_POSITION_URL,
    timeout=30,
)

CORP_REVERSE_REPO_2015_URL = (
    "https://markets.newyorkfed.org/api/pd/get/SBN2015/timeseries/"
    "PDSIRRA-CD_PDSIRRA-CDTAL30_PDSIRRA-CDTAG30.csv"
)

CORP_REPO_2015_URL = (
    "https://markets.newyorkfed.org/api/pd/get/SBN2015/timeseries/"
    "PDSORA-CD_PDSORA-CDTAL30_PDSORA-CDTAG30.csv"
)

CORP_REVERSE_REPO_2022_UB_URL = (
    "https://markets.newyorkfed.org/api/pd/get/SBN2022/timeseries/"
    "PDSIRRA-UBSCD_PDSIRRA-UBSCDTAL30_PDSIRRA-UBSCDTAG30_"
    "PDSIRRA-UBGCD_PDSIRRA-UBGCDTAL30_PDSIRRA-UBGCDTAG30.csv"
)

CORP_REVERSE_REPO_2022_CB_URL = (
    "https://markets.newyorkfed.org/api/pd/get/SBN2022/timeseries/"
    "PDSIRRA-CBSCD_PDSIRRA-CBSCDTAL30_PDSIRRA-CBSCDTAG30_"
    "PDSIRRA-CBGCD_PDSIRRA-CBGCDTAL30_PDSIRRA-CBGCDTAG30_"
    "PDSIRRA-CBSPCD_PDSIRRA-CBSPCDTAL30_PDSIRRA-CBSPCDTAG30.csv"
)

CORP_REVERSE_REPO_2022_GCF_TRI_URL = (
    "https://markets.newyorkfed.org/api/pd/get/SBN2022/timeseries/"
    "PDSIRRA-GCFCD_PDSIRRA-GCFCDTAL30_PDSIRRA-GCFCDTAG30_"
    "PDSIRRA-TRICD_PDSIRRA-TRICDTAL30_PDSIRRA-TRICDTAG30.csv"
)

CORP_REPO_2022_UB_URL = (
    "https://markets.newyorkfed.org/api/pd/get/SBN2022/timeseries/"
    "PDSORA-UBSCD_PDSORA-UBSCDTAL30_PDSORA-UBSCDTAG30_"
    "PDSORA-UBGCD_PDSORA-UBGCDTAL30_PDSORA-UBGCDTAG30.csv"
)

CORP_REPO_2022_CB_URL = (
    "https://markets.newyorkfed.org/api/pd/get/SBN2022/timeseries/"
    "PDSORA-CBSCD_PDSORA-CBSCDTAL30_PDSORA-CBSCDTAG30_"
    "PDSORA-CBGCD_PDSORA-CBGCDTAL30_PDSORA-CBGCDTAG30_"
    "PDSORA-CBSPCD_PDSORA-CBSPCDTAL30_PDSORA-CBSPCDTAG30.csv"
)

CORP_REPO_2022_GCF_TRI_URL = (
    "https://markets.newyorkfed.org/api/pd/get/SBN2022/timeseries/"
    "PDSORA-GCFCD_PDSORA-GCFCDTAL30_PDSORA-GCFCDTAG30_"
    "PDSORA-TRICD_PDSORA-TRICDTAL30_PDSORA-TRICDTAG30.csv"
)

CORP_FAILS_2001_URL = (
    "https://markets.newyorkfed.org/api/pd/get/SBP2013/timeseries/"
    "PDFASCFRA_PDFASCFDA.csv"
)

CORP_FAILS_2013_URL = (
    "https://markets.newyorkfed.org/api/pd/get/SBN2013/timeseries/"
    "PDFTR-CS_PDFTD-CS.csv"
)

CORP_FAILS_2015_URL = (
    "https://markets.newyorkfed.org/api/pd/get/SBN2015/timeseries/"
    "PDFTR-CS_PDFTD-CS.csv"
)

CORP_FAILS_2022_URL = (
    "https://markets.newyorkfed.org/api/pd/get/SBN2022/timeseries/"
    "PDFTR-CS_PDFTD-CS.csv"
)

CORP_FAILS_2024_URL = (
    "https://markets.newyorkfed.org/api/pd/get/SBN2024/timeseries/"
    "PDFTR-CS_PDFTD-CS.csv"
)

response.raise_for_status()

data = pd.read_csv(
    StringIO(response.text)
)

print()
print("Download complete.")
print(f"Rows: {len(data):,}")

print()
print("Columns:")
print(data.columns.tolist())

print()
print("First five rows:")
print(data.head())

print()
print("Last five rows:")
print(data.tail())

# ------------------------------------------------------------
# 2015–2021 HY dealer positions by maturity
# ------------------------------------------------------------

print()
print("=" * 60)
print("NY FED HY DEALER POSITIONS — 2015–2021")
print("=" * 60)

response_2015 = requests.get(
    HY_NET_POSITION_2015_URL,
    timeout=30,
)

response_2015.raise_for_status()

hy_2015 = pd.read_csv(
    StringIO(response_2015.text)
)

print()
print(f"Rows: {len(hy_2015):,}")

print()
print("Columns:")
print(hy_2015.columns.tolist())

print()
print("Series IDs:")
print(hy_2015["Time Series"].value_counts())

print()
print("First five rows:")
print(hy_2015.head())

print()
print("Last five rows:")
print(hy_2015.tail())

# ------------------------------------------------------------
# Reconstruct total HY dealer net position — 2015–2021
# ------------------------------------------------------------

hy_2015["As Of Date"] = pd.to_datetime(
    hy_2015["As Of Date"]
)

hy_2015["Value (millions)"] = pd.to_numeric(
    hy_2015["Value (millions)"],
    errors="coerce",
)

expected_series = {
    "PDPOSCSBND-BELL13",
    "PDPOSCSBND-BELG13",
    "PDPOSCSBND-BELG5L10",
    "PDPOSCSBND-BELG10",
}

actual_series = set(
    hy_2015["Time Series"].unique()
)

print()
print("Expected series present:")
print(actual_series == expected_series)

series_per_date = (
    hy_2015
    .groupby("As Of Date")["Time Series"]
    .nunique()
)

print()
print("Number of dates with fewer than four maturity buckets:")
print((series_per_date < 4).sum())

hy_2015_total = (
    hy_2015
    .groupby(
        "As Of Date",
        as_index=False,
    )["Value (millions)"]
    .sum()
    .rename(
        columns={
            "Value (millions)":
            "HY_DEALER_NET_POSITION_MILLIONS"
        }
    )
)

print()
print("Reconstructed HY total:")
print(f"Rows: {len(hy_2015_total):,}")
print(f"First date: {hy_2015_total['As Of Date'].min().date()}")
print(f"Last date: {hy_2015_total['As Of Date'].max().date()}")

print()
print("First five reconstructed observations:")
print(hy_2015_total.head())

print()
print("Last five reconstructed observations:")
print(hy_2015_total.tail())

# ------------------------------------------------------------
# 2014–2015 reporting-boundary diagnostic
# ------------------------------------------------------------

hy_old = data.copy()

hy_old["As Of Date"] = pd.to_datetime(
    hy_old["As Of Date"]
)

hy_old = (
    hy_old[
        ["As Of Date", "Value (millions)"]
    ]
    .rename(
        columns={
            "Value (millions)":
            "HY_DEALER_NET_POSITION_MILLIONS"
        }
    )
)

print()
print("=" * 60)
print("HY POSITION REPORTING BOUNDARY — 2014 / 2015")
print("=" * 60)

print()
print("Last 8 observations — old reporting regime:")
print(
    hy_old.tail(8).to_string(index=False)
)

print()
print("First 8 observations — reconstructed 2015 regime:")
print(
    hy_2015_total.head(8).to_string(index=False)
)

# ------------------------------------------------------------
# 2022–2024 HY dealer positions by maturity
# ------------------------------------------------------------

print()
print("=" * 60)
print("NY FED HY DEALER POSITIONS — 2022–2024")
print("=" * 60)

response_2022 = requests.get(
    HY_NET_POSITION_2022_URL,
    timeout=30,
)

response_2022.raise_for_status()

hy_2022 = pd.read_csv(
    StringIO(response_2022.text)
)

hy_2022["As Of Date"] = pd.to_datetime(
    hy_2022["As Of Date"]
)

hy_2022["Value (millions)"] = pd.to_numeric(
    hy_2022["Value (millions)"],
    errors="coerce",
)

print()
print("Series counts:")
print(hy_2022["Time Series"].value_counts())

series_per_date_2022 = (
    hy_2022
    .groupby("As Of Date")["Time Series"]
    .nunique()
)

print()
print("Dates with fewer than four maturity buckets:")
print((series_per_date_2022 < 4).sum())

hy_2022_total = (
    hy_2022
    .groupby(
        "As Of Date",
        as_index=False,
    )["Value (millions)"]
    .sum()
    .rename(
        columns={
            "Value (millions)":
            "HY_DEALER_NET_POSITION_MILLIONS"
        }
    )
)

print()
print("Reconstructed HY total:")
print(f"Rows: {len(hy_2022_total):,}")
print(f"First date: {hy_2022_total['As Of Date'].min().date()}")
print(f"Last date: {hy_2022_total['As Of Date'].max().date()}")

print()
print("First five:")
print(hy_2022_total.head())

print()
print("Last five:")
print(hy_2022_total.tail())

# ------------------------------------------------------------
# July 2024 onward — HY dealer positions by maturity
# ------------------------------------------------------------

print()
print("=" * 60)
print("NY FED HY DEALER POSITIONS — JULY 2024 ONWARD")
print("=" * 60)

response_2024 = requests.get(
    HY_NET_POSITION_2024_URL,
    timeout=30,
)

response_2024.raise_for_status()

hy_2024 = pd.read_csv(
    StringIO(response_2024.text)
)

hy_2024["As Of Date"] = pd.to_datetime(
    hy_2024["As Of Date"]
)

hy_2024["Value (millions)"] = pd.to_numeric(
    hy_2024["Value (millions)"],
    errors="coerce",
)

print()
print("Series counts:")
print(hy_2024["Time Series"].value_counts())

series_per_date_2024 = (
    hy_2024
    .groupby("As Of Date")["Time Series"]
    .nunique()
)

print()
print("Dates with fewer than four maturity buckets:")
print((series_per_date_2024 < 4).sum())

hy_2024_total = (
    hy_2024
    .groupby(
        "As Of Date",
        as_index=False,
    )["Value (millions)"]
    .sum()
    .rename(
        columns={
            "Value (millions)":
            "HY_DEALER_NET_POSITION_MILLIONS"
        }
    )
)

print()
print("Reconstructed HY total:")
print(f"Rows: {len(hy_2024_total):,}")
print(f"First date: {hy_2024_total['As Of Date'].min().date()}")
print(f"Last date: {hy_2024_total['As Of Date'].max().date()}")

print()
print("First five:")
print(hy_2024_total.head())

print()
print("Last five:")
print(hy_2024_total.tail())

# ------------------------------------------------------------
# 2013–2014 corporate repo financing
# ------------------------------------------------------------

print()
print("=" * 60)
print("NY FED CORPORATE REPO FINANCING — 2013–2014")
print("=" * 60)

for label, url in {
    "REVERSE_REPO": CORP_REVERSE_REPO_2013_URL,
    "REPO": CORP_REPO_2013_URL,
}.items():

    response = requests.get(
        url,
        timeout=30,
    )

    response.raise_for_status()

    financing = pd.read_csv(
        StringIO(response.text)
    )

    print()
    print(label)
    print("-" * 40)

    print("Rows:")
    print(len(financing))

    print()
    print("Series counts:")
    print(
        financing["Time Series"]
        .value_counts()
    )

    print()
    print("First six rows:")
    print(financing.head(6))

    print()
    print("Last six rows:")
    print(financing.tail(6))

    # ------------------------------------------------------------
# Extract 2013–2014 corporate repo as-of-date series
# ------------------------------------------------------------

def get_as_of_date_series(url, series_id, column_name):

    response = requests.get(
        url,
        timeout=30,
    )
    response.raise_for_status()

    df = pd.read_csv(
        StringIO(response.text)
    )

    df = df[
        df["Time Series"] == series_id
    ].copy()

    df["As Of Date"] = pd.to_datetime(
        df["As Of Date"]
    )

    df["Value (millions)"] = pd.to_numeric(
        df["Value (millions)"],
        errors="coerce",
    )

    df = (
        df[
            ["As Of Date", "Value (millions)"]
        ]
        .rename(
            columns={
                "Value (millions)": column_name
            }
        )
        .sort_values("As Of Date")
        .reset_index(drop=True)
    )

    return df


reverse_repo_2013 = get_as_of_date_series(
    CORP_REVERSE_REPO_2013_URL,
    "PDSIRRA-CD",
    "CORP_REVERSE_REPO_MILLIONS",
)

repo_2013 = get_as_of_date_series(
    CORP_REPO_2013_URL,
    "PDSORA-CD",
    "CORP_REPO_MILLIONS",
)


corp_repo_2013 = repo_2013.merge(
    reverse_repo_2013,
    on="As Of Date",
    how="inner",
)

corp_repo_2013["GROSS_CORP_REPO_MILLIONS"] = (
    corp_repo_2013["CORP_REPO_MILLIONS"]
    + corp_repo_2013["CORP_REVERSE_REPO_MILLIONS"]
)

corp_repo_2013["NET_CORP_REPO_BORROWING_MILLIONS"] = (
    corp_repo_2013["CORP_REPO_MILLIONS"]
    - corp_repo_2013["CORP_REVERSE_REPO_MILLIONS"]
)

print()
print("=" * 60)
print("CORPORATE REPO FINANCING — 2013–2014")
print("=" * 60)

print(corp_repo_2013.head())

print()
print(corp_repo_2013.tail())

print()
print("Missing values:")
print(corp_repo_2013.isna().sum())

reverse_repo_2015 = get_as_of_date_series(
    CORP_REVERSE_REPO_2015_URL,
    "PDSIRRA-CD",
    "CORP_REVERSE_REPO_MILLIONS",
)

repo_2015 = get_as_of_date_series(
    CORP_REPO_2015_URL,
    "PDSORA-CD",
    "CORP_REPO_MILLIONS",
)

corp_repo_2015 = repo_2015.merge(
    reverse_repo_2015,
    on="As Of Date",
    how="inner",
)

corp_repo_2015["GROSS_CORP_REPO_MILLIONS"] = (
    corp_repo_2015["CORP_REPO_MILLIONS"]
    + corp_repo_2015["CORP_REVERSE_REPO_MILLIONS"]
)

corp_repo_2015["NET_CORP_REPO_BORROWING_MILLIONS"] = (
    corp_repo_2015["CORP_REPO_MILLIONS"]
    - corp_repo_2015["CORP_REVERSE_REPO_MILLIONS"]
)

print()
print("=" * 60)
print("CORPORATE REPO FINANCING — 2015–2021")
print("=" * 60)

print(f"Rows: {len(corp_repo_2015):,}")
print(f"First date: {corp_repo_2015['As Of Date'].min().date()}")
print(f"Last date: {corp_repo_2015['As Of Date'].max().date()}")

print()
print("First five:")
print(corp_repo_2015.head())

print()
print("Last five:")
print(corp_repo_2015.tail())

print()
print("Missing values:")
print(corp_repo_2015.isna().sum())

print()
print("=" * 60)
print("CORPORATE REPO REPORTING BOUNDARY — 2014 / 2015")
print("=" * 60)

print()
print("Last 8 observations — 2013 reporting regime:")
print(
    corp_repo_2013.tail(8).to_string(index=False)
)

print()
print("First 8 observations — 2015 reporting regime:")
print(
    corp_repo_2015.head(8).to_string(index=False)
)

# ------------------------------------------------------------
# 2022–June 2024 corporate repo financing — API inspection
# ------------------------------------------------------------

print()
print("=" * 60)
print("NY FED CORPORATE REPO FINANCING — 2022 API INSPECTION")
print("=" * 60)

financing_2022_urls = {
    "REVERSE REPO — UNCLEARED BILATERAL":
        CORP_REVERSE_REPO_2022_UB_URL,

    "REVERSE REPO — CLEARED BILATERAL":
        CORP_REVERSE_REPO_2022_CB_URL,

    "REVERSE REPO — GCF & TRI-PARTY":
        CORP_REVERSE_REPO_2022_GCF_TRI_URL,

    "REPO — UNCLEARED BILATERAL":
        CORP_REPO_2022_UB_URL,

    "REPO — CLEARED BILATERAL":
        CORP_REPO_2022_CB_URL,

    "REPO — GCF & TRI-PARTY":
        CORP_REPO_2022_GCF_TRI_URL,
}

for label, url in financing_2022_urls.items():

    response = requests.get(
        url,
        timeout=30,
    )
    response.raise_for_status()

    df = pd.read_csv(
        StringIO(response.text)
    )

    df["As Of Date"] = pd.to_datetime(
        df["As Of Date"]
    )

    print()
    print(label)
    print("-" * 60)

    print(f"Rows: {len(df):,}")

    print(
        f"Date range: "
        f"{df['As Of Date'].min().date()} "
        f"to {df['As Of Date'].max().date()}"
    )

    print("Series IDs:")
    print(df["Time Series"].value_counts().sort_index())

    # ------------------------------------------------------------
# 2022 corporate repo financing — component completeness check
# ------------------------------------------------------------

print()
print("=" * 60)
print("2022 CORPORATE REPO — COMPONENT COMPLETENESS CHECK")
print("=" * 60)

for label, url in financing_2022_urls.items():

    response = requests.get(
        url,
        timeout=30,
    )
    response.raise_for_status()

    df = pd.read_csv(
        StringIO(response.text)
    )

    df["As Of Date"] = pd.to_datetime(
        df["As Of Date"]
    )

    df["Value (millions)"] = pd.to_numeric(
        df["Value (millions)"],
        errors="coerce",
    )

    # Number of distinct component series in this endpoint
    expected_components = df["Time Series"].nunique()

    # Check duplicate series/date observations
    duplicate_series_dates = (
        df.duplicated(
            subset=["As Of Date", "Time Series"],
            keep=False,
        )
        .sum()
    )

    # Check number of components present on every date
    components_per_date = (
        df
        .groupby("As Of Date")["Time Series"]
        .nunique()
    )

    incomplete_dates = (
        components_per_date != expected_components
    ).sum()

    # Check values that could not be parsed numerically
    missing_values = df["Value (millions)"].isna().sum()

    print()
    print(label)
    print("-" * 60)

    print(f"Expected components per date: {expected_components}")
    print(f"Dates: {df['As Of Date'].nunique()}")
    print(f"Duplicate series/date rows: {duplicate_series_dates}")
    print(f"Dates with incomplete component sets: {incomplete_dates}")
    print(f"Missing/non-numeric values: {missing_values}")

    # ------------------------------------------------------------
# 2022 corporate repo financing — inspect non-numeric values
# ------------------------------------------------------------

print()
print("=" * 60)
print("2022 CORPORATE REPO — NON-NUMERIC VALUE DIAGNOSTIC")
print("=" * 60)

for label, url in financing_2022_urls.items():

    response = requests.get(
        url,
        timeout=30,
    )
    response.raise_for_status()

    df = pd.read_csv(
        StringIO(response.text),
        dtype={"Value (millions)": str},
    )

    df["As Of Date"] = pd.to_datetime(
        df["As Of Date"]
    )

    numeric_values = pd.to_numeric(
        df["Value (millions)"],
        errors="coerce",
    )

    bad = df[
        numeric_values.isna()
    ].copy()

    print()
    print(label)
    print("-" * 60)

    print(f"Non-numeric rows: {len(bad)}")

    if len(bad) > 0:

        print()
        print("Raw non-numeric values:")
        print(
            bad["Value (millions)"]
            .value_counts(dropna=False)
        )

        print()
        print("Non-numeric rows by series:")
        print(
            bad["Time Series"]
            .value_counts()
            .sort_index()
        )

        print()
        print("First 20 affected rows:")
        print(
            bad[
                [
                    "As Of Date",
                    "Time Series",
                    "Value (millions)",
                ]
            ]
            .head(20)
            .to_string(index=False)
        )

# ------------------------------------------------------------
# 2022 corporate repo — fully observable dates
# ------------------------------------------------------------

print()
print("=" * 60)
print("2022 CORPORATE REPO — FULL OBSERVABILITY BY DATE")
print("=" * 60)

all_frames = []

for label, url in financing_2022_urls.items():

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    df = pd.read_csv(
        StringIO(response.text),
        dtype={"Value (millions)": str},
    )

    df["As Of Date"] = pd.to_datetime(df["As Of Date"])

    df["Numeric Value"] = pd.to_numeric(
        df["Value (millions)"],
        errors="coerce",
    )

    df["Group"] = label

    all_frames.append(
        df[
            [
                "As Of Date",
                "Time Series",
                "Value (millions)",
                "Numeric Value",
                "Group",
            ]
        ]
    )

all_2022_components = pd.concat(
    all_frames,
    ignore_index=True,
)

observability = (
    all_2022_components
    .groupby("As Of Date")
    .agg(
        TOTAL_COMPONENTS=("Time Series", "count"),
        OBSERVED_COMPONENTS=("Numeric Value", "count"),
    )
)

observability["SUPPRESSED_COMPONENTS"] = (
    observability["TOTAL_COMPONENTS"]
    - observability["OBSERVED_COMPONENTS"]
)

fully_observed = observability[
    observability["SUPPRESSED_COMPONENTS"] == 0
]

print()
print("Suppressed components per date:")
print(
    observability["SUPPRESSED_COMPONENTS"]
    .value_counts()
    .sort_index()
)

print()
print(
    f"Fully observable dates: "
    f"{len(fully_observed)} / {len(observability)}"
)

if len(fully_observed) > 0:
    print()
    print("Fully observable dates:")
    print(fully_observed)

    # ------------------------------------------------------------
# PROVENANCE DECISION — 2022 CORPORATE REPO FINANCING
# ------------------------------------------------------------
#
# The Jan 2022–Jun 2024 NY Fed corporate repo/reverse-repo
# reporting regime decomposes financing into 21 components
# per side (Uncleared Bilateral, Cleared Bilateral, and
# GCF/Tri-Party).
#
# API validation found:
#   - 130 weekly dates
#   - complete structural coverage of requested series IDs
#   - no duplicate series/date observations
#   - disclosure-suppressed values represented by "*"
#   - between 2 and 7 suppressed components on EVERY date
#   - 0 / 130 dates with complete numeric observability
#
# Therefore an exact bottom-up corporate repo or reverse-repo
# total cannot be reconstructed from the publicly disclosed
# 2022-regime component data without imposing assumptions on
# suppressed observations.
#
# DECISION:
#   Do NOT treat "*" as zero.
#   Do NOT impute suppressed observations at this stage.
#   Do NOT splice a reconstructed 2022 series to the
#   2015–2021 aggregate series.
#
# The 2022 reporting regime remains a documented provenance
# boundary requiring a different measurement strategy if
# post-2021 corporate financing is used in subsequent analysis.

# July 2024 onward:
# Manual inspection of the NY Fed Jul 2024+ reporting regime
# confirms that corporate repo/reverse-repo financing remains
# decomposed into:
#   - Uncleared Bilateral
#   - Cleared Bilateral
#   - GCF & Tri-Party
#
# Disclosure suppression ("*") persists in the published tables.
# For example, General Overnight & Continuing observations within
# Uncleared Bilateral are suppressed while corresponding Specified
# observations are reported numerically.
#
# Because at least one required component of the total is
# disclosure-suppressed, an exact aggregate corporate repo financing
# series cannot be reconstructed from the public component data.
#
# DECISION:
#   Do not construct a Jul 2024+ exact corporate repo/reverse-repo total.
#   Do not replace "*" with zero.
#   Do not impute suppressed values.
#   Do not splice this regime to the pre-2022 aggregate series.

# ------------------------------------------------------------
# Corporate securities fails — reporting-regime inspection
# ------------------------------------------------------------

print()
print("=" * 60)
print("NY FED CORPORATE SECURITIES FAILS — REGIME INSPECTION")
print("=" * 60)

corp_fails_urls = {
    "2001–2013": CORP_FAILS_2001_URL,
    "2013–2014": CORP_FAILS_2013_URL,
    "2015–2021": CORP_FAILS_2015_URL,
    "2022–JUN 2024": CORP_FAILS_2022_URL,
    "JUL 2024+": CORP_FAILS_2024_URL,
}

for regime, url in corp_fails_urls.items():

    response = requests.get(
        url,
        timeout=30,
    )
    response.raise_for_status()

    df = pd.read_csv(
        StringIO(response.text),
        dtype={"Value (millions)": str},
    )

    df["As Of Date"] = pd.to_datetime(
        df["As Of Date"]
    )

    numeric_values = pd.to_numeric(
        df["Value (millions)"],
        errors="coerce",
    )

    print()
    print(regime)
    print("-" * 60)

    print(f"Rows: {len(df):,}")
    print(f"Unique dates: {df['As Of Date'].nunique():,}")

    print(
        f"Date range: "
        f"{df['As Of Date'].min().date()} "
        f"to {df['As Of Date'].max().date()}"
    )

    print()
    print("Series IDs:")
    print(
        df["Time Series"]
        .value_counts()
        .sort_index()
    )

    duplicates = df.duplicated(
        subset=["As Of Date", "Time Series"],
        keep=False,
    ).sum()

    print()
    print(f"Duplicate series/date rows: {duplicates}")

    series_per_date = (
        df
        .groupby("As Of Date")["Time Series"]
        .nunique()
    )

    expected_series_count = df["Time Series"].nunique()

    incomplete_dates = (
        series_per_date != expected_series_count
    ).sum()

    print(
        f"Dates with fewer than "
        f"{expected_series_count} series: "
        f"{incomplete_dates}"
    )

    non_numeric = df[
        numeric_values.isna()
    ].copy()

    print(f"Non-numeric values: {len(non_numeric)}")

    if len(non_numeric) > 0:

        print()
        print("Raw non-numeric values:")
        print(
            non_numeric["Value (millions)"]
            .value_counts(dropna=False)
        )

        print()
        print("Affected series:")
        print(
            non_numeric["Time Series"]
            .value_counts()
            .sort_index()
        )

    print()
    print("First four rows:")
    print(
        df[
            ["As Of Date", "Time Series", "Value (millions)"]
        ]
        .head(4)
        .to_string(index=False)
    )

    print()
    print("Last four rows:")
    print(
        df[
            ["As Of Date", "Time Series", "Value (millions)"]
        ]
        .tail(4)
        .to_string(index=False)
    )

    # ------------------------------------------------------------
# Corporate securities fails — 2013 reporting-boundary check
# ------------------------------------------------------------

print()
print("=" * 60)
print("CORPORATE FAILS REPORTING BOUNDARY — 2013")
print("=" * 60)

for regime, url in {
    "PRE-APRIL 2013": CORP_FAILS_2001_URL,
    "APRIL 2013+": CORP_FAILS_2013_URL,
}.items():

    response = requests.get(
        url,
        timeout=30,
    )
    response.raise_for_status()

    df = pd.read_csv(
        StringIO(response.text)
    )

    df["As Of Date"] = pd.to_datetime(
        df["As Of Date"]
    )

    df["Value (millions)"] = pd.to_numeric(
        df["Value (millions)"],
        errors="coerce",
    )

    wide = (
        df
        .pivot(
            index="As Of Date",
            columns="Time Series",
            values="Value (millions)",
        )
        .sort_index()
    )

    print()
    print(regime)
    print("-" * 60)

    if regime == "PRE-APRIL 2013":
        print(wide.tail(8).to_string())
    else:
        print(wide.head(8).to_string())

        # ------------------------------------------------------------
# Corporate securities fails — standardized historical series
# ------------------------------------------------------------

def get_corporate_fails(
    url,
    receive_id,
    deliver_id,
    regime,
):

    response = requests.get(
        url,
        timeout=30,
    )
    response.raise_for_status()

    df = pd.read_csv(
        StringIO(response.text)
    )

    df["As Of Date"] = pd.to_datetime(
        df["As Of Date"]
    )

    df["Value (millions)"] = pd.to_numeric(
        df["Value (millions)"],
        errors="coerce",
    )

    # Explicit economic mapping of NY Fed series IDs
    mapping = {
        receive_id: "CORP_FAILS_TO_RECEIVE_MILLIONS",
        deliver_id: "CORP_FAILS_TO_DELIVER_MILLIONS",
    }

    df["Measure"] = df["Time Series"].map(mapping)

    if df["Measure"].isna().any():
        raise ValueError(
            f"Unexpected series ID in {regime}"
        )

    wide = (
        df
        .pivot(
            index="As Of Date",
            columns="Measure",
            values="Value (millions)",
        )
        .reset_index()
    )

    wide.columns.name = None

    wide["REPORTING_REGIME"] = regime

    return wide


fails_2001 = get_corporate_fails(
    CORP_FAILS_2001_URL,
    receive_id="PDFASCFRA",
    deliver_id="PDFASCFDA",
    regime="2001-07_to_2013-03",
)

fails_2013 = get_corporate_fails(
    CORP_FAILS_2013_URL,
    receive_id="PDFTR-CS",
    deliver_id="PDFTD-CS",
    regime="2013-04_to_2014-12",
)

fails_2015 = get_corporate_fails(
    CORP_FAILS_2015_URL,
    receive_id="PDFTR-CS",
    deliver_id="PDFTD-CS",
    regime="2015-01_to_2021-12",
)

fails_2022 = get_corporate_fails(
    CORP_FAILS_2022_URL,
    receive_id="PDFTR-CS",
    deliver_id="PDFTD-CS",
    regime="2022-01_to_2024-06",
)

fails_2024 = get_corporate_fails(
    CORP_FAILS_2024_URL,
    receive_id="PDFTR-CS",
    deliver_id="PDFTD-CS",
    regime="2024-07_onward",
)


corp_fails = pd.concat(
    [
        fails_2001,
        fails_2013,
        fails_2015,
        fails_2022,
        fails_2024,
    ],
    ignore_index=True,
)

corp_fails = (
    corp_fails
    .sort_values("As Of Date")
    .reset_index(drop=True)
)


# ------------------------------------------------------------
# Final continuity validation
# ------------------------------------------------------------

print()
print("=" * 60)
print("CORPORATE SECURITIES FAILS — STANDARDIZED SERIES")
print("=" * 60)

print(f"Rows: {len(corp_fails):,}")
print(
    f"Date range: "
    f"{corp_fails['As Of Date'].min().date()} "
    f"to {corp_fails['As Of Date'].max().date()}"
)

print()
print("Missing values:")
print(
    corp_fails[
        [
            "CORP_FAILS_TO_RECEIVE_MILLIONS",
            "CORP_FAILS_TO_DELIVER_MILLIONS",
        ]
    ].isna().sum()
)

print()
print("Duplicate dates:")
print(
    corp_fails["As Of Date"]
    .duplicated()
    .sum()
)

print()
print("Observations by reporting regime:")
print(
    corp_fails["REPORTING_REGIME"]
    .value_counts(sort=False)
)

print()
print("First five:")
print(corp_fails.head().to_string(index=False))

print()
print("Last five:")
print(corp_fails.tail().to_string(index=False))

# ------------------------------------------------------------
# Corporate securities fails — relationship diagnostic
# ------------------------------------------------------------

print()
print("=" * 60)
print("CORPORATE SECURITIES FAILS — RECEIVE / DELIVER RELATIONSHIP")
print("=" * 60)

fails_corr = (
    corp_fails[
        [
            "CORP_FAILS_TO_RECEIVE_MILLIONS",
            "CORP_FAILS_TO_DELIVER_MILLIONS",
        ]
    ]
    .corr()
    .iloc[0, 1]
)

print()
print(f"Level correlation: {fails_corr:.4f}")

corp_fails["FAILS_GAP_MILLIONS"] = (
    corp_fails["CORP_FAILS_TO_DELIVER_MILLIONS"]
    - corp_fails["CORP_FAILS_TO_RECEIVE_MILLIONS"]
)

corp_fails["FAILS_DELIVER_RECEIVE_RATIO"] = (
    corp_fails["CORP_FAILS_TO_DELIVER_MILLIONS"]
    / corp_fails["CORP_FAILS_TO_RECEIVE_MILLIONS"]
)

print()
print("Fails gap summary:")
print(
    corp_fails["FAILS_GAP_MILLIONS"]
    .describe()
)

print()
print("Deliver / Receive ratio summary:")
print(
    corp_fails["FAILS_DELIVER_RECEIVE_RATIO"]
    .replace([float("inf"), -float("inf")], pd.NA)
    .describe()
)

print()
print("Largest absolute gaps:")
print(
    corp_fails.assign(
        ABS_FAILS_GAP_MILLIONS=
        corp_fails["FAILS_GAP_MILLIONS"].abs()
    )
    .nlargest(
        10,
        "ABS_FAILS_GAP_MILLIONS"
    )[
        [
            "As Of Date",
            "CORP_FAILS_TO_RECEIVE_MILLIONS",
            "CORP_FAILS_TO_DELIVER_MILLIONS",
            "FAILS_GAP_MILLIONS",
            "REPORTING_REGIME",
        ]
    ]
    .to_string(index=False)
)

# ------------------------------------------------------------
# Corporate securities fails — change relationship
# ------------------------------------------------------------

corp_fails["D_FAILS_RECEIVE"] = (
    corp_fails["CORP_FAILS_TO_RECEIVE_MILLIONS"].diff()
)

corp_fails["D_FAILS_DELIVER"] = (
    corp_fails["CORP_FAILS_TO_DELIVER_MILLIONS"].diff()
)

change_corr = (
    corp_fails[
        [
            "D_FAILS_RECEIVE",
            "D_FAILS_DELIVER",
        ]
    ]
    .corr()
    .iloc[0, 1]
)

print()
print("=" * 60)
print("CORPORATE SECURITIES FAILS — WEEKLY CHANGE RELATIONSHIP")
print("=" * 60)

print()
print(f"Change correlation: {change_corr:.4f}")

print()
print("Weekly change summary:")
print(
    corp_fails[
        [
            "D_FAILS_RECEIVE",
            "D_FAILS_DELIVER",
        ]
    ]
    .describe()
)

# ------------------------------------------------------------
# Corporate fails — monthly aggregation
# Primary measure: mean weekly Fails to Deliver
# ------------------------------------------------------------

corp_fails_monthly = (
    corp_fails
    .set_index("As Of Date")
    ["CORP_FAILS_TO_DELIVER_MILLIONS"]
    .resample("ME")
    .agg(
        MONTHLY_MEAN_FAILS_TO_DELIVER_MILLIONS="mean",
        WEEKS_IN_MONTH="count",
    )
    .reset_index()
)

print()
print("=" * 60)
print("CORPORATE FAILS - MONTHLY FAILS TO DELIVER")
print("=" * 60)

print()
print(f"Months: {len(corp_fails_monthly):,}")

print(
    f"Date range: "
    f"{corp_fails_monthly['As Of Date'].min().date()} "
    f"to {corp_fails_monthly['As Of Date'].max().date()}"
)

print()
print("Weeks per month:")
print(
    corp_fails_monthly["WEEKS_IN_MONTH"]
    .value_counts()
    .sort_index()
)

print()
print("Missing monthly means:")
print(
    corp_fails_monthly[
        "MONTHLY_MEAN_FAILS_TO_DELIVER_MILLIONS"
    ].isna().sum()
)

print()
print("Summary:")
print(
    corp_fails_monthly[
        "MONTHLY_MEAN_FAILS_TO_DELIVER_MILLIONS"
    ].describe()
)

print()
print("First five:")
print(corp_fails_monthly.head().to_string(index=False))

print()
print("Last five:")
print(corp_fails_monthly.tail().to_string(index=False))

# Exclude incomplete current month
corp_fails_monthly_complete = (
    corp_fails_monthly[
        corp_fails_monthly["WEEKS_IN_MONTH"] >= 4
    ]
    .copy()
)

output_path = (
    RAW_DIR / "nyfed_corporate_fails_monthly.csv"
)

corp_fails_monthly_complete.to_csv(
    output_path,
    index=False,
)

print()
print(f"Saved: {output_path}")
print(
    f"Complete months saved: "
    f"{len(corp_fails_monthly_complete):,}"
)