import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------

st.set_page_config(
    page_title="Superstore Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# -------------------------------------------------
# LOAD DATASET
# -------------------------------------------------

df = pd.read_csv("train.csv")

# Convert Order Date to datetime
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")

# -------------------------------------------------
# TITLE
# -------------------------------------------------

st.title("📊 Superstore Sales Analysis Dashboard")
st.write(
    "Interactive dashboard for exploring sales performance "
    "across categories, regions, customers and locations."
)

# -------------------------------------------------
# SIDEBAR FILTERS
# -------------------------------------------------

st.sidebar.header("🔎 Filters")

category_options = df["Category"].dropna().unique()
selected_category = st.sidebar.multiselect(
    "Select Category",
    category_options,
    default=list(category_options)
)

region_options = df["Region"].dropna().unique()
selected_region = st.sidebar.multiselect(
    "Select Region",
    region_options,
    default=list(region_options)
)

segment_options = df["Segment"].dropna().unique()
selected_segment = st.sidebar.multiselect(
    "Select Segment",
    segment_options,
    default=list(segment_options)
)

# -------------------------------------------------
# FILTER DATA
# -------------------------------------------------

filtered_df = df[
    (df["Category"].isin(selected_category)) &
    (df["Region"].isin(selected_region)) &
    (df["Segment"].isin(selected_segment))
].copy()

# -------------------------------------------------
# SUMMARY METRICS
# -------------------------------------------------

total_sales = filtered_df["Sales"].sum()
total_orders = filtered_df["Order ID"].nunique()
total_customers = filtered_df["Customer ID"].nunique()

col1, col2, col3 = st.columns(3)

col1.metric(
    "💰 Total Sales",
    f"${total_sales:,.2f}"
)

col2.metric(
    "🛒 Total Orders",
    f"{total_orders:,}"
)

col3.metric(
    "👥 Total Customers",
    f"{total_customers:,}"
)

st.divider()

# -------------------------------------------------
# SALES BY CATEGORY
# -------------------------------------------------

st.subheader("📊 Sales by Category")

category_sales = (
    filtered_df.groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(category_sales)

# -------------------------------------------------
# SALES BY REGION
# -------------------------------------------------

st.subheader("🌎 Sales by Region")

region_sales = (
    filtered_df.groupby("Region")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(region_sales)

# -------------------------------------------------
# SALES BY SUB-CATEGORY
# -------------------------------------------------

st.subheader("📦 Sales by Sub-Category")

subcategory_sales = (
    filtered_df.groupby("Sub-Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(subcategory_sales)

# -------------------------------------------------
# SALES BY SEGMENT
# -------------------------------------------------

st.subheader("👥 Sales by Segment")

segment_sales = (
    filtered_df.groupby("Segment")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(segment_sales)

# -------------------------------------------------
# SALES BY SHIP MODE
# -------------------------------------------------

st.subheader("🚚 Sales by Ship Mode")

ship_sales = (
    filtered_df.groupby("Ship Mode")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(ship_sales)

# -------------------------------------------------
# YEAR-WISE SALES TREND
# -------------------------------------------------

st.subheader("📈 Sales Trend by Year")

filtered_df["Year"] = filtered_df["Order Date"].dt.year

year_sales = (
    filtered_df.groupby("Year")["Sales"]
    .sum()
    .sort_index()
)

st.line_chart(year_sales)

# -------------------------------------------------
# TOP 10 STATES
# -------------------------------------------------

st.subheader("🏆 Top 10 States by Sales")

state_sales = (
    filtered_df.groupby("State")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(state_sales)

# -------------------------------------------------
# TOP 10 CITIES
# -------------------------------------------------

st.subheader("🏙️ Top 10 Cities by Sales")

city_sales = (
    filtered_df.groupby("City")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(city_sales)

# -------------------------------------------------
# TOP 10 PRODUCTS
# -------------------------------------------------

st.subheader("🏅 Top 10 Products by Sales")

product_sales = (
    filtered_df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(product_sales)

# -------------------------------------------------
# DATA TABLE
# -------------------------------------------------

st.subheader("📋 Filtered Sales Data")

st.dataframe(
    filtered_df,
    use_container_width=True
)