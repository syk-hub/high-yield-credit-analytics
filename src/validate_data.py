"""Validate processed credit-market datasets."""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

DAILY_FILE = PROCESSED_DATA_DIR / "credit_market_daily.csv"
MONTHLY_FILE = PROCESSED_DATA_DIR / "credit_macro_monthly.csv"


def validate_daily() -> None:
    """Run basic checks on the daily processed table."""

    daily = pd.read_csv(
        DAILY_FILE,
        parse_dates=["Date"],
    )

    print()
    print("DAILY TABLE VALIDATION")
    print("-" * 50)

    print(f"Rows: {len(daily):,}")
    print(f"Columns: {len(daily.columns):,}")
    print(f"First date: {daily['Date'].min().date()}")
    print(f"Last date: {daily['Date'].max().date()}")

    duplicate_dates = daily["Date"].duplicated().sum()
    print(f"Duplicate dates: {duplicate_dates:,}")

    missing_dates = daily["Date"].isna().sum()
    print(f"Missing dates: {missing_dates:,}")

    print()
    print("Missing values by column:")
    print(daily.isna().sum())

    print()
    print("HY OAS basis-point range:")
    print(daily["HY_OAS_BPS"].describe())

    invalid_oas = (daily["HY_OAS_BPS"] < 0).sum()
    print(f"Negative HY OAS values: {invalid_oas:,}")

    valid_regimes = {
        "Tight",
        "Normal",
        "Stressed",
        "Severe Stress",
    }

    observed_regimes = set(
        daily["CREDIT_REGIME"].dropna().unique()
    )

    invalid_regimes = observed_regimes - valid_regimes

    print(f"Observed regimes: {sorted(observed_regimes)}")
    print(f"Invalid regimes: {sorted(invalid_regimes)}")

    assert duplicate_dates == 0, "Daily table contains duplicate dates."
    assert missing_dates == 0, "Daily table contains missing dates."
    assert invalid_oas == 0, "Daily table contains negative OAS values."
    assert not invalid_regimes, "Daily table contains invalid regimes."

    print()
    print("Daily validation passed.")


def validate_monthly() -> None:
    """Run basic checks on the monthly processed table."""

    monthly = pd.read_csv(
        MONTHLY_FILE,
        parse_dates=["MonthStart", "MonthEnd"],
    )

    print()
    print("MONTHLY TABLE VALIDATION")
    print("-" * 50)

    print(f"Rows: {len(monthly):,}")
    print(f"Columns: {len(monthly.columns):,}")
    print(f"First month: {monthly['MonthStart'].min().date()}")
    print(f"Last month: {monthly['MonthStart'].max().date()}")

    duplicate_months = monthly["MonthStart"].duplicated().sum()
    print(f"Duplicate months: {duplicate_months:,}")

    missing_months = monthly["MonthStart"].isna().sum()
    print(f"Missing MonthStart values: {missing_months:,}")

    print()
    print("Missing values by column:")
    print(monthly.isna().sum())

    recession_values = set(
        monthly["RECESSION_FLAG"].dropna().unique()
    )

    invalid_recession_values = recession_values - {0, 1}

    print(f"Observed recession flags: {sorted(recession_values)}")
    print(
        "Invalid recession flags: "
        f"{sorted(invalid_recession_values)}"
    )

    assert duplicate_months == 0, (
        "Monthly table contains duplicate months."
    )

    assert missing_months == 0, (
        "Monthly table contains missing MonthStart values."
    )

    assert not invalid_recession_values, (
        "RECESSION_FLAG contains values other than 0 or 1."
    )

    print()
    print("Monthly validation passed.")


def main() -> None:
    """Run all validation checks."""

    if not DAILY_FILE.exists():
        raise FileNotFoundError(
            f"Missing processed file: {DAILY_FILE}"
        )

    if not MONTHLY_FILE.exists():
        raise FileNotFoundError(
            f"Missing processed file: {MONTHLY_FILE}"
        )

    validate_daily()
    validate_monthly()

    print()
    print("=" * 60)
    print("ALL DATA VALIDATION CHECKS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()