import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Page Config
st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("📊 Interactive Sales & Performance Dashboard")

# 1. Generate Sample Data (Replace this with pd.read_csv("your_data.csv"))
@st.cache_data
def load_data():
    np.random.seed(42)
    dates = pd.date_range("2026-01-01", periods=100)
    df = pd.DataFrame({
        "Date": dates,
        "Region": np.random.choice(["North", "South", "East", "West"], 100),
        "Product": np.random.choice(["Laptop", "Tablet", "Phone"], 100),
        "Sales": np.random.randint(200, 2000, 100),
        "Profit": np.random.randint(50, 600, 100)
    })
    return df

df = load_data()

# 2. Sidebar Filters
st.sidebar.header("Filter Data")
selected_region = st.sidebar.multiselect(
    "Select Region:", options=df["Region"].unique(), default=df["Region"].unique()
)
selected_product = st.sidebar.multiselect(
    "Select Product:", options=df["Product"].unique(), default=df["Product"].unique()
)

filtered_df = df[(df["Region"].isin(selected_region)) & (df["Product"].isin(selected_product))]

# 3. KPI Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${filtered_df['Sales'].sum():,}")
col2.metric("Total Profit", f"${filtered_df['Profit'].sum():,}")
col3.metric("Total Orders", len(filtered_df))

st.markdown("---")

# 4. Interactive Charts
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Sales Over Time")
    fig_line = px.line(filtered_df, x="Date", y="Sales", color="Region")
    st.plotly_chart(fig_line, use_container_width=True)

with chart_col2:
    st.subheader("Profit by Product")
    fig_bar = px.bar(filtered_df, x="Product", y="Profit", color="Product", barmode="group")
    st.plotly_chart(fig_bar, use_container_width=True)

# 5. Raw Data Table
with st.expander("View Filtered Data Table"):
    st.dataframe(filtered_df)