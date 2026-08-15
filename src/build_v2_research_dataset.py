from pathlib import Path

import pandas as pd


# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------
# Source files
# ------------------------------------------------------------

EBP_FILE = RAW_DIR / "fed_ebp_snapshot_2026-08-13.csv"

UNEMPLOYMENT_FILE = (
    RAW_DIR
    / "fred_UNRATE_snapshot_2026-07-28.csv"
)

RECESSION_FILE = (
    RAW_DIR
    / "fred_USREC_snapshot_2026-07-28.csv"
)

TREASURY_10Y_FILE = (
    RAW_DIR
    / "fred_DGS10_snapshot_2026-07-28.csv"
)

VIX_FILE = (
    RAW_DIR
    / "fred_VIXCLS_snapshot_2026-07-28.csv"
)

# ------------------------------------------------------------
# Sample A — Core Credit Sample
# ------------------------------------------------------------

core_credit = pd.read_csv(EBP_FILE)

core_credit["date"] = pd.to_datetime(
    core_credit["date"]
)

core_credit = core_credit[
    ["date", "gz_spread", "ebp", "est_prob"]
].copy()

core_credit = core_credit.sort_values("date").reset_index(drop=True)

OUTPUT_FILE = PROCESSED_DIR / "v2_core_credit_monthly.csv"

core_credit.to_csv(
    OUTPUT_FILE,
    index=False,
)

print("=" * 60)
print("V2 SAMPLE A — CORE CREDIT SAMPLE")
print("=" * 60)

print(f"First observation: {core_credit['date'].min().date()}")
print(f"Latest observation: {core_credit['date'].max().date()}")
print(f"Observations: {len(core_credit):,}")

print()
print("Missing values:")
print(core_credit.isna().sum())

print()
print(core_credit.head())
print()
print(core_credit.tail())

print()
print(f"Saved processed dataset: {OUTPUT_FILE}")

# ------------------------------------------------------------
# Sample B — Add unemployment
# ------------------------------------------------------------

unemployment = pd.read_csv(UNEMPLOYMENT_FILE)

unemployment["Date"] = pd.to_datetime(
    unemployment["Date"]
)

unemployment["UNEMPLOYMENT_RATE"] = pd.to_numeric(
    unemployment["UNEMPLOYMENT_RATE"],
    errors="coerce",
)

unemployment = unemployment.rename(
    columns={"Date": "date"}
)

sample_b = core_credit.merge(
    unemployment,
    on="date",
    how="left",
)

print()
print("=" * 60)
print("V2 SAMPLE B — AFTER UNEMPLOYMENT MERGE")
print("=" * 60)

print(f"Observations: {len(sample_b):,}")
print(f"First observation: {sample_b['date'].min().date()}")
print(f"Latest observation: {sample_b['date'].max().date()}")

print()
print("Missing values:")
print(sample_b.isna().sum())

print()
print("Missing unemployment dates:")
print(
    sample_b.loc[
        sample_b["UNEMPLOYMENT_RATE"].isna(),
        "date",
    ].dt.date.tolist()
)

# ------------------------------------------------------------
# Sample B — Add recession indicator
# ------------------------------------------------------------

recession = pd.read_csv(RECESSION_FILE)

recession["Date"] = pd.to_datetime(
    recession["Date"]
)

recession["RECESSION_FLAG"] = pd.to_numeric(
    recession["RECESSION_FLAG"],
    errors="coerce",
)

recession = recession.rename(
    columns={"Date": "date"}
)

sample_b = sample_b.merge(
    recession,
    on="date",
    how="left",
)

print()
print("=" * 60)
print("V2 SAMPLE B — AFTER RECESSION MERGE")
print("=" * 60)

print(f"Observations: {len(sample_b):,}")
print(f"First observation: {sample_b['date'].min().date()}")
print(f"Latest observation: {sample_b['date'].max().date()}")

print()
print("Missing values:")
print(sample_b.isna().sum())

print()
print("Missing recession dates:")
print(
    sample_b.loc[
        sample_b["RECESSION_FLAG"].isna(),
        "date",
    ].dt.date.tolist()
)

# ------------------------------------------------------------
# Sample B — Add monthly mean 10Y Treasury yield
# ------------------------------------------------------------

treasury = pd.read_csv(TREASURY_10Y_FILE)

treasury["Date"] = pd.to_datetime(
    treasury["Date"]
)

treasury["TREASURY_10Y"] = pd.to_numeric(
    treasury["TREASURY_10Y"],
    errors="coerce",
)

# Convert daily observations to calendar month.
treasury["date"] = (
    treasury["Date"]
    .dt.to_period("M")
    .dt.to_timestamp()
)

# Average available daily Treasury yields within each month.
treasury_monthly = (
    treasury
    .groupby("date", as_index=False)["TREASURY_10Y"]
    .mean()
)

sample_b = sample_b.merge(
    treasury_monthly,
    on="date",
    how="left",
)

print()
print("=" * 60)
print("V2 SAMPLE B — AFTER 10Y TREASURY MERGE")
print("=" * 60)

print(f"Observations: {len(sample_b):,}")
print(f"First observation: {sample_b['date'].min().date()}")
print(f"Latest observation: {sample_b['date'].max().date()}")

print()
print("Missing values:")
print(sample_b.isna().sum())

# ------------------------------------------------------------
# Save Sample B
# ------------------------------------------------------------

SAMPLE_B_OUTPUT = (
    PROCESSED_DIR
    / "v2_macro_credit_monthly.csv"
)

sample_b.to_csv(
    SAMPLE_B_OUTPUT,
    index=False,
)

print()
print(f"Saved Sample B: {SAMPLE_B_OUTPUT}")

# ------------------------------------------------------------
# Sample C — Add monthly mean VIX
# ------------------------------------------------------------

vix = pd.read_csv(VIX_FILE)

vix["Date"] = pd.to_datetime(
    vix["Date"]
)

vix["VIX"] = pd.to_numeric(
    vix["VIX"],
    errors="coerce",
)

# Convert daily observations to calendar month.
vix["date"] = (
    vix["Date"]
    .dt.to_period("M")
    .dt.to_timestamp()
)

# Average available daily VIX observations within each month.
vix_monthly = (
    vix
    .groupby("date", as_index=False)["VIX"]
    .mean()
)

# Sample C begins with Sample B but retains only months
# for which VIX history is potentially available.
sample_c = sample_b.merge(
    vix_monthly,
    on="date",
    how="inner",
)

print()
print("=" * 60)
print("V2 SAMPLE C — MARKET STRESS SAMPLE")
print("=" * 60)

print(f"Observations: {len(sample_c):,}")
print(f"First observation: {sample_c['date'].min().date()}")
print(f"Latest observation: {sample_c['date'].max().date()}")

print()
print("Missing values:")
print(sample_c.isna().sum())

SAMPLE_C_OUTPUT = (
    PROCESSED_DIR
    / "v2_market_stress_monthly.csv"
)

sample_c.to_csv(
    SAMPLE_C_OUTPUT,
    index=False,
)

print()
print(f"Saved Sample C: {SAMPLE_C_OUTPUT}")
