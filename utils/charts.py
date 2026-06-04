import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# ==================================================
# INDUSTRY FUNDING CHART
# ==================================================

def industry_funding_chart(df):

    industry_funding = (
        df.groupby("Industry")
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
        text_auto=True,
        title="Funding by Industry"
    )

    return fig


# ==================================================
# INDUSTRY REVENUE CHART
# ==================================================

def industry_revenue_chart(df):

    industry_revenue = (
        df.groupby("Industry")
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
        text_auto=True,
        title="Revenue by Industry"
    )

    return fig


# ==================================================
# REGION FUNDING CHART
# ==================================================

def region_funding_chart(df):

    region_funding = (
        df.groupby("Region")
        ["Funding Amount (M USD)"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        region_funding,
        values="Funding Amount (M USD)",
        names="Region",
        hole=0.4,
        title="Funding Distribution by Region"
    )

    return fig


# ==================================================
# REGION REVENUE CHART
# ==================================================

def region_revenue_chart(df):

    region_revenue = (
        df.groupby("Region")
        ["Revenue (M USD)"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        region_revenue,
        x="Region",
        y="Revenue (M USD)",
        color="Region",
        text_auto=True,
        title="Revenue by Region"
    )

    return fig


# ==================================================
# FUNDING VS VALUATION
# ==================================================

def funding_vs_valuation_chart(df):

    fig = px.scatter(
        df,
        x="Funding Amount (M USD)",
        y="Valuation (M USD)",
        size="Revenue (M USD)",
        color="Industry",
        hover_name="Startup Name",
        title="Funding vs Valuation"
    )

    return fig


# ==================================================
# REVENUE VS EMPLOYEES
# ==================================================

def revenue_vs_employees_chart(df):

    fig = px.scatter(
        df,
        x="Employees",
        y="Revenue (M USD)",
        size="Valuation (M USD)",
        color="Industry",
        hover_name="Startup Name",
        title="Revenue vs Employees"
    )

    return fig


# ==================================================
# PROFITABILITY CHART
# ==================================================

def profitability_chart(df):

    profitability = (
        df["Profitable"]
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
        values="Count",
        title="Profitability Analysis"
    )

    return fig


# ==================================================
# TOP STARTUPS CHART
# ==================================================

def top_startups_chart(df, top_n=10):

    top_df = (
        df.sort_values(
            "Valuation (M USD)",
            ascending=False
        )
        .head(top_n)
    )

    fig = px.bar(
        top_df,
        x="Startup Name",
        y="Valuation (M USD)",
        color="Industry",
        text_auto=True,
        title=f"Top {top_n} Startups by Valuation"
    )

    return fig


# ==================================================
# FUNDING DISTRIBUTION
# ==================================================

def funding_distribution_chart(df):

    fig = px.histogram(
        df,
        x="Funding Amount (M USD)",
        nbins=30,
        title="Funding Distribution"
    )

    return fig


# ==================================================
# REVENUE DISTRIBUTION
# ==================================================

def revenue_distribution_chart(df):

    fig = px.histogram(
        df,
        x="Revenue (M USD)",
        nbins=30,
        title="Revenue Distribution"
    )

    return fig


# ==================================================
# MARKET SHARE CHART
# ==================================================

def market_share_chart(df):

    market_share = (
        df.groupby("Industry")
        ["Market Share (%)"]
        .mean()
        .reset_index()
    )

    fig = px.pie(
        market_share,
        values="Market Share (%)",
        names="Industry",
        hole=0.4,
        title="Average Market Share"
    )

    return fig


# ==================================================
# INDUSTRY TREEMAP
# ==================================================

def industry_treemap(df):

    fig = px.treemap(
        df,
        path=["Industry"],
        values="Revenue (M USD)",
        color="Revenue (M USD)"
    )

    return fig


# ==================================================
# HEATMAP
# ==================================================

def industry_region_heatmap(df):

    heatmap_data = pd.pivot_table(
        df,
        values="Funding Amount (M USD)",
        index="Industry",
        columns="Region",
        aggfunc="sum",
        fill_value=0
    )

    fig = px.imshow(
        heatmap_data,
        text_auto=True,
        aspect="auto",
        title="Industry vs Region Funding Heatmap"
    )

    return fig


# ==================================================
# GROWTH SCORE CHART
# ==================================================

def growth_score_chart(df):

    temp_df = df.copy()

    temp_df["Growth Score"] = (
        temp_df["Funding Amount (M USD)"] * 0.30 +
        temp_df["Revenue (M USD)"] * 0.30 +
        temp_df["Valuation (M USD)"] * 0.30 +
        temp_df["Market Share (%)"] * 0.10
    )

    top_growth = (
        temp_df.sort_values(
            "Growth Score",
            ascending=False
        )
        .head(15)
    )

    fig = px.bar(
        top_growth,
        x="Startup Name",
        y="Growth Score",
        color="Industry",
        title="Top Growth Startups"
    )

    return fig


# ==================================================
# CLUSTER VISUALIZATION
# ==================================================

def cluster_chart(df):

    if "Cluster Name" not in df.columns:
        return None

    fig = px.scatter(
        df,
        x="Funding Amount (M USD)",
        y="Valuation (M USD)",
        size="Revenue (M USD)",
        color="Cluster Name",
        hover_name="Startup Name",
        title="Startup Clustering"
    )

    return fig


# ==================================================
# KPI HELPER
# ==================================================

def create_gauge_chart(value, title):

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            title={"text": title},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"thickness": 0.4}
            }
        )
    )

    return fig
