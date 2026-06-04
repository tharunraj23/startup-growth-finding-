import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Industry Analysis",
    page_icon="🏭",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("data/startup_data.csv")

df = load_data()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.header("Industry Filters")

selected_industries = st.sidebar.multiselect(
    "Select Industries",
    df["Industry"].unique(),
    default=df["Industry"].unique()
)

filtered_df = df[
    df["Industry"].isin(selected_industries)
]

# --------------------------------------------------
# PAGE TITLE
# --------------------------------------------------

st.title("🏭 Industry Analysis Dashboard")

st.markdown("""
Analyze startup ecosystem performance across industries,
including funding, valuation, profitability, revenue,
market share, and employee growth.
""")

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

total_industries = filtered_df["Industry"].nunique()

total_funding = filtered_df[
    "Funding Amount (M USD)"
].sum()

total_revenue = filtered_df[
    "Revenue (M USD)"
].sum()

avg_valuation = filtered_df[
    "Valuation (M USD)"
].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Industries",
    total_industries
)

col2.metric(
    "Funding",
    f"${total_funding:,.0f} M"
)

col3.metric(
    "Revenue",
    f"${total_revenue:,.0f} M"
)

col4.metric(
    "Avg Valuation",
    f"${avg_valuation:,.0f} M"
)

st.divider()

# --------------------------------------------------
# FUNDING BY INDUSTRY
# --------------------------------------------------

st.subheader("💰 Funding by Industry")

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

# --------------------------------------------------
# REVENUE ANALYSIS
# --------------------------------------------------

st.subheader("📈 Revenue by Industry")

industry_revenue = (
    filtered_df.groupby("Industry")
    ["Revenue (M USD)"]
    .sum()
    .reset_index()
    .sort_values(
        "Revenue (M USD)",
        ascending=False
    )
)

fig = px.bar(
    industry_revenue,
    x="Industry",
    y="Revenue (M USD)",
    color="Industry",
    text_auto=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# VALUATION ANALYSIS
# --------------------------------------------------

st.subheader("🏢 Industry Valuation")

industry_valuation = (
    filtered_df.groupby("Industry")
    ["Valuation (M USD)"]
    .mean()
    .reset_index()
)

fig = px.bar(
    industry_valuation,
    x="Industry",
    y="Valuation (M USD)",
    color="Industry",
    text_auto=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# FUNDING VS VALUATION
# --------------------------------------------------

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

# --------------------------------------------------
# EMPLOYEE DISTRIBUTION
# --------------------------------------------------

st.subheader("👨‍💼 Employee Distribution")

fig = px.box(
    filtered_df,
    x="Industry",
    y="Employees",
    color="Industry"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# PROFITABILITY ANALYSIS
# --------------------------------------------------

st.subheader("✅ Profitability by Industry")

profitability = (
    filtered_df.groupby("Industry")
    ["Profitable"]
    .mean()
    .reset_index()
)

profitability["Profitable"] *= 100

fig = px.bar(
    profitability,
    x="Industry",
    y="Profitable",
    color="Industry",
    text_auto=".1f"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# FUNDING ROUNDS ANALYSIS
# --------------------------------------------------

st.subheader("🔄 Funding Rounds Analysis")

funding_rounds = (
    filtered_df.groupby("Industry")
    ["Funding Rounds"]
    .mean()
    .reset_index()
)

fig = px.line(
    funding_rounds,
    x="Industry",
    y="Funding Rounds",
    markers=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# INDUSTRY MARKET SHARE
# --------------------------------------------------

st.subheader("🌍 Industry Market Share")

market_share = (
    filtered_df.groupby("Industry")
    ["Market Share (%)"]
    .mean()
    .reset_index()
)

fig = px.pie(
    market_share,
    names="Industry",
    values="Market Share (%)",
    hole=0.4
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# TREEMAP
# --------------------------------------------------

st.subheader("🌳 Industry Revenue Treemap")

fig = px.treemap(
    filtered_df,
    path=["Industry"],
    values="Revenue (M USD)",
    color="Revenue (M USD)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# TOP INDUSTRIES TABLE
# --------------------------------------------------

st.subheader("🏆 Industry Ranking")

ranking = (
    filtered_df.groupby("Industry")
    .agg({
        "Funding Amount (M USD)": "sum",
        "Revenue (M USD)": "sum",
        "Valuation (M USD)": "mean",
        "Employees": "mean"
    })
    .round(2)
)

st.dataframe(
    ranking,
    use_container_width=True
)

# --------------------------------------------------
# AI GENERATED INSIGHTS
# --------------------------------------------------

st.subheader("🧠 AI Industry Insights")

highest_funding = (
    industry_funding.iloc[0]["Industry"]
)

highest_revenue = (
    industry_revenue.iloc[0]["Industry"]
)

highest_valuation = (
    industry_valuation.sort_values(
        "Valuation (M USD)",
        ascending=False
    )
    .iloc[0]["Industry"]
)

st.success(
    f"🏆 {highest_funding} attracts the highest total funding."
)

st.info(
    f"💰 {highest_revenue} generates the highest total revenue."
)

st.success(
    f"📈 {highest_valuation} has the highest average valuation."
)

# --------------------------------------------------
# DATA PREVIEW
# --------------------------------------------------

with st.expander("📄 Industry Dataset"):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.markdown("""
### Industry Analytics Summary

This dashboard helps stakeholders identify:

- High-growth industries
- Investment opportunities
- Revenue leaders
- Valuation trends
- Market share dominance
- Profitability patterns

**Built using Streamlit, Plotly, Pandas, and Business Intelligence techniques.**
""")
