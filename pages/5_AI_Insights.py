import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Insights",
    page_icon="🧠",
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
# SIDEBAR
# =====================================================

st.sidebar.header("AI Analytics Filters")

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
    (df["Industry"].isin(industry_filter))
    &
    (df["Region"].isin(region_filter))
]

# =====================================================
# TITLE
# =====================================================

st.title("🧠 AI Insights & Predictive Analytics")

st.markdown("""
Advanced Machine Learning and Business Intelligence
for Startup Ecosystem Analysis.
""")

# =====================================================
# PROFITABILITY PREDICTION
# =====================================================

st.header("🤖 Profitability Prediction Model")

features = [
    "Funding Rounds",
    "Funding Amount (M USD)",
    "Valuation (M USD)",
    "Revenue (M USD)",
    "Employees",
    "Market Share (%)"
]

target = "Profitable"

try:

    X = filtered_df[features]
    y = filtered_df[target]

    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42
        )
    )

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    st.success(
        f"Model Accuracy: {accuracy*100:.2f}%"
    )

except Exception as e:
    st.error(str(e))

# =====================================================
# FEATURE IMPORTANCE
# =====================================================

st.subheader("📊 Key Drivers of Profitability")

importance_df = pd.DataFrame({
    "Feature": features,
    "Importance":
    model.feature_importances_
})

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)

fig = px.bar(
    importance_df,
    x="Feature",
    y="Importance",
    color="Importance",
    text_auto=".3f"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# STARTUP CLUSTERING
# =====================================================

st.header("🎯 Startup Segmentation")

cluster_features = [
    "Funding Amount (M USD)",
    "Revenue (M USD)",
    "Valuation (M USD)",
    "Employees"
]

cluster_data = filtered_df[
    cluster_features
].copy()

scaler = StandardScaler()

scaled_data = scaler.fit_transform(
    cluster_data
)

kmeans = KMeans(
    n_clusters=3,
    random_state=42,
    n_init=10
)

filtered_df["Cluster"] = (
    kmeans.fit_predict(scaled_data)
)

cluster_names = {
    0: "Emerging",
    1: "Growth",
    2: "Enterprise"
}

filtered_df["Cluster Name"] = (
    filtered_df["Cluster"]
    .map(cluster_names)
)

fig = px.scatter(
    filtered_df,
    x="Funding Amount (M USD)",
    y="Valuation (M USD)",
    color="Cluster Name",
    size="Revenue (M USD)",
    hover_name="Startup Name"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# GROWTH SCORE
# =====================================================

st.header("🚀 Growth Potential Score")

filtered_df["Growth Score"] = (
    filtered_df["Funding Amount (M USD)"] * 0.30 +
    filtered_df["Revenue (M USD)"] * 0.30 +
    filtered_df["Valuation (M USD)"] * 0.30 +
    filtered_df["Market Share (%)"] * 0.10
)

top_growth = (
    filtered_df.sort_values(
        "Growth Score",
        ascending=False
    )
    .head(15)
)

fig = px.bar(
    top_growth,
    x="Startup Name",
    y="Growth Score",
    color="Industry"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# RISK ANALYSIS
# =====================================================

st.header("⚠ Startup Risk Analysis")

filtered_df["Risk Score"] = (
    filtered_df["Funding Amount (M USD)"] /
    (
        filtered_df["Revenue (M USD)"] + 1
    )
)

risk_df = (
    filtered_df.sort_values(
        "Risk Score",
        ascending=False
    )
    .head(15)
)

fig = px.bar(
    risk_df,
    x="Startup Name",
    y="Risk Score",
    color="Industry"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# INDUSTRY AI INSIGHTS
# =====================================================

st.header("🏭 AI Industry Insights")

industry_summary = (
    filtered_df.groupby("Industry")
    .agg({
        "Funding Amount (M USD)": "mean",
        "Revenue (M USD)": "mean",
        "Valuation (M USD)": "mean",
        "Growth Score": "mean"
    })
    .round(2)
)

st.dataframe(
    industry_summary,
    use_container_width=True
)

# =====================================================
# REGION AI INSIGHTS
# =====================================================

st.header("🌎 AI Regional Insights")

region_summary = (
    filtered_df.groupby("Region")
    .agg({
        "Funding Amount (M USD)": "mean",
        "Revenue (M USD)": "mean",
        "Valuation (M USD)": "mean",
        "Growth Score": "mean"
    })
    .round(2)
)

st.dataframe(
    region_summary,
    use_container_width=True
)

# =====================================================
# EXECUTIVE RECOMMENDATIONS
# =====================================================

st.header("📋 Executive Recommendations")

top_industry = (
    industry_summary["Growth Score"]
    .idxmax()
)

top_region = (
    region_summary["Growth Score"]
    .idxmax()
)

best_startup = (
    filtered_df.sort_values(
        "Growth Score",
        ascending=False
    )
    .iloc[0]["Startup Name"]
)

st.success(
    f"🏆 Highest Growth Industry: {top_industry}"
)

st.success(
    f"🌍 Best Performing Region: {top_region}"
)

st.success(
    f"🚀 Most Promising Startup: {best_startup}"
)

# =====================================================
# AUTOMATED INSIGHTS
# =====================================================

st.header("💡 Automated AI Insights")

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

highest_valuation_region = (
    filtered_df.groupby("Region")
    ["Valuation (M USD)"]
    .mean()
    .idxmax()
)

st.info(
    f"💰 {highest_funding_industry} receives the highest average funding."
)

st.info(
    f"📈 {highest_revenue_industry} generates the highest average revenue."
)

st.info(
    f"🏢 {highest_valuation_region} shows the highest average valuation."
)

# =====================================================
# TOP GROWTH STARTUPS TABLE
# =====================================================

st.header("🏆 Top Growth Startups")

display_columns = [
    "Startup Name",
    "Industry",
    "Region",
    "Funding Amount (M USD)",
    "Revenue (M USD)",
    "Valuation (M USD)",
    "Growth Score"
]

st.dataframe(
    top_growth[display_columns],
    use_container_width=True
)

# =====================================================
# DATA PREVIEW
# =====================================================

with st.expander("📄 View Full Dataset"):
    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.markdown("""
### AI Analytics Engine

Features Included:

✔ Profitability Prediction

✔ Startup Segmentation

✔ Growth Potential Analysis

✔ Risk Assessment

✔ Industry Intelligence

✔ Regional Intelligence

✔ Automated Recommendations

✔ Executive Decision Support

Built using:

- Python
- Streamlit
- Scikit-Learn
- Pandas
- Plotly
- Machine Learning
""")
