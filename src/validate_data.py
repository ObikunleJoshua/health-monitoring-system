import pandas as pd
import sqlite3

# Connect to DB
conn = sqlite3.connect("health_monitoring.db")

# Load raw data
df = pd.read_sql("SELECT * FROM raw_health_reports", conn)

# ---------------------------
# VALIDATION RULES
# ---------------------------

validation_results = []

for idx, row in df.iterrows():
    issues = []

    # Rule 1: Missing values
    if pd.isna(row["reported_cases"]):
        issues.append("Missing cases")

    # Rule 2: Negative values
    if row["reported_cases"] is not None and row["reported_cases"] < 0:
        issues.append("Negative cases")

    # Rule 3: Zero cases (suspicious)
    if row["reported_cases"] == 0:
        issues.append("Zero cases (possible reporting issue)")

    validation_results.append(", ".join(issues) if issues else "OK")

df["validation_notes"] = validation_results
df["is_valid"] = df["validation_notes"] == "OK"

# ---------------------------
# DUPLICATE DETECTION
# ---------------------------

duplicates = df.duplicated(
    subset=["report_date", "region", "disease"], keep=False
)

# FORCE column to string (critical fix)
df["validation_notes"] = df["validation_notes"].astype(str)

# Now safe to concatenate
df.loc[duplicates, "validation_notes"] = (
    df.loc[duplicates, "validation_notes"] + " | Duplicate"
)

df.loc[duplicates, "is_valid"] = False

# ---------------------------
# SAVE TO PROCESSED TABLE
# ---------------------------

# Keep required columns only
processed_df = df[[
    "report_id",
    "report_date",
    "region",
    "disease",
    "reported_cases",
    "vaccinations",
    "is_valid",
    "validation_notes"
]]

# Save
processed_df.to_sql(
    "processed_health_reports",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("Validation completed and data saved to processed_health_reports.")