import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Regional Analytics",
    page_icon="🌍",
    layout="wide"
)

# ==================================================
# LOAD DATA
# ==================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/startup_data.csv")

df = load_data()

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.header("Regional Filters")

selected_regions = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

filtered_df = df[
    df["Region"].isin(selected_regions)
]

# ==================================================
# TITLE
# ==================================================

st.title("🌍 Regional Analytics Dashboard")

st.markdown("""
Analyze startup ecosystem performance across different regions,
including funding trends, revenue generation, valuation growth,
market share, and profitability.
""")

# ==================================================
# KPI SECTION
# ==================================================

total_regions = filtered_df["Region"].nunique()

total_startups = len(filtered_df)

total_funding = filtered_df[
    "Funding Amount (M USD)"
].sum()

total_revenue = filtered_df[
    "Revenue (M USD)"
].sum()

avg_valuation = filtered_df[
    "Valuation (M USD)"
].mean()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "🌍 Regions",
    total_regions
)

col2.metric(
    "🚀 Startups",
    f"{total_startups:,}"
)

col3.metric(
    "💰 Funding",
    f"${total_funding:,.0f} M"
)

col4.metric(
    "📈 Revenue",
    f"${total_revenue:,.0f} M"
)

col5.metric(
    "🏢 Avg Valuation",
    f"${avg_valuation:,.0f} M"
)

st.divider()

# ==================================================
# STARTUP DISTRIBUTION
# ==================================================

st.subheader("🚀 Startup Distribution by Region")

startup_count = (
    filtered_df["Region"]
    .value_counts()
    .reset_index()
)

startup_count.columns = [
    "Region",
    "Startups"
]

fig = px.bar(
    startup_count,
    x="Region",
    y="Startups",
    color="Region",
    text_auto=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==================================================
# FUNDING ANALYSIS
# ==================================================

st.subheader("💰 Funding by Region")

region_funding = (
    filtered_df.groupby("Region")
    ["Funding Amount (M USD)"]
    .sum()
    .reset_index()
)

fig = px.bar(
    region_funding,
    x="Region",
    y="Funding Amount (M USD)",
    color="Region",
    text_auto=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==================================================
# REVENUE ANALYSIS
# ==================================================

st.subheader("📈 Revenue by Region")

region_revenue = (
    filtered_df.groupby("Region")
    ["Revenue (M USD)"]
    .sum()
    .reset_index()
)

fig = px.bar(
    region_revenue,
    x="Region",
    y="Revenue (M USD)",
    color="Region",
    text_auto=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==================================================
# VALUATION ANALYSIS
# ==================================================

st.subheader("🏢 Average Valuation by Region")

valuation_data = (
    filtered_df.groupby("Region")
    ["Valuation (M USD)"]
    .mean()
    .reset_index()
)

fig = px.bar(
    valuation_data,
    x="Region",
    y="Valuation (M USD)",
    color="Region",
    text_auto=".2f"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==================================================
# PROFITABILITY ANALYSIS
# ==================================================

st.subheader("✅ Profitability Rate by Region")

profitability = (
    filtered_df.groupby("Region")
    ["Profitable"]
    .mean()
    .reset_index()
)

profitability["Profitable"] *= 100

fig = px.bar(
    profitability,
    x="Region",
    y="Profitable",
    color="Region",
    text_auto=".1f"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==================================================
# EMPLOYEE ANALYSIS
# ==================================================

st.subheader("👨‍💼 Employee Distribution")

fig = px.box(
    filtered_df,
    x="Region",
    y="Employees",
    color="Region"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==================================================
# MARKET SHARE ANALYSIS
# ==================================================

st.subheader("📊 Average Market Share")

market_share = (
    filtered_df.groupby("Region")
    ["Market Share (%)"]
    .mean()
    .reset_index()
)

fig = px.pie(
    market_share,
    names="Region",
    values="Market Share (%)",
    hole=0.4
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==================================================
# REGION VS INDUSTRY HEATMAP
# ==================================================

st.subheader("🔥 Industry Presence Across Regions")

heatmap_data = pd.pivot_table(
    filtered_df,
    values="Startup Name",
    index="Industry",
    columns="Region",
    aggfunc="count",
    fill_value=0
)

fig = px.imshow(
    heatmap_data,
    text_auto=True,
    aspect="auto"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==================================================
# FUNDING VS REVENUE
# ==================================================

st.subheader("📊 Funding vs Revenue by Region")

fig = px.scatter(
    filtered_df,
    x="Funding Amount (M USD)",
    y="Revenue (M USD)",
    color="Region",
    size="Valuation (M USD)",
    hover_name="Startup Name"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==================================================
# REGIONAL GROWTH SCORE
# ==================================================

st.subheader("🚀 Regional Growth Score")

growth_score = (
    filtered_df.groupby("Region")
    .agg({
        "Funding Amount (M USD)": "mean",
        "Revenue (M USD)": "mean",
        "Valuation (M USD)": "mean"
    })
)

growth_score["Growth Score"] = (
    growth_score["Funding Amount (M USD)"] +
    growth_score["Revenue (M USD)"] +
    growth_score["Valuation (M USD)"]
)

growth_score = growth_score.reset_index()

fig = px.bar(
    growth_score,
    x="Region",
    y="Growth Score",
    color="Region",
    text_auto=".0f"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==================================================
# REGIONAL LEADERBOARD
# ==================================================

st.subheader("🏆 Regional Leaderboard")

leaderboard = (
    filtered_df.groupby("Region")
    .agg({
        "Funding Amount (M USD)": "sum",
        "Revenue (M USD)": "sum",
        "Valuation (M USD)": "mean",
        "Employees": "mean"
    })
    .round(2)
    .sort_values(
        "Funding Amount (M USD)",
        ascending=False
    )
)

st.dataframe(
    leaderboard,
    use_container_width=True
)

# ==================================================
# AI INSIGHTS
# ==================================================

st.subheader("🧠 Regional Insights")

top_funding_region = (
    region_funding.sort_values(
        "Funding Amount (M USD)",
        ascending=False
    )
    .iloc[0]["Region"]
)

top_revenue_region = (
    region_revenue.sort_values(
        "Revenue (M USD)",
        ascending=False
    )
    .iloc[0]["Region"]
)

top_valuation_region = (
    valuation_data.sort_values(
        "Valuation (M USD)",
        ascending=False
    )
    .iloc[0]["Region"]
)

st.success(
    f"🏆 {top_funding_region} attracts the highest startup funding."
)

st.info(
    f"💰 {top_revenue_region} generates the highest startup revenue."
)

st.success(
    f"📈 {top_valuation_region} has the highest average startup valuation."
)

# ==================================================
# DATA PREVIEW
# ==================================================

with st.expander("📄 View Regional Dataset"):
    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.markdown("""
### Regional Analytics Summary

This dashboard helps identify:

- High-growth startup regions
- Funding hotspots
- Revenue-leading regions
- Valuation trends
- Market share leaders
- Regional investment opportunities

**Powered by Streamlit, Plotly, Pandas, and Business Intelligence Analytics.**
""")
