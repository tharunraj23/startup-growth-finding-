import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ----------------------------------------
# PAGE CONFIG
# ----------------------------------------

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📊",
    layout="wide"
)

# ----------------------------------------
# LOAD DATA
# ----------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("data/startup_data.csv")

df = load_data()

# ----------------------------------------
# SIDEBAR FILTERS
# ----------------------------------------

st.sidebar.header("Dashboard Filters")

industry = st.sidebar.multiselect(
    "Industry",
    options=df["Industry"].unique(),
    default=df["Industry"].unique()
)

region = st.sidebar.multiselect(
    "Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

filtered_df = df[
    (df["Industry"].isin(industry)) &
    (df["Region"].isin(region))
]

# ----------------------------------------
# TITLE
# ----------------------------------------

st.title("📊 Executive Dashboard")

st.markdown("""
This dashboard provides a high-level business overview
of startup performance, funding trends, revenue growth,
valuation metrics, and profitability insights.
""")

# ----------------------------------------
# KPI SECTION
# ----------------------------------------

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

profitability_rate = (
    filtered_df["Profitable"].mean() * 100
)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "🚀 Startups",
        f"{total_startups:,}"
    )

with col2:
    st.metric(
        "💰 Funding",
        f"${total_funding:,.0f} M"
    )

with col3:
    st.metric(
        "📈 Revenue",
        f"${total_revenue:,.0f} M"
    )

with col4:
    st.metric(
        "🏢 Avg Valuation",
        f"${avg_valuation:,.0f} M"
    )

with col5:
    st.metric(
        "✅ Profitability",
        f"{profitability_rate:.1f}%"
    )

st.divider()

# ----------------------------------------
# FUNDING VS REVENUE
# ----------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("Funding Distribution")

    fig = px.histogram(
        filtered_df,
        x="Funding Amount (M USD)",
        nbins=25,
        title="Funding Spread"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    st.subheader("Revenue Distribution")

    fig = px.histogram(
        filtered_df,
        x="Revenue (M USD)",
        nbins=25,
        title="Revenue Spread"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ----------------------------------------
# INDUSTRY OVERVIEW
# ----------------------------------------

st.subheader("🏭 Industry Performance")

industry_data = (
    filtered_df.groupby("Industry")
    .agg({
        "Funding Amount (M USD)": "sum",
        "Revenue (M USD)": "sum",
        "Valuation (M USD)": "mean"
    })
    .reset_index()
)

fig = px.bar(
    industry_data,
    x="Industry",
    y="Funding Amount (M USD)",
    color="Industry",
    text_auto=True,
    title="Total Funding by Industry"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------
# REGIONAL PERFORMANCE
# ----------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("🌎 Regional Distribution")

    region_data = (
        filtered_df["Region"]
        .value_counts()
        .reset_index()
    )

    region_data.columns = [
        "Region",
        "Count"
    ]

    fig = px.pie(
        region_data,
        names="Region",
        values="Count",
        hole=0.4
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    st.subheader("Regional Funding")

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

# ----------------------------------------
# TOP STARTUPS
# ----------------------------------------

st.subheader("🏆 Top 10 Startups by Valuation")

top_startups = (
    filtered_df.sort_values(
        by="Valuation (M USD)",
        ascending=False
    )
    .head(10)
)

fig = px.bar(
    top_startups,
    x="Startup Name",
    y="Valuation (M USD)",
    color="Industry",
    text_auto=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------
# FUNDING VS VALUATION
# ----------------------------------------

st.subheader("📈 Funding vs Valuation")

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

# ----------------------------------------
# PROFITABILITY ANALYSIS
# ----------------------------------------

st.subheader("📊 Profitability Analysis")

profitability = (
    filtered_df["Profitable"]
    .value_counts()
    .reset_index()
)

profitability.columns = [
    "Profitable",
    "Count"
]

fig = px.pie(
    profitability,
    names="Profitable",
    values="Count"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------
# AI GENERATED INSIGHTS
# ----------------------------------------

st.subheader("🧠 Executive Insights")

highest_funding_industry = (
    filtered_df.groupby("Industry")
    ["Funding Amount (M USD)"]
    .mean()
    .idxmax()
)

highest_revenue_industry = (
    filtered_df.groupby("Industry")
    ["Revenue (M USD)"]
    .mean()
    .idxmax()
)

best_region = (
    filtered_df.groupby("Region")
    ["Valuation (M USD)"]
    .mean()
    .idxmax()
)

st.success(
    f"🏆 {highest_funding_industry} has the highest average funding."
)

st.info(
    f"💰 {highest_revenue_industry} generates the highest average revenue."
)

st.success(
    f"🌎 {best_region} has the highest average startup valuation."
)

# ----------------------------------------
# DATA PREVIEW
# ----------------------------------------

with st.expander("📄 View Dataset"):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# ----------------------------------------
# FOOTER
# ----------------------------------------

st.markdown("---")

st.markdown(
    """
### Startup Analytics Intelligence System

Executive dashboard for monitoring startup ecosystem performance,
funding patterns, profitability, valuation growth, and regional trends.

**Technology Stack**
- Python
- Streamlit
- Plotly
- Pandas
- Business Intelligence Analytics
"""
)
