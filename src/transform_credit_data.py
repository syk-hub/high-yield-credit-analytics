"""Transform raw FRED snapshots into daily and monthly analytical tables."""

from pathlib import Path

import numpy as np
import pandas as pd


# ---------------------------------------------------------
# 1. Define project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


# ---------------------------------------------------------
# 2. Define the FRED series used by the project
# ---------------------------------------------------------

SERIES_DICTIONARY = {
    "HY_OAS_PERCENT": "BAMLH0A0HYM2",
    "HY_EFFECTIVE_YIELD": "BAMLH0A0HYM2EY",
    "HY_TOTAL_RETURN_INDEX": "BAMLHYH0A0HYM2TRIV",
    "TREASURY_10Y": "DGS10",
    "EFFR": "EFFR",
    "VIX": "VIXCLS",
    "UNEMPLOYMENT_RATE": "UNRATE",
    "RECESSION_FLAG": "USREC",
}


DAILY_SERIES = [
    "HY_OAS_PERCENT",
    "HY_EFFECTIVE_YIELD",
    "HY_TOTAL_RETURN_INDEX",
    "TREASURY_10Y",
    "EFFR",
    "VIX",
]


MONTHLY_SERIES = [
    "UNEMPLOYMENT_RATE",
    "RECESSION_FLAG",
]


# ---------------------------------------------------------
# 3. Find and read the latest raw snapshot for each series
# ---------------------------------------------------------

def load_latest_snapshot(
    series_name: str,
    fred_id: str,
) -> pd.DataFrame:
    """Load the most recently created raw CSV for one FRED series."""

    file_pattern = f"fred_{fred_id}_snapshot_*.csv"

    matching_files = sorted(
        RAW_DATA_DIR.glob(file_pattern)
    )

    if not matching_files:
        raise FileNotFoundError(
            f"No raw snapshot found for {series_name} "
            f"using pattern {file_pattern}"
        )

    latest_file = matching_files[-1]

    dataframe = pd.read_csv(latest_file)

    if "Date" not in dataframe.columns:
        raise ValueError(
            f"The Date column is missing from {latest_file.name}."
        )

    if series_name not in dataframe.columns:
        raise ValueError(
            f"The {series_name} column is missing "
            f"from {latest_file.name}."
        )

    dataframe["Date"] = pd.to_datetime(
        dataframe["Date"],
        errors="coerce",
    )

    dataframe[series_name] = pd.to_numeric(
        dataframe[series_name],
        errors="coerce",
    )

    dataframe = dataframe[
        ["Date", series_name]
    ].copy()

    dataframe = dataframe.dropna(
        subset=["Date"]
    )

    dataframe = dataframe.drop_duplicates(
        subset=["Date"],
        keep="last",
    )

    dataframe = dataframe.sort_values("Date")

    print(
        f"Loaded {series_name}: "
        f"{len(dataframe):,} rows from {latest_file.name}"
    )

    return dataframe


# ---------------------------------------------------------
# 4. Merge a collection of series on Date
# ---------------------------------------------------------

def merge_series(
    series_names: list[str],
) -> pd.DataFrame:
    """Outer-join multiple FRED series by date."""

    merged_dataframe = None

    for series_name in series_names:

        fred_id = SERIES_DICTIONARY[series_name]

        current_dataframe = load_latest_snapshot(
            series_name=series_name,
            fred_id=fred_id,
        )

        if merged_dataframe is None:
            merged_dataframe = current_dataframe
        else:
            merged_dataframe = merged_dataframe.merge(
                current_dataframe,
                on="Date",
                how="outer",
            )

    if merged_dataframe is None:
        raise ValueError("No series were available to merge.")

    merged_dataframe = merged_dataframe.sort_values(
        "Date"
    ).reset_index(drop=True)

    return merged_dataframe


# ---------------------------------------------------------
# 5. Credit-regime classification
# ---------------------------------------------------------

def classify_credit_regime(
    oas_value: float,
    percentile_25: float,
    percentile_75: float,
    percentile_95: float,
) -> str:
    """Classify the credit regime using historical OAS thresholds."""

    if pd.isna(oas_value):
        return np.nan

    if oas_value < percentile_25:
        return "Tight"

    if oas_value < percentile_75:
        return "Normal"

    if oas_value < percentile_95:
        return "Stressed"

    return "Severe Stress"


# ---------------------------------------------------------
# 6. Create the daily credit-market table
# ---------------------------------------------------------

def build_daily_table() -> pd.DataFrame:
    """Build the processed daily market table."""

    daily = merge_series(DAILY_SERIES)

    # OAS is reported by FRED in percentage points.
    # Multiplying by 100 converts it to basis points.
    daily["HY_OAS_BPS"] = (
        daily["HY_OAS_PERCENT"] * 100
    )

    # Approximate one and three trading months.
    daily["HY_OAS_1M_CHANGE_BPS"] = (
        daily["HY_OAS_BPS"]
        - daily["HY_OAS_BPS"].shift(21)
    )

    daily["HY_OAS_3M_CHANGE_BPS"] = (
        daily["HY_OAS_BPS"]
        - daily["HY_OAS_BPS"].shift(63)
    )

    # Percentile rank within the trailing 252 observations.
    daily["HY_OAS_ROLLING_252D_PERCENTILE"] = (
        daily["HY_OAS_BPS"]
        .rolling(window=252, min_periods=126)
        .rank(pct=True)
    )

    daily["VIX_20D_AVERAGE"] = (
        daily["VIX"]
        .rolling(window=20, min_periods=10)
        .mean()
    )

    # Total-return calculations.
    daily["HY_TOTAL_RETURN_1D"] = (
        daily["HY_TOTAL_RETURN_INDEX"]
        .pct_change(fill_method=None)
    )

    daily["HY_TOTAL_RETURN_1M"] = (
        daily["HY_TOTAL_RETURN_INDEX"]
        .pct_change(periods=21, fill_method=None)
    )

    running_peak = (
        daily["HY_TOTAL_RETURN_INDEX"]
        .cummax()
    )

    daily["HY_TOTAL_RETURN_DRAWDOWN"] = (
        daily["HY_TOTAL_RETURN_INDEX"]
        / running_peak
        - 1
    )

    # Full available-history thresholds.
    percentile_25 = daily["HY_OAS_BPS"].quantile(0.25)
    percentile_75 = daily["HY_OAS_BPS"].quantile(0.75)
    percentile_95 = daily["HY_OAS_BPS"].quantile(0.95)

    daily["CREDIT_REGIME"] = daily["HY_OAS_BPS"].apply(
        classify_credit_regime,
        args=(
            percentile_25,
            percentile_75,
            percentile_95,
        ),
    )

    daily["OAS_25TH_PERCENTILE_BPS"] = percentile_25
    daily["OAS_75TH_PERCENTILE_BPS"] = percentile_75
    daily["OAS_95TH_PERCENTILE_BPS"] = percentile_95

    return daily


# ---------------------------------------------------------
# 7. Create the monthly credit-macro table
# ---------------------------------------------------------

def build_monthly_table(
    daily: pd.DataFrame,
) -> pd.DataFrame:
    """Build a monthly table from market and macro data."""

    market = daily.set_index("Date")

    monthly_market = pd.DataFrame(
        {
            "HY_OAS_MONTH_END_BPS": (
                market["HY_OAS_BPS"].resample("ME").last()
            ),
            "HY_OAS_MONTHLY_AVERAGE_BPS": (
                market["HY_OAS_BPS"].resample("ME").mean()
            ),
            "EFFR_MONTH_END": (
                market["EFFR"].resample("ME").last()
            ),
            "VIX_MONTHLY_AVERAGE": (
                market["VIX"].resample("ME").mean()
            ),
            "HY_TOTAL_RETURN_INDEX_MONTH_END": (
                market["HY_TOTAL_RETURN_INDEX"]
                .resample("ME")
                .last()
            ),
        }
    )

    monthly_market["HY_OAS_MONTHLY_CHANGE_BPS"] = (
        monthly_market["HY_OAS_MONTH_END_BPS"]
        .diff()
    )

    monthly_market["HY_TOTAL_RETURN_MONTHLY"] = (
        monthly_market["HY_TOTAL_RETURN_INDEX_MONTH_END"]
        .pct_change(fill_method=None)
    )

    monthly_macro = merge_series(
        MONTHLY_SERIES
    ).set_index("Date")

    monthly_macro = monthly_macro.resample("ME").last()

    monthly = monthly_market.join(
        monthly_macro,
        how="outer",
    )

    monthly["UNEMPLOYMENT_3M_CHANGE"] = (
        monthly["UNEMPLOYMENT_RATE"].diff(3)
    )

    monthly = monthly.reset_index()

    monthly = monthly.rename(
        columns={"Date": "MonthEnd"}
    )

    monthly["MonthStart"] = (
        monthly["MonthEnd"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    column_order = [
        "MonthStart",
        "MonthEnd",
        "HY_OAS_MONTH_END_BPS",
        "HY_OAS_MONTHLY_AVERAGE_BPS",
        "HY_OAS_MONTHLY_CHANGE_BPS",
        "UNEMPLOYMENT_RATE",
        "UNEMPLOYMENT_3M_CHANGE",
        "RECESSION_FLAG",
        "EFFR_MONTH_END",
        "VIX_MONTHLY_AVERAGE",
        "HY_TOTAL_RETURN_INDEX_MONTH_END",
        "HY_TOTAL_RETURN_MONTHLY",
    ]

    monthly = monthly[column_order]

    return monthly


# ---------------------------------------------------------
# 8. Run the transformation process
# ---------------------------------------------------------

def main() -> None:
    """Create and export the processed analytical tables."""

    PROCESSED_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print()
    print("Building daily credit-market table...")

    daily = build_daily_table()

    daily_output_file = (
        PROCESSED_DATA_DIR
        / "credit_market_daily.csv"
    )

    daily.to_csv(
        daily_output_file,
        index=False,
    )

    print()
    print("Building monthly credit-macro table...")

    monthly = build_monthly_table(daily)

    monthly_output_file = (
        PROCESSED_DATA_DIR
        / "credit_macro_monthly.csv"
    )

    monthly.to_csv(
        monthly_output_file,
        index=False,
    )

    print()
    print("=" * 60)
    print("DATA TRANSFORMATION COMPLETE")
    print("=" * 60)
    print(f"Daily rows: {len(daily):,}")
    print(f"Monthly rows: {len(monthly):,}")
    print(f"Daily table: {daily_output_file}")
    print(f"Monthly table: {monthly_output_file}")


if __name__ == "__main__":
    main()