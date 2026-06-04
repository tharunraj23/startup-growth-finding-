import pandas as pd
import streamlit as st

# ==========================================
# LOAD DATASET
# ==========================================

@st.cache_data
def load_data():
    """
    Load startup dataset and perform
    basic cleaning.
    """

    try:
        df = pd.read_csv("data/startup_data.csv")

        # Remove duplicate rows
        df = df.drop_duplicates()

        # Remove leading/trailing spaces
        df.columns = df.columns.str.strip()

        # Fill missing numeric values
        numeric_cols = df.select_dtypes(
            include=["int64", "float64"]
        ).columns

        for col in numeric_cols:
            df[col] = df[col].fillna(
                df[col].median()
            )

        # Fill missing categorical values
        categorical_cols = df.select_dtypes(
            include=["object"]
        ).columns

        for col in categorical_cols:
            df[col] = df[col].fillna(
                "Unknown"
            )

        return df

    except FileNotFoundError:

        st.error(
            "Dataset not found. Place startup_data.csv inside data/ folder."
        )

        return pd.DataFrame()

    except Exception as e:

        st.error(
            f"Error loading dataset: {e}"
        )

        return pd.DataFrame()


# ==========================================
# FILTER DATA
# ==========================================

def filter_data(
    df,
    industries=None,
    regions=None
):
    """
    Filter dataset based on
    selected industries and regions.
    """

    filtered_df = df.copy()

    if industries:
        filtered_df = filtered_df[
            filtered_df["Industry"]
            .isin(industries)
        ]

    if regions:
        filtered_df = filtered_df[
            filtered_df["Region"]
            .isin(regions)
        ]

    return filtered_df


# ==========================================
# KPI CALCULATIONS
# ==========================================

def get_kpis(df):
    """
    Calculate dashboard KPIs.
    """

    kpis = {
        "total_startups": len(df),

        "total_funding":
        df["Funding Amount (M USD)"].sum(),

        "total_revenue":
        df["Revenue (M USD)"].sum(),

        "avg_valuation":
        df["Valuation (M USD)"].mean(),

        "avg_employees":
        df["Employees"].mean(),

        "profitability_rate":
        df["Profitable"].mean() * 100
    }

    return kpis


# ==========================================
# INDUSTRY SUMMARY
# ==========================================

def industry_summary(df):
    """
    Industry-wise summary.
    """

    return (
        df.groupby("Industry")
        .agg({
            "Funding Amount (M USD)": "sum",
            "Revenue (M USD)": "sum",
            "Valuation (M USD)": "mean",
            "Employees": "mean"
        })
        .round(2)
        .reset_index()
    )


# ==========================================
# REGION SUMMARY
# ==========================================

def region_summary(df):
    """
    Region-wise summary.
    """

    return (
        df.groupby("Region")
        .agg({
            "Funding Amount (M USD)": "sum",
            "Revenue (M USD)": "sum",
            "Valuation (M USD)": "mean",
            "Employees": "mean"
        })
        .round(2)
        .reset_index()
    )


# ==========================================
# TOP STARTUPS
# ==========================================

def top_startups(
    df,
    n=10
):
    """
    Get top startups by valuation.
    """

    return (
        df.sort_values(
            by="Valuation (M USD)",
            ascending=False
        )
        .head(n)
    )


# ==========================================
# AI INSIGHT HELPERS
# ==========================================

def generate_ai_insights(df):
    """
    Generate automated business insights.
    """

    insights = []

    try:

        top_funding_industry = (
            df.groupby("Industry")
            ["Funding Amount (M USD)"]
            .mean()
            .idxmax()
        )

        insights.append(
            f"🏆 {top_funding_industry} receives the highest average funding."
        )

        top_revenue_industry = (
            df.groupby("Industry")
            ["Revenue (M USD)"]
            .mean()
            .idxmax()
        )

        insights.append(
            f"💰 {top_revenue_industry} generates the highest average revenue."
        )

        best_region = (
            df.groupby("Region")
            ["Valuation (M USD)"]
            .mean()
            .idxmax()
        )

        insights.append(
            f"🌍 {best_region} has the highest startup valuation."
        )

    except:
        pass

    return insights
