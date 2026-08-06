from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

daily = pd.read_csv(
    PROJECT_ROOT
    / "data"
    / "processed"
    / "credit_market_daily.csv",
    parse_dates=["Date"],
)


# Keep only observations with an HY OAS value.
credit_data = daily.dropna(
    subset=["HY_OAS_BPS"]
).copy()


# Select the latest available credit observation.
latest = credit_data.iloc[-1]


# Measure how unusual the current spread is.
current_oas = latest["HY_OAS_BPS"]

current_drawdown = latest["HY_TOTAL_RETURN_DRAWDOWN"]
current_vix = latest["VIX"]

historical_percentile = (
    credit_data["HY_OAS_BPS"]
    .le(current_oas)
    .mean()
)


# Classify the one-month direction.
one_month_change = latest["HY_OAS_1M_CHANGE_BPS"]

if pd.isna(one_month_change):
    one_month_direction = "Unavailable"
elif one_month_change > 10:
    one_month_direction = "Deteriorating"
elif one_month_change < -10:
    one_month_direction = "Improving"
else:
    one_month_direction = "Broadly Stable"


# Print the analytical summary.
print()
print("=" * 55)
print("CURRENT HIGH-YIELD CREDIT MARKET SUMMARY")
print("=" * 55)

print(f"Observation date: {latest['Date'].date()}")
print(f"HY OAS: {current_oas:.0f} bps")
print(f"Credit regime: {latest['CREDIT_REGIME']}")

print(
    "Sample OAS percentile: "
    f"{historical_percentile:.1%}"
)

print(
    "1-month OAS change: "
    f"{one_month_change:+.0f} bps"
)

print(
    "3-month OAS change: "
    f"{latest['HY_OAS_3M_CHANGE_BPS']:+.0f} bps"
)

print(
    "1-month credit direction: "
    f"{one_month_direction}"
)

print(f"HY total return drawdown: {current_drawdown:.1%}")
print(f"VIX: {current_vix:.1f}")

print("=" * 55)

print()
print("MARKET CONTEXT")
print("-" * 55)

print(f"Sample minimum OAS: {credit_data['HY_OAS_BPS'].min():.0f} bps")
print(f"Sample median OAS : {credit_data['HY_OAS_BPS'].median():.0f} bps")
print(f"Sample maximum OAS: {credit_data['HY_OAS_BPS'].max():.0f} bps")

distance = current_oas - credit_data["HY_OAS_BPS"].median()

print(f"Distance from median: {distance:+.0f} bps")

worst_1m_idx = credit_data["HY_OAS_1M_CHANGE_BPS"].idxmax()
best_1m_idx = credit_data["HY_OAS_1M_CHANGE_BPS"].idxmin()

worst_1m_row = credit_data.loc[worst_1m_idx]
best_1m_row = credit_data.loc[best_1m_idx]

worst_1m_widening = worst_1m_row["HY_OAS_1M_CHANGE_BPS"]
worst_1m_date = worst_1m_row["Date"]

best_1m_tightening = best_1m_row["HY_OAS_1M_CHANGE_BPS"]
best_1m_date = best_1m_row["Date"]

print(
    f"Worst 1M widening: {worst_1m_widening:+.0f} bps "
    f"({worst_1m_date.date()})"
)

print(
    f"Best 1M tightening: {best_1m_tightening:+.0f} bps "
    f"({best_1m_date.date()})"
)
