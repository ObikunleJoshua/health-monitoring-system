import pandas as pd
import sqlite3

# Connect to DB
conn = sqlite3.connect("health_monitoring.db")

# Load processed data (only valid records)
df = pd.read_sql("""
SELECT *
FROM processed_health_reports
WHERE is_valid = 1
""", conn)

# Ensure correct types
df["report_date"] = pd.to_datetime(df["report_date"])

# ---------------------------
# AGGREGATION
# ---------------------------

agg_df = df.groupby(
    ["report_date", "region", "disease"],
    as_index=False
).agg({
    "reported_cases": "sum",
    "vaccinations": "sum"
})

# ---------------------------
# ROLLING METRICS
# ---------------------------

agg_df = agg_df.sort_values(by=["region", "disease", "report_date"])

agg_df["avg_7d_cases"] = agg_df.groupby(
    ["region", "disease"]
)["reported_cases"].transform(
    lambda x: x.rolling(window=7, min_periods=1).mean()
)

# ---------------------------
# ANOMALY DETECTION
# ---------------------------

def detect_anomaly(row):
    if abs(row["reported_cases"] - row["avg_7d_cases"]) > 10:
        return 1
    return 0

agg_df["anomaly_flag"] = agg_df.apply(detect_anomaly, axis=1)

# ---------------------------
# FINAL METRICS
# ---------------------------

agg_df.rename(columns={
    "reported_cases": "total_cases"
}, inplace=True)

# Avoid division issues
agg_df["vaccination_rate"] = agg_df["vaccinations"] / (agg_df["total_cases"] + 1)

# Keep only required columns
final_df = agg_df[[
    "report_date",
    "region",
    "disease",
    "total_cases",
    "avg_7d_cases",
    "vaccination_rate",
    "anomaly_flag"
]]

# Save to SQL
final_df.to_sql(
    "aggregated_metrics",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("Anomaly detection completed and saved to aggregated_metrics.")