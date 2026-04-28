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

## Run Locally

```bash
pip install -r requirements.txt
python src/generate_data.py
python src/load_data.py
python src/validate_data.py
python src/anomaly_detection.py
python -m streamlit run app.py