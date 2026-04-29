# 🏥 Public Health Monitoring System

A data monitoring system that simulates real-world public health pipelines, including data ingestion, validation, anomaly detection, and dashboard visualization.

---

## Features

- Data pipeline (Python + SQL)
- Data validation engine
- Anomaly detection system
- Interactive dashboard (Streamlit + Plotly)
- Authentication system
- Business insights & reporting

---

## Use Case

Designed for health officers to monitor:
- Disease trends
- Data quality issues
- Potential outbreak anomalies

---

## Tech Stack

- Python (Pandas, NumPy)
- SQLite
- Streamlit
- Plotly

---

## Dashboard Preview

![Dashboard](images/dashboard.png)
![Dashboard](images/plotly.png)
![Dashboard](images/risk.png)

---
## System Architecture

Data Flow:
CSV → SQL → Validation → Aggregation → Dashboard

Components:
- Data Generator (synthetic health data)
- Validation Engine (data quality checks)
- Anomaly Detection (trend deviation)
- Dashboard (Streamlit + Plotly)

---

## Run Locally

```bash
pip install -r requirements.txt
python src/generate_data.py
python src/load_data.py
python src/validate_data.py
python src/anomaly_detection.py
python -m streamlit run app.py