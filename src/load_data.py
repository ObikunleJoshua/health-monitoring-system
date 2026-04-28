import pandas as pd
import sqlite3

def main():
    df = pd.read_csv("data/raw_health_data.csv")

    df.rename(columns={
        "date": "report_date",
        "cases": "reported_cases"
    }, inplace=True)

    conn = sqlite3.connect("health_monitoring.db")

    conn.execute("DELETE FROM raw_health_reports")

    df.to_sql("raw_health_reports", conn, if_exists="append", index=False)

    conn.commit()
    conn.close()

    print("Data loaded into raw_health_reports.")


if __name__ == "__main__":
    main()