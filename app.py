import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Lulu Hypermarket Analytics",
    page_icon="🛒",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

.metric-card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
}

h1 {
    color: #0E1117;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("lulu_dataset.csv")
    return df

df = load_data()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Lulu_Hypermarket_logo.svg/2560px-Lulu_Hypermarket_logo.svg.png",
    width=200
)

st.sidebar.title("🔍 Dashboard Filters")

segment_filter = st.sidebar.multiselect(
    "Customer Segment",
    options=df["Customer_Segment"].unique(),
    default=df["Customer_Segment"].unique()
)

category_filter = st.sidebar.multiselect(
    "Product Category",
    options=df["Product_Category"].unique(),
    default=df["Product_Category"].unique()
)

payment_filter = st.sidebar.multiselect(
    "Payment Method",
    options=df["Payment_Method"].unique(),
    default=df["Payment_Method"].unique()
)

# ---------------------------------------------------
# FILTER DATA
# ---------------------------------------------------
filtered_df = df[
    (df["Customer_Segment"].isin(segment_filter)) &
    (df["Product_Category"].isin(category_filter)) &
    (df["Payment_Method"].isin(payment_filter))
]

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
st.title("🛒 Lulu Hypermarket Dubai Dashboard")
st.markdown("### Customer Insights • Sales Analytics • Retail Intelligence")

# ---------------------------------------------------
# KPI METRICS
# ---------------------------------------------------
total_sales = filtered_df["Purchase_Amount_USD"].sum()
avg_sales = filtered_df["Purchase_Amount_USD"].mean()
total_customers = filtered_df["Customer_ID"].nunique()
avg_visits = filtered_df["Visit_Frequency"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Revenue", f"${total_sales:,.2f}")
col2.metric("🧑 Customers", total_customers)
col3.metric("🛍 Avg Purchase", f"${avg_sales:.2f}")
col4.metric("🔁 Avg Visits", f"{avg_visits:.1f}")

st.markdown("---")

# ---------------------------------------------------
# CHARTS ROW 1
# ---------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📦 Sales by Product Category")

    category_sales = filtered_df.groupby(
        "Product_Category"
    )["Purchase_Amount_USD"].sum().reset_index()

    fig_bar = px.bar(
        category_sales,
        x="Product_Category",
        y="Purchase_Amount_USD",
        color="Product_Category",
        text_auto=True
    )

    fig_bar.update_layout(
        template="plotly_white",
        height=450
    )

    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.subheader("👥 Customer Segment Distribution")

    segment_count = filtered_df["Customer_Segment"].value_counts().reset_index()
    segment_count.columns = ["Segment", "Count"]

    fig_pie = px.pie(
        segment_count,
        names="Segment",
        values="Count",
        hole=0.5
    )

    fig_pie.update_layout(height=450)

    st.plotly_chart(fig_pie, use_container_width=True)

# ---------------------------------------------------
# CHARTS ROW 2
# ---------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Purchase Amount Distribution")

    fig_hist = px.histogram(
        filtered_df,
        x="Purchase_Amount_USD",
        nbins=30
    )

    fig_hist.update_layout(
        template="plotly_white",
        height=450
    )

    st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    st.subheader("🧠 Age vs Purchase Amount")

    fig_scatter = px.scatter(
        filtered_df,
        x="Age",
        y="Purchase_Amount_USD",
        color="Customer_Segment",
        size="Quantity",
        hover_data=["Customer_Name"]
    )

    fig_scatter.update_layout(
        template="plotly_white",
        height=450
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

# ---------------------------------------------------
# LINE CHART
# ---------------------------------------------------
st.subheader("📊 Average Spending by Visit Frequency")

visit_analysis = filtered_df.groupby(
    "Visit_Frequency"
)["Purchase_Amount_USD"].mean().reset_index()

fig_line = px.line(
    visit_analysis,
    x="Visit_Frequency",
    y="Purchase_Amount_USD",
    markers=True
)

fig_line.update_layout(
    template="plotly_white",
    height=500
)

st.plotly_chart(fig_line, use_container_width=True)

# ---------------------------------------------------
# DATA TABLE
# ---------------------------------------------------
st.subheader("📋 Customer Dataset")

st.dataframe(filtered_df, use_container_width=True)

# ---------------------------------------------------
# DOWNLOAD BUTTON
# ---------------------------------------------------
csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="⬇ Download Filtered Data",
    data=csv,
    file_name='filtered_lulu_data.csv',
    mime='text/csv'
)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("---")
st.markdown(
    "Made with ❤️ using Streamlit | Lulu Hypermarket Analytics Dashboard"
)
