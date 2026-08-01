"""Download the Version 1 FRED series and save raw snapshots."""

from datetime import date
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from fredapi import Fred


# ---------------------------------------------------------
# 1. Define project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

ENV_FILE = PROJECT_ROOT / ".env"

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


# ---------------------------------------------------------
# 2. Define the FRED series required for Version 1
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


# ---------------------------------------------------------
# 3. Load the API key
# ---------------------------------------------------------

load_dotenv(ENV_FILE)

api_key = os.getenv("FRED_API_KEY")

if not api_key:
    raise ValueError(
        "FRED_API_KEY was not found. "
        "Check the .env file in the project folder."
    )


# ---------------------------------------------------------
# 4. Create the FRED connection
# ---------------------------------------------------------

fred = Fred(api_key=api_key)


# ---------------------------------------------------------
# 5. Create the raw-data folder
# ---------------------------------------------------------

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# 6. Download and save each series
# ---------------------------------------------------------

extraction_date = date.today().isoformat()

download_summary = []

for series_name, series_id in SERIES_DICTIONARY.items():

    print()
    print(f"Downloading {series_name} ({series_id})...")

    try:
        series = fred.get_series(series_id)

        if series.empty:
            raise ValueError(
                f"No observations were returned for {series_id}."
            )

        dataframe = series.rename(series_name).reset_index()

        dataframe.columns = [
            "Date",
            series_name,
        ]

        dataframe["Date"] = pd.to_datetime(
            dataframe["Date"]
        )

        dataframe[series_name] = pd.to_numeric(
            dataframe[series_name],
            errors="coerce",
        )

        output_file = (
            RAW_DATA_DIR
            / f"fred_{series_id}_snapshot_{extraction_date}.csv"
        )

        dataframe.to_csv(
            output_file,
            index=False,
        )

        summary_record = {
            "Series_Name": series_name,
            "FRED_ID": series_id,
            "Rows": len(dataframe),
            "First_Date": dataframe["Date"].min().date(),
            "Last_Date": dataframe["Date"].max().date(),
            "Missing_Values": dataframe[series_name].isna().sum(),
            "Status": "Success",
        }

        download_summary.append(summary_record)

        print("Download successful.")
        print(f"Rows: {len(dataframe):,}")
        print(
            f"First date: "
            f"{dataframe['Date'].min().date()}"
        )
        print(
            f"Last date: "
            f"{dataframe['Date'].max().date()}"
        )
        print(
            f"Missing values: "
            f"{dataframe[series_name].isna().sum():,}"
        )
        print(f"Saved to: {output_file}")

    except Exception as error:

        summary_record = {
            "Series_Name": series_name,
            "FRED_ID": series_id,
            "Rows": None,
            "First_Date": None,
            "Last_Date": None,
            "Missing_Values": None,
            "Status": f"Failed: {error}",
        }

        download_summary.append(summary_record)

        print(f"Download failed: {error}")


# ---------------------------------------------------------
# 7. Save a download summary
# ---------------------------------------------------------

summary_dataframe = pd.DataFrame(download_summary)

summary_file = (
    RAW_DATA_DIR
    / f"fred_download_summary_{extraction_date}.csv"
)

summary_dataframe.to_csv(
    summary_file,
    index=False,
)


# ---------------------------------------------------------
# 8. Print final status
# ---------------------------------------------------------

successful_downloads = (
    summary_dataframe["Status"] == "Success"
).sum()

total_downloads = len(SERIES_DICTIONARY)

print()
print("=" * 60)
print("FRED DOWNLOAD PROCESS COMPLETE")
print("=" * 60)
print(
    f"Successful downloads: "
    f"{successful_downloads} of {total_downloads}"
)
print(f"Summary saved to: {summary_file}")