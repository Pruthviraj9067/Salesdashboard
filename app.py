import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Lulu Hypermarket Dashboard", layout="wide")

st.title("🛒 Lulu Hypermarket Dubai - Customer Analytics Dashboard")

@st.cache_data
def load_data():
    return pd.read_csv("lulu_dataset.csv")

df = load_data()

st.sidebar.header("Filters")

segment = st.sidebar.multiselect(
    "Customer Segment",
    options=df["Customer_Segment"].unique(),
    default=df["Customer_Segment"].unique()
)

category = st.sidebar.multiselect(
    "Product Category",
    options=df["Product_Category"].unique(),
    default=df["Product_Category"].unique()
)

df_filtered = df[
    (df["Customer_Segment"].isin(segment)) &
    (df["Product_Category"].isin(category))
]

st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Customers", len(df_filtered))
col2.metric("Total Revenue ($)", round(df_filtered["Purchase_Amount_USD"].sum(), 2))
col3.metric("Avg Purchase ($)", round(df_filtered["Purchase_Amount_USD"].mean(), 2))

st.subheader("📈 Visual Insights")

st.write("### Age Distribution")
fig1 = plt.figure()
df_filtered["Age"].hist(bins=20)
st.pyplot(fig1)

st.write("### Purchase Amount Distribution")
fig2 = plt.figure()
df_filtered["Purchase_Amount_USD"].hist(bins=20)
st.pyplot(fig2)

st.write("### Sales by Product Category")
category_sales = df_filtered.groupby("Product_Category")["Purchase_Amount_USD"].sum()
fig3 = plt.figure()
category_sales.plot(kind="bar")
st.pyplot(fig3)

st.write("### Customer Segment Distribution")
segment_count = df_filtered["Customer_Segment"].value_counts()
fig4 = plt.figure()
segment_count.plot(kind="pie", autopct='%1.1f%%')
plt.ylabel("")
st.pyplot(fig4)

st.subheader("📋 Raw Data")
st.dataframe(df_filtered)

st.download_button(
    label="Download Filtered Data",
    data=df_filtered.to_csv(index=False),
    file_name="filtered_data.csv",
    mime="text/csv"
)
