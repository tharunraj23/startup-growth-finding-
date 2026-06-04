import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Funding Insights",
    page_icon="💰",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/startup_data.csv")

df = load_data()

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header("Funding Filters")

industry_filter = st.sidebar.multiselect(
    "Industry",
    df["Industry"].unique(),
    default=df["Industry"].unique()
)

region_filter = st.sidebar.multiselect(
    "Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

filtered_df = df[
    (df["Industry"].isin(industry_filter)) &
    (df["Region"].isin(region_filter))
]

# =====================================================
# PAGE TITLE
# =====================================================

st.title("💰 Funding Insights Dashboard")

st.markdown("""
Comprehensive funding intelligence dashboard for analyzing
investment patterns, startup funding performance,
valuation growth, and funding efficiency.
""")

# =====================================================
# KPI SECTION
# =====================================================

total_funding = filtered_df[
    "Funding Amount (M USD)"
].sum()

avg_funding = filtered_df[
    "Funding Amount (M USD)"
].mean()

max_funding = filtered_df[
    "Funding Amount (M USD)"
].max()

avg_rounds = filtered_df[
    "Funding Rounds"
].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Total Funding",
    f"${total_funding:,.0f} M"
)

col2.metric(
    "📊 Avg Funding",
    f"${avg_funding:,.1f} M"
)

col3.metric(
    "🚀 Highest Funding",
    f"${max_funding:,.1f} M"
)

col4.metric(
    "🔄 Avg Rounds",
    f"{avg_rounds:.1f}"
)

st.divider()

# =====================================================
# FUNDING DISTRIBUTION
# =====================================================

st.subheader("📈 Funding Distribution")

fig = px.histogram(
    filtered_df,
    x="Funding Amount (M USD)",
    nbins=30,
    title="Funding Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# INDUSTRY FUNDING
# =====================================================

st.subheader("🏭 Funding by Industry")

industry_funding = (
    filtered_df.groupby("Industry")
    ["Funding Amount (M USD)"]
    .sum()
    .reset_index()
    .sort_values(
        "Funding Amount (M USD)",
        ascending=False
    )
)

fig = px.bar(
    industry_funding,
    x="Industry",
    y="Funding Amount (M USD)",
    color="Industry",
    text_auto=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# REGION FUNDING
# =====================================================

st.subheader("🌍 Funding by Region")

region_funding = (
    filtered_df.groupby("Region")
    ["Funding Amount (M USD)"]
    .sum()
    .reset_index()
)

fig = px.pie(
    region_funding,
    names="Region",
    values="Funding Amount (M USD)",
    hole=0.4
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# FUNDING ROUNDS ANALYSIS
# =====================================================

st.subheader("🔄 Funding Rounds Analysis")

rounds_data = (
    filtered_df.groupby("Industry")
    ["Funding Rounds"]
    .mean()
    .reset_index()
)

fig = px.line(
    rounds_data,
    x="Industry",
    y="Funding Rounds",
    markers=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# FUNDING VS VALUATION
# =====================================================

st.subheader("📊 Funding vs Valuation")

fig = px.scatter(
    filtered_df,
    x="Funding Amount (M USD)",
    y="Valuation (M USD)",
    size="Revenue (M USD)",
    color="Industry",
    hover_name="Startup Name"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# FUNDING VS REVENUE
# =====================================================

st.subheader("📈 Funding vs Revenue")

fig = px.scatter(
    filtered_df,
    x="Funding Amount (M USD)",
    y="Revenue (M USD)",
    color="Industry",
    size="Valuation (M USD)",
    hover_name="Startup Name"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# TOP FUNDED STARTUPS
# =====================================================

st.subheader("🏆 Top 15 Funded Startups")

top_funded = (
    filtered_df.sort_values(
        "Funding Amount (M USD)",
        ascending=False
    )
    .head(15)
)

fig = px.bar(
    top_funded,
    x="Startup Name",
    y="Funding Amount (M USD)",
    color="Industry",
    text_auto=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# FUNDING EFFICIENCY SCORE
# =====================================================

st.subheader("⚡ Funding Efficiency Analysis")

filtered_df["Funding Efficiency"] = (
    filtered_df["Revenue (M USD)"] /
    filtered_df["Funding Amount (M USD)"]
)

efficiency = (
    filtered_df.groupby("Industry")
    ["Funding Efficiency"]
    .mean()
    .reset_index()
)

fig = px.bar(
    efficiency,
    x="Industry",
    y="Funding Efficiency",
    color="Industry",
    text_auto=".2f"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# VALUATION MULTIPLIER
# =====================================================

st.subheader("📈 Valuation Multiplier")

filtered_df["Valuation Multiplier"] = (
    filtered_df["Valuation (M USD)"] /
    filtered_df["Funding Amount (M USD)"]
)

valuation_multiplier = (
    filtered_df.groupby("Industry")
    ["Valuation Multiplier"]
    .mean()
    .reset_index()
)

fig = px.bar(
    valuation_multiplier,
    x="Industry",
    y="Valuation Multiplier",
    color="Industry",
    text_auto=".2f"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# INVESTMENT HEATMAP
# =====================================================

st.subheader("🔥 Industry-Region Investment Heatmap")

heatmap_data = pd.pivot_table(
    filtered_df,
    values="Funding Amount (M USD)",
    index="Industry",
    columns="Region",
    aggfunc="sum"
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

# =====================================================
# FUNDING LEADERBOARD TABLE
# =====================================================

st.subheader("📋 Funding Leaderboard")

leaderboard = (
    filtered_df.groupby("Industry")
    .agg({
        "Funding Amount (M USD)": "sum",
        "Revenue (M USD)": "sum",
        "Valuation (M USD)": "mean",
        "Funding Rounds": "mean"
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

# =====================================================
# AI INSIGHTS
# =====================================================

st.subheader("🧠 AI Funding Insights")

highest_funded_industry = (
    industry_funding.iloc[0]["Industry"]
)

highest_efficiency = (
    efficiency.sort_values(
        "Funding Efficiency",
        ascending=False
    )
    .iloc[0]["Industry"]
)

highest_multiplier = (
    valuation_multiplier.sort_values(
        "Valuation Multiplier",
        ascending=False
    )
    .iloc[0]["Industry"]
)

st.success(
    f"🏆 {highest_funded_industry} attracts the highest total investment."
)

st.info(
    f"⚡ {highest_efficiency} delivers the best funding efficiency."
)

st.success(
    f"📈 {highest_multiplier} achieves the highest valuation multiplier."
)

# =====================================================
# DATA PREVIEW
# =====================================================

with st.expander("📄 View Funding Dataset"):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.markdown("""
### Funding Analytics Summary

This dashboard helps investors and stakeholders identify:

- High-investment industries
- Efficient capital utilization
- Funding-to-revenue performance
- Valuation growth potential
- Regional investment trends
- Startup funding leaders

**Powered by Streamlit, Plotly, Pandas, and Business Intelligence Analytics.**
""")
