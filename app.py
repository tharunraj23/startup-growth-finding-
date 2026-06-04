import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="Startup Analytics Dashboard",
    page_icon="🚀",
    layout="wide"
)

# -------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

h1,h2,h3 {
    color: #00E5FF;
}

.metric-card {
    background-color:#1E293B;
    padding:20px;
    border-radius:15px;
}

[data-testid="stMetricValue"]{
    font-size:28px;
    color:#00E5FF;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("data/startup_data.csv")
    return df

df = load_data()

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/5968/5968350.png",
    width=120
)

st.sidebar.title("🚀 Startup Analytics")

industry_filter = st.sidebar.multiselect(
    "Select Industry",
    options=df["Industry"].unique(),
    default=df["Industry"].unique()
)

region_filter = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

filtered_df = df[
    (df["Industry"].isin(industry_filter)) &
    (df["Region"].isin(region_filter))
]

# -------------------------------------------------
# TITLE
# -------------------------------------------------

st.title("🚀 Startup Analytics & Intelligence Dashboard")

st.markdown("""
Comprehensive Startup Analytics Platform with
deep business insights and machine learning.
""")

# -------------------------------------------------
# KPI SECTION
# -------------------------------------------------

total_startups = len(filtered_df)

total_funding = filtered_df["Funding Amount (M USD)"].sum()

total_revenue = filtered_df["Revenue (M USD)"].sum()

avg_valuation = filtered_df["Valuation (M USD)"].mean()

profit_rate = (
    filtered_df["Profitable"].mean() * 100
)

col1,col2,col3,col4,col5 = st.columns(5)

col1.metric(
    "Startups",
    f"{total_startups:,}"
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

col5.metric(
    "Profitability",
    f"{profit_rate:.1f}%"
)

st.divider()

# -------------------------------------------------
# FUNDING BY INDUSTRY
# -------------------------------------------------

st.subheader("💰 Industry Funding Analysis")

industry_funding = (
    filtered_df.groupby("Industry")
    ["Funding Amount (M USD)"]
    .sum()
    .reset_index()
)

fig1 = px.bar(
    industry_funding,
    x="Industry",
    y="Funding Amount (M USD)",
    color="Industry",
    text_auto=True
)

st.plotly_chart(fig1, use_container_width=True)

# -------------------------------------------------
# REGION DISTRIBUTION
# -------------------------------------------------

col1,col2 = st.columns(2)

with col1:

    st.subheader("🌎 Startup Distribution")

    region_count = (
        filtered_df["Region"]
        .value_counts()
        .reset_index()
    )

    region_count.columns = ["Region","Count"]

    fig2 = px.pie(
        region_count,
        values="Count",
        names="Region",
        hole=0.4
    )

    st.plotly_chart(fig2,
                    use_container_width=True)

with col2:

    st.subheader("🏭 Industry Distribution")

    fig3 = px.treemap(
        filtered_df,
        path=["Industry"],
        values="Revenue (M USD)"
    )

    st.plotly_chart(fig3,
                    use_container_width=True)

# -------------------------------------------------
# FUNDING VS VALUATION
# -------------------------------------------------

st.subheader("📈 Funding vs Valuation")

fig4 = px.scatter(
    filtered_df,
    x="Funding Amount (M USD)",
    y="Valuation (M USD)",
    color="Industry",
    size="Revenue (M USD)",
    hover_name="Startup Name"
)

st.plotly_chart(fig4,
                use_container_width=True)

# -------------------------------------------------
# REVENUE VS EMPLOYEES
# -------------------------------------------------

st.subheader("👨‍💼 Revenue vs Employees")

fig5 = px.scatter(
    filtered_df,
    x="Employees",
    y="Revenue (M USD)",
    color="Industry",
    size="Valuation (M USD)"
)

st.plotly_chart(fig5,
                use_container_width=True)

# -------------------------------------------------
# CORRELATION MATRIX
# -------------------------------------------------

st.subheader("📊 Correlation Analysis")

numeric_df = filtered_df.select_dtypes(
    include=np.number
)

corr = numeric_df.corr()

fig6 = px.imshow(
    corr,
    text_auto=True,
    aspect="auto"
)

st.plotly_chart(fig6,
                use_container_width=True)

# -------------------------------------------------
# TOP 10 VALUED STARTUPS
# -------------------------------------------------

st.subheader("🏆 Top 10 Startups")

top10 = filtered_df.sort_values(
    "Valuation (M USD)",
    ascending=False
).head(10)

fig7 = px.bar(
    top10,
    x="Startup Name",
    y="Valuation (M USD)",
    color="Industry"
)

st.plotly_chart(fig7,
                use_container_width=True)

# -------------------------------------------------
# EXIT STATUS
# -------------------------------------------------

st.subheader("🎯 Exit Status Analysis")

exit_count = (
    filtered_df["Exit Status"]
    .value_counts()
    .reset_index()
)

exit_count.columns = [
    "Exit Status",
    "Count"
]

fig8 = px.pie(
    exit_count,
    values="Count",
    names="Exit Status"
)

st.plotly_chart(fig8,
                use_container_width=True)

# -------------------------------------------------
# MACHINE LEARNING
# -------------------------------------------------

st.subheader("🤖 Profitability Prediction")

try:

    features = [
        "Funding Rounds",
        "Funding Amount (M USD)",
        "Valuation (M USD)",
        "Revenue (M USD)",
        "Employees",
        "Market Share (%)"
    ]

    X = filtered_df[features]

    y = filtered_df["Profitable"]

    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    pred = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        pred
    )

    st.success(
        f"Model Accuracy: {accuracy*100:.2f}%"
    )

    importance = pd.DataFrame({
        "Feature": features,
        "Importance":
        model.feature_importances_
    })

    importance = importance.sort_values(
        "Importance",
        ascending=False
    )

    fig9 = px.bar(
        importance,
        x="Feature",
        y="Importance",
        color="Importance"
    )

    st.plotly_chart(
        fig9,
        use_container_width=True
    )

except Exception as e:
    st.warning(
        f"ML Model Error: {e}"
    )

# -------------------------------------------------
# AI INSIGHTS
# -------------------------------------------------

st.subheader("🧠 AI Generated Insights")

highest_funding_industry = (
    filtered_df.groupby("Industry")
    ["Funding Amount (M USD)"]
    .mean()
    .idxmax()
)

best_region = (
    filtered_df.groupby("Region")
    ["Valuation (M USD)"]
    .mean()
    .idxmax()
)

highest_revenue_industry = (
    filtered_df.groupby("Industry")
    ["Revenue (M USD)"]
    .mean()
    .idxmax()
)

st.success(
    f"🏆 {highest_funding_industry} receives the highest average funding."
)

st.info(
    f"🌎 {best_region} has the highest startup valuation."
)

st.success(
    f"💵 {highest_revenue_industry} generates the highest revenue."
)

# -------------------------------------------------
# RAW DATA
# -------------------------------------------------

with st.expander("📄 View Dataset"):
    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.markdown("---")

st.markdown(
    """
    ### 🚀 Startup Analytics Intelligence System

    Built with:
    - Streamlit
    - Plotly
    - Pandas
    - Machine Learning
    - Business Intelligence

    """
)
