import sqlite3

def main():
    conn = sqlite3.connect("health_monitoring.db")
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS raw_health_reports (
        report_id INTEGER PRIMARY KEY AUTOINCREMENT,
        report_date DATE,
        region TEXT,
        disease TEXT,
        reported_cases INTEGER,
        vaccinations INTEGER
    );

    CREATE TABLE IF NOT EXISTS processed_health_reports (
        report_id INTEGER,
        report_date DATE,
        region TEXT,
        disease TEXT,
        reported_cases INTEGER,
        vaccinations INTEGER,
        is_valid BOOLEAN,
        validation_notes TEXT
    );

    CREATE TABLE IF NOT EXISTS aggregated_metrics (
        report_date DATE,
        region TEXT,
        disease TEXT,
        total_cases INTEGER,
        avg_7d_cases REAL,
        vaccination_rate REAL,
        anomaly_flag INTEGER
    );
    """)

    conn.commit()
    conn.close()

    print("Database setup complete.")


if __name__ == "__main__":
    main()