import pandas as pd
import sqlite3

def main():
    conn = sqlite3.connect("health_monitoring.db")

    df = pd.read_sql("SELECT * FROM raw_health_reports", conn)

    validation_results = []

    for _, row in df.iterrows():
        issues = []

        if pd.isna(row["reported_cases"]):
            issues.append("Missing cases")

        if row["reported_cases"] is not None and row["reported_cases"] < 0:
            issues.append("Negative cases")

        if row["reported_cases"] == 0:
            issues.append("Zero cases")

        validation_results.append(", ".join(issues) if issues else "OK")

    df["validation_notes"] = pd.Series(validation_results, dtype="string")
    df["is_valid"] = df["validation_notes"] == "OK"

    # Duplicate handling (safe)
    duplicates = df.duplicated(
        subset=["report_date", "region", "disease"],
        keep="first"
    )

    df.loc[duplicates, "validation_notes"] = (
        df.loc[duplicates, "validation_notes"].astype(str) + " | Duplicate"
    )

    df.loc[duplicates, "is_valid"] = True

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

    processed_df.to_sql(
        "processed_health_reports",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    print("Validation completed.")


if __name__ == "__main__":
    main()