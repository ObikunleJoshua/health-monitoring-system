import sqlite3
import pandas as pd

def main():
    conn = sqlite3.connect("health_monitoring.db")

    df = pd.read_sql("SELECT COUNT(*) as total FROM aggregated_metrics", conn)
    print(df)

    conn.close()


if __name__ == "__main__":
    main()