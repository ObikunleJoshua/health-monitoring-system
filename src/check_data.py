import sqlite3
import pandas as pd

conn = sqlite3.connect("health_monitoring.db")

# Total rows
total = pd.read_sql("SELECT COUNT(*) as total FROM aggregated_metrics", conn)
print("Total rows:")
print(total)

# Anomaly count
anomalies = pd.read_sql("""
SELECT COUNT(*) as anomaly_count
FROM aggregated_metrics
WHERE anomaly_flag = 1
""", conn)

print("\nAnomaly count:")
print(anomalies)

# Sample anomalies
sample = pd.read_sql("""
SELECT report_date, region, disease, total_cases, avg_7d_cases
FROM aggregated_metrics
WHERE anomaly_flag = 1
LIMIT 10
""", conn)

print("\nSample anomalies:")
print(sample)

conn.close()