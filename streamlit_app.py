
import streamlit as st
import json
import os
import matplotlib.pyplot as plt

st.set_page_config(page_title="Equity Research Dashboard", layout="wide")
st.title("📊 Equity Intelligence Dashboard")

json_files = [f for f in os.listdir() if f.endswith(".json")]
companies = {}

for file in json_files:
    with open(file) as f:
        data = json.load(f)
        companies[data['company_name']] = data

company = st.selectbox("Select a company", list(companies.keys()))
data = companies[company]

col1, col2 = st.columns(2)
col1.metric("ROCE", data['ratios'].get("ROCE", ""))
col1.metric("P/E", data['ratios'].get("P/E", ""))
col2.metric("Debt/Equity", data['ratios'].get("Debt to equity", ""))
col2.metric("Promoter Holding", data['ratios'].get("Promoter holding", ""))

st.subheader("📄 Executive Summary")
st.write(data["executive_summary"])
st.subheader("📈 Growth Drivers")
st.write(data["growth_drivers"])
st.subheader("💰 Valuation View")
st.write(data["valuation_comment"])
st.subheader("⚠️ Risks")
st.write(data["risk_factors"])

if data["revenue"] and data["net_profit"]:
    st.subheader("📊 Revenue & Profit Trend")
    fig, ax = plt.subplots()
    years = list(data["revenue"].keys())
    ax.plot(years, list(data["revenue"].values()), label="Revenue")
    ax.plot(years, list(data["net_profit"].values()), label="Net Profit")
    ax.legend()
    st.pyplot(fig)

base = company.replace(" ", "_")
st.download_button("📥 Download PDF", open(f"{base}_Research_Report.pdf", "rb"), f"{base}.pdf")
