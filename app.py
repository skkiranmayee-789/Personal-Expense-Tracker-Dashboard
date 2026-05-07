import streamlit as st
import plotly.express as px

from src.data_loader import load_data
from src.analyzer import analyze_expenses

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Expense Tracker Dashboard",
    layout="wide"
)

# =========================================
# CUSTOM CSS
# =========================================

st.markdown("""
<style>

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 1rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

[data-testid="metric-container"] {
    background-color: #111827;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #374151;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# LOAD DATA
# =========================================

df = load_data("data/expenses.csv")

# =========================================
# SIDEBAR FILTERS
# =========================================

st.sidebar.title("🔍 Filters")

selected_month = st.sidebar.multiselect(
    "Select Month",
    options=df["Month"].unique(),
    default=df["Month"].unique()
)

selected_category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

selected_payment = st.sidebar.multiselect(
    "Select Payment Method",
    options=df["Payment_Method"].unique(),
    default=df["Payment_Method"].unique()
)

# =========================================
# FILTER DATA
# =========================================

filtered_df = df[
    (df["Month"].isin(selected_month)) &
    (df["Category"].isin(selected_category)) &
    (df["Payment_Method"].isin(selected_payment))
]

# =========================================
# ANALYZE DATA
# =========================================

results = analyze_expenses(filtered_df)

highest_category = (
    results["category_analysis"]
    .idxmax()
)

# =========================================
# TITLE
# =========================================

st.title("💰 Personal Expense Tracker Dashboard")

st.markdown("---")

# =========================================
# KPI CARDS
# =========================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "💸 Total Spending",
        f"₹{results['total_spending']}"
    )

with col2:
    st.metric(
        "📊 Average Spending",
        f"₹{results['average_daily']:.2f}"
    )

with col3:
    st.metric(
        "🏆 Highest Category",
        highest_category
    )

st.markdown("---")

# =========================================
# DATASET
# =========================================

with st.expander("📄 View Expense Dataset"):

    st.dataframe(
        filtered_df.reset_index(drop=True),
        use_container_width=True
    )

# =========================================
# CHART ROW 1
# =========================================

col4, col5 = st.columns(2)

# -----------------------------------------
# CATEGORY BAR CHART
# -----------------------------------------

with col4:

    st.subheader("📊 Category-wise Spending")

    category_df = (
        results["category_analysis"]
        .reset_index()
    )

    category_df.columns = [
        "Category",
        "Amount"
    ]

    fig1 = px.bar(
        category_df,
        x="Category",
        y="Amount",
        height=280,
        template="plotly_dark"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

# -----------------------------------------
# PAYMENT PIE CHART
# -----------------------------------------

with col5:

    st.subheader("💳 Payment Distribution")

    payment_df = (
        results["payment_analysis"]
        .reset_index()
    )

    payment_df.columns = [
        "Payment Method",
        "Amount"
    ]

    fig2 = px.pie(
        payment_df,
        names="Payment Method",
        values="Amount",
        height=280,
        template="plotly_dark"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# =========================================
# CHART ROW 2
# =========================================

col6, col7 = st.columns(2)

# -----------------------------------------
# MONTHLY TREND
# -----------------------------------------

with col6:

    st.subheader("📈 Monthly Spending")

    monthly_df = (
        results["monthly_analysis"]
        .reset_index()
    )

    monthly_df = monthly_df[
        monthly_df["Amount"] > 0
    ]

    monthly_df.columns = [
        "Month",
        "Amount"
    ]

    fig3 = px.line(
        monthly_df,
        x="Month",
        y="Amount",
        markers=True,
        height=280,
        template="plotly_dark"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

# -----------------------------------------
# DAILY TREND
# -----------------------------------------

with col7:

    st.subheader("📅 Daily Spending")

    daily_df = (
        results["daily_analysis"]
        .reset_index()
    )

    daily_df.columns = [
        "Date",
        "Amount"
    ]

    fig4 = px.line(
        daily_df,
        x="Date",
        y="Amount",
        markers=True,
        height=280,
        template="plotly_dark"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

# =========================================
# INSIGHTS
# =========================================

st.markdown("---")

st.subheader("🧠 Financial Insights")

col8, col9, col10 = st.columns(3)

with col8:
    st.success(
        f"Highest spending area:\n\n{highest_category}"
    )

with col9:
    st.info(
        "Digital payments dominate transactions."
    )

with col10:
    st.warning(
        "Monthly analysis helps track overspending."
    )

# =========================================
# FOOTER
# =========================================

st.markdown("---")

st.caption(
    "Built using Python, Pandas, Plotly, and Streamlit"
)