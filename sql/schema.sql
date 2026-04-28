CREATE TABLE raw_health_reports (
    report_id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_date DATE,
    region TEXT,
    disease TEXT,
    reported_cases INTEGER,
    vaccinations INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE processed_health_reports (
    report_id INTEGER PRIMARY KEY,
    report_date DATE,
    region TEXT,
    disease TEXT,
    reported_cases INTEGER,
    vaccinations INTEGER,
    is_valid BOOLEAN,
    validation_notes TEXT,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE aggregated_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_date DATE,
    region TEXT,
    disease TEXT,
    total_cases INTEGER,
    avg_7d_cases REAL,
    vaccination_rate REAL,
    anomaly_flag BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);