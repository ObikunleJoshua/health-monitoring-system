import pandas as pd
import sqlite3

# Load CSV
df = pd.read_csv("data/raw_health_data.csv")

print("CSV rows:", len(df))  # DEBUG

# Rename columns to match SQL
df.rename(columns={
    "date": "report_date",
    "cases": "reported_cases"
}, inplace=True)

# Connect DB
conn = sqlite3.connect("health_monitoring.db")

# CLEAR TABLE before loading (important)
conn.execute("DELETE FROM raw_health_reports")

# Insert data
df.to_sql("raw_health_reports", conn, if_exists="append", index=False)

conn.commit()
conn.close()

print("Data loaded into raw_health_reports.")