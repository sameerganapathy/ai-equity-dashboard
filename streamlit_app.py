
import streamlit as st
import json
import os
import matplotlib.pyplot as plt

st.set_page_config(page_title="Equity Research Dashboard", layout="wide")
st.title("📊 Equity Intelligence Dashboard")

json_files = [f for f in os.listdir() if f.endswith(".json")]
companies = {}

for file in json_files:
    try:
        with open(file) as f:
            data = json.load(f)
            if "company_name" not in data:
                continue
            companies[data["company_name"]] = data
    except Exception as e:
        st.warning(f"❌ Error reading {file}: {e}")

if not companies:
    st.warning("No valid reports found.")
    st.stop()

company = st.selectbox("Select a company", list(companies.keys()))
data = companies[company]

col1, col2 = st.columns(2)
col1.metric("ROCE", data["ratios"].get("ROCE", "N/A"))
col1.metric("P/E", data["ratios"].get("P/E", "N/A"))
col2.metric("Debt/Equity", data["ratios"].get("Debt to equity", "N/A"))
col2.metric("Promoter Holding", data["ratios"].get("Promoter holding", "N/A"))

st.subheader("📄 Executive Summary")
st.write(data.get("executive_summary", "Not available."))

st.subheader("📈 Growth Drivers")
st.write(data.get("growth_drivers", "Not available."))

st.subheader("💰 Valuation View")
st.write(data.get("valuation_comment", "Not available."))

st.subheader("⚠️ Risks")
st.write(data.get("risk_factors", "Not available."))

if data.get("revenue") and data.get("net_profit"):
    st.subheader("📊 Revenue & Profit Trend")
    fig, ax = plt.subplots()
    years = list(data["revenue"].keys())
    ax.plot(years, list(data["revenue"].values()), label="Revenue")
    ax.plot(years, list(data["net_profit"].values()), label="Net Profit")
    ax.legend()
    st.pyplot(fig)

base = company.replace(" ", "_")
if os.path.exists(f"{base}_Report.pdf"):
    st.download_button("📥 Download PDF", open(f"{base}_Report.pdf", "rb"), f"{base}.pdf")

if os.path.exists(f"{base}_Report.json"):
    st.download_button("📥 Download JSON", open(f"{base}_Report.json", "rb"), f"{base}.json")
