import streamlit as st
import pandas as pd
import kagglehub
from kagglehub import KaggleDatasetAdapter
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Supermart Grocery Sales Dashboard", layout="wide")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    return kagglehub.load_dataset(
        KaggleDatasetAdapter.PANDAS,
        "mohamedharris/supermart-grocery-sales-retail-analytics-dataset",
        "Supermart Grocery Sales - Retail Analytics Dataset.csv"
    )

df = load_data()

# =========================
# HEADER
# =========================
st.title("🛒 Supermart Grocery Sales Dashboard")
st.caption("Retail Analytics Dashboard")

# =========================
# SIDEBAR - FILTER KOTA
# =========================
st.sidebar.header("📍 Filter Kota")

select_all_city = st.sidebar.checkbox("Pilih Semua Kota", value=True)

if select_all_city:
    city_selected = st.sidebar.multiselect(
        "Pilih Kota",
        options=df["City"].unique(),
        default=df["City"].unique()
    )
else:
    city_selected = st.sidebar.multiselect(
        "Pilih Kota",
        options=df["City"].unique()
    )

# =========================
# SIDEBAR - FILTER KATEGORI
# =========================
st.sidebar.header("📦 Filter Kategori")

category_selected = st.sidebar.multiselect(
    "Pilih Kategori",
    df["Category"].unique(),
    df["Category"].unique()
)

# =========================
# FILTER DATA
# =========================
filtered_df = df[
    (df["City"].isin(city_selected)) &
    (df["Category"].isin(category_selected))
]

# =========================
# INFO KOTA (FITUR BARU)
# =========================
st.subheader("📍 Informasi Kota Terpilih")

city_info = (
    filtered_df
    .groupby("City")
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Jumlah_Transaksi=("Sales", "count")
    )
    .reset_index()
)

st.dataframe(city_info, use_container_width=True)

# =========================
# METRICS
# =========================
st.subheader("📊 Ringkasan Utama")

c1, c2, c3 = st.columns(3)
c1.metric("💰 Total Penjualan", f"{filtered_df['Sales'].sum():,.0f}")
c2.metric("💹 Total Profit", f"{filtered_df['Profit'].sum():,.0f}")
c3.metric("🧾 Total Transaksi", len(filtered_df))

# =========================
# CHART: SALES PER KATEGORI
# =========================
st.subheader("📈 Penjualan per Kategori")

fig1, ax1 = plt.subplots()
sns.barplot(
    data=filtered_df,
    x="Category",
    y="Sales",
    estimator=sum,
    ax=ax1
)
plt.xticks(rotation=45)
st.pyplot(fig1)

# =========================
# CHART: PROFIT PER KOTA
# =========================
st.subheader("💰 Profit per Kota")

fig2, ax2 = plt.subplots()
sns.barplot(
    data=filtered_df,
    x="City",
    y="Profit",
    estimator=sum,
    ax=ax2
)
st.pyplot(fig2)

# =========================
# TOP & BOTTOM SUB CATEGORY
# =========================
st.subheader("⭐ Top & Bottom Sub Category")

top_sub = (
    filtered_df.groupby("Sub Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

bottom_sub = (
    filtered_df.groupby("Sub Category")["Sales"]
    .sum()
    .sort_values()
    .head(5)
)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔝 Top 5")
    st.bar_chart(top_sub)

with col2:
    st.markdown("### 🔻 Bottom 5")
    st.bar_chart(bottom_sub)

# =========================
# SALES VS PROFIT
# =========================
st.subheader("📊 Sales vs Profit")

fig3, ax3 = plt.subplots()
sns.scatterplot(
    data=filtered_df,
    x="Sales",
    y="Profit",
    hue="Category",
    ax=ax3
)
st.pyplot(fig3)

# =========================
# INSIGHT OTOMATIS
# =========================
st.subheader("🧠 Insight Otomatis")

best_city = city_info.sort_values("Total_Sales", ascending=False).iloc[0]
worst_city = city_info.sort_values("Total_Profit").iloc[0]

st.success(
    f"""
    📌 Kota dengan penjualan tertinggi adalah **{best_city['City']}**  
    dengan total penjualan **{best_city['Total_Sales']:,.0f}**.
    
    ⚠️ Kota dengan profit terendah adalah **{worst_city['City']}**  
    sehingga perlu evaluasi strategi penjualan.
    """
)

st.markdown("---")
st.caption("📌 Streamlit Dashboard | Supermart Grocery Sales Dataset")