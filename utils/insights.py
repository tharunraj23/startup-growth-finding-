import pandas as pd
import numpy as np

# ==================================================
# EXECUTIVE INSIGHTS
# ==================================================

def generate_executive_insights(df):

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

        top_region = (
            df.groupby("Region")
            ["Valuation (M USD)"]
            .mean()
            .idxmax()
        )

        insights.append(
            f"🌎 {top_region} has the highest average startup valuation."
        )

        profitability = (
            df["Profitable"]
            .mean() * 100
        )

        insights.append(
            f"✅ Overall profitability rate is {profitability:.1f}%."
        )

    except Exception:
        pass

    return insights


# ==================================================
# INDUSTRY INSIGHTS
# ==================================================

def generate_industry_insights(df):

    insights = []

    try:

        funding = (
            df.groupby("Industry")
            ["Funding Amount (M USD)"]
            .sum()
            .sort_values(
                ascending=False
            )
        )

        revenue = (
            df.groupby("Industry")
            ["Revenue (M USD)"]
            .sum()
            .sort_values(
                ascending=False
            )
        )

        insights.append(
            f"🏭 {funding.index[0]} attracts the highest total funding."
        )

        insights.append(
            f"📈 {revenue.index[0]} generates the highest total revenue."
        )

    except Exception:
        pass

    return insights


# ==================================================
# REGIONAL INSIGHTS
# ==================================================

def generate_regional_insights(df):

    insights = []

    try:

        region_funding = (
            df.groupby("Region")
            ["Funding Amount (M USD)"]
            .sum()
            .idxmax()
        )

        region_revenue = (
            df.groupby("Region")
            ["Revenue (M USD)"]
            .sum()
            .idxmax()
        )

        insights.append(
            f"🌍 {region_funding} is the leading investment region."
        )

        insights.append(
            f"💰 {region_revenue} produces the highest startup revenue."
        )

    except Exception:
        pass

    return insights


# ==================================================
# GROWTH SCORE
# ==================================================

def calculate_growth_score(df):

    temp = df.copy()

    temp["Growth Score"] = (
        temp["Funding Amount (M USD)"] * 0.30 +
        temp["Revenue (M USD)"] * 0.30 +
        temp["Valuation (M USD)"] * 0.30 +
        temp["Market Share (%)"] * 0.10
    )

    return temp


# ==================================================
# RISK SCORE
# ==================================================

def calculate_risk_score(df):

    temp = df.copy()

    temp["Risk Score"] = (
        temp["Funding Amount (M USD)"] /
        (temp["Revenue (M USD)"] + 1)
    )

    return temp


# ==================================================
# TOP GROWTH STARTUPS
# ==================================================

def top_growth_startups(df, top_n=10):

    temp = calculate_growth_score(df)

    return (
        temp.sort_values(
            "Growth Score",
            ascending=False
        )
        .head(top_n)
    )


# ==================================================
# HIGH RISK STARTUPS
# ==================================================

def high_risk_startups(df, top_n=10):

    temp = calculate_risk_score(df)

    return (
        temp.sort_values(
            "Risk Score",
            ascending=False
        )
        .head(top_n)
    )


# ==================================================
# INVESTMENT RECOMMENDATION
# ==================================================

def investment_recommendation(df):

    temp = calculate_growth_score(df)

    best = (
        temp.sort_values(
            "Growth Score",
            ascending=False
        )
        .iloc[0]
    )

    return (
        f"🚀 Recommended investment opportunity: "
        f"{best['Startup Name']} "
        f"({best['Industry']}) "
        f"with Growth Score "
        f"{best['Growth Score']:.2f}"
    )


# ==================================================
# PROFITABILITY INSIGHTS
# ==================================================

def profitability_insights(df):

    insights = []

    try:

        profitable = (
            df[df["Profitable"] == True]
        )

        avg_val = profitable[
            "Valuation (M USD)"
        ].mean()

        insights.append(
            f"💹 Profitable startups average valuation is "
            f"${avg_val:,.2f}M."
        )

    except Exception:
        pass

    return insights


# ==================================================
# MARKET LEADERS
# ==================================================

def market_leaders(df, top_n=5):

    return (
        df.sort_values(
            "Market Share (%)",
            ascending=False
        )
        [
            [
                "Startup Name",
                "Industry",
                "Region",
                "Market Share (%)"
            ]
        ]
        .head(top_n)
    )


# ==================================================
# AUTOMATED EXECUTIVE SUMMARY
# ==================================================

def executive_summary(df):

    try:

        total_startups = len(df)

        total_funding = df[
            "Funding Amount (M USD)"
        ].sum()

        total_revenue = df[
            "Revenue (M USD)"
        ].sum()

        avg_valuation = df[
            "Valuation (M USD)"
        ].mean()

        summary = f"""
Startup Ecosystem Summary

• Total Startups: {total_startups}

• Total Funding: ${total_funding:,.0f}M

• Total Revenue: ${total_revenue:,.0f}M

• Average Valuation: ${avg_valuation:,.0f}M

The ecosystem demonstrates strong investment activity,
steady revenue generation, and promising valuation growth.
"""

        return summary

    except Exception:

        return "Summary unavailable."


# ==================================================
# AI RECOMMENDATIONS
# ==================================================

def ai_recommendations(df):

    recommendations = []

    try:

        best_industry = (
            df.groupby("Industry")
            ["Revenue (M USD)"]
            .mean()
            .idxmax()
        )

        recommendations.append(
            f"📈 Focus future investments on {best_industry}."
        )

        best_region = (
            df.groupby("Region")
            ["Valuation (M USD)"]
            .mean()
            .idxmax()
        )

        recommendations.append(
            f"🌍 Expand operations in {best_region}."
        )

        recommendations.append(
            "🤖 Prioritize startups with high revenue-to-funding ratios."
        )

        recommendations.append(
            "🚀 Monitor emerging startups with rapidly growing market share."
        )

    except Exception:
        pass

    return recommendations
