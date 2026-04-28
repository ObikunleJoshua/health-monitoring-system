import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Health Monitoring System", layout="wide")

# ---------------------------
# AUTH SYSTEM
# ---------------------------
def login():
    st.sidebar.title("🔐 Login")

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state["logged_in"] = True
        else:
            st.sidebar.error("Invalid credentials")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
    st.stop()

# ---------------------------
# AUTO-SETUP DATABASE
# ---------------------------
import os

if not os.path.exists("health_monitoring.db"):
    from src import generate_data, load_data, validate_data, anomaly_detection, db_setup

    db_setup.main()          
    generate_data.main()    
    load_data.main()        
    validate_data.main()     
    anomaly_detection.main()

# ---------------------------
# LOAD DATA
# ---------------------------
conn = sqlite3.connect("health_monitoring.db")

agg_df = pd.read_sql("SELECT * FROM aggregated_metrics", conn)
proc_df = pd.read_sql("SELECT * FROM processed_health_reports", conn)

conn.close()

# Fix date type
agg_df["report_date"] = pd.to_datetime(agg_df["report_date"])

# ---------------------------
# HEADER
# ---------------------------
st.title("🏥 Public Health Monitoring System")
st.markdown("Monitor disease trends, anomalies, and data quality in real-time.")

# ---------------------------
# KPI SECTION
# ---------------------------
total_cases = int(agg_df["total_cases"].sum())
total_anomalies = int(agg_df["anomaly_flag"].sum())
invalid_records = len(proc_df[proc_df["is_valid"] == 0])

col1, col2, col3 = st.columns(3)

col1.metric("📊 Total Cases", f"{total_cases:,}")
col2.metric("⚠️ Anomalies Detected", total_anomalies)
col3.metric("🧪 Data Issues", invalid_records)

# ---------------------------
# ALERT SYSTEM
# ---------------------------
if total_anomalies > 50:
    st.error("🚨 High number of anomalies detected!")
elif total_anomalies > 0:
    st.warning("⚠️ Some anomalies detected.")
else:
    st.success("✅ System stable.")

# ---------------------------
# SIDEBAR FILTERS
# ---------------------------
st.sidebar.header("Filters")

regions = st.sidebar.multiselect(
    "Region",
    options=agg_df["region"].unique(),
    default=agg_df["region"].unique()
)

diseases = st.sidebar.multiselect(
    "Disease",
    options=agg_df["disease"].unique(),
    default=agg_df["disease"].unique()
)

filtered_df = agg_df[
    (agg_df["region"].isin(regions)) &
    (agg_df["disease"].isin(diseases))
]

# ---------------------------
# TREND CHART (PLOTLY)
# ---------------------------
st.subheader("📈 Disease Trends Over Time")

trend = filtered_df.groupby("report_date")["total_cases"].sum().reset_index()

fig = px.line(
    trend,
    x="report_date",
    y="total_cases",
    title="Total Cases Over Time"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# ANOMALIES TABLE
# ---------------------------
st.subheader("⚠️ Detected Anomalies")

anomalies = filtered_df[filtered_df["anomaly_flag"] == 1]

if len(anomalies) > 0:
    st.dataframe(anomalies.sort_values(by="total_cases", ascending=False).head(20))
else:
    st.info("No anomalies detected.")

# ---------------------------
# DATA QUALITY ISSUES
# ---------------------------
st.subheader("🧪 Data Quality Issues")

issues = proc_df[proc_df["is_valid"] == 0]

st.dataframe(issues.head(20))

# ---------------------------
# INSIGHT ENGINE
# ---------------------------
st.subheader("🧠 Automated Insights")

if len(trend) > 1:
    latest = trend.iloc[-1]["total_cases"]
    previous = trend.iloc[-2]["total_cases"]

    if latest > previous:
        st.info("📈 Cases are increasing.")
    elif latest < previous:
        st.info("📉 Cases are decreasing.")
    else:
        st.info("➡️ Cases are stable.")

# ---------------------------
# DOWNLOAD REPORT
# ---------------------------
st.subheader("📥 Export Anomaly Report")

csv = anomalies.to_csv(index=False)

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="anomaly_report.csv",
    mime="text/csv"
)