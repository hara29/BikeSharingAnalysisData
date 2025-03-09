import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Helper function untuk menyiapkan berbagai DataFrame
def create_monthly_trend(df):
    monthly_trend_df = df.resample(rule='ME', on='date').agg({"count_rental": "sum", "casual": "sum", "registered": "sum"})
    monthly_trend_df.index = monthly_trend_df.index.strftime('%b %Y')
    monthly_trend_df = monthly_trend_df.reset_index()
    monthly_trend_df.rename(columns={"count_rental": "Total peminjaman", "date": "Bulan"}, inplace=True)
    return monthly_trend_df

def create_seasonal_trend(df):
    return df.groupby('season', observed=True)['count_rental'].sum().reset_index()

def create_clustered_hourly_data(df):
    df['Cluster'] = pd.qcut(df['count_rental'], q=3, labels=['Low', 'Medium', 'High'])
    return df

def create_weekly_rental_trend(df):
    weekly_trend = df.groupby('weekday', observed=False).agg({'casual': 'sum', 'registered': 'sum'}).reset_index()
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekly_trend['weekday'] = pd.Categorical(weekly_trend['weekday'], categories=weekday_order, ordered=True)
    return weekly_trend.sort_values('weekday')

def create_hourly_rental_trend(df):
    hour_trend = df.groupby('hour', observed=False).agg({'casual': 'sum', 'registered': 'sum'}).reset_index()
    return hour_trend

# Load data
day_df = pd.read_csv("dashboard/day_final.csv")
hour_df = pd.read_csv("dashboard/hour_final.csv")

for df in [day_df, hour_df]:
    df.sort_values(by="date", inplace=True)
    df.reset_index(drop=True, inplace=True)
    df["date"] = pd.to_datetime(df["date"])

# Sidebar untuk filter tanggal
with st.sidebar:
    st.image(
        "https://img.freepik.com/free-vector/commuting-by-bike-concept-illustration_114360-15164.jpg?w=1480",
        width=230
    )
    
    min_date = day_df["date"].min()
    max_date = day_df["date"].max()
    
    start_date, end_date = st.date_input(
        label="Rentang Waktu", 
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
# Konversi start_date dan end_date ke Timestamp
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter data berdasarkan tanggal yang dipilih
main_df_day = day_df[(day_df["date"] >= start_date) & (day_df["date"] <= end_date)]
main_df_hour = hour_df[(hour_df["date"] >= start_date) & (hour_df["date"] <= end_date)]

# Menyiapkan berbagai dataframe
monthly_data = create_monthly_trend(main_df_day)
seasonal_data = create_seasonal_trend(main_df_day)
clustering = create_clustered_hourly_data(main_df_hour)
weekly_rental_data = create_weekly_rental_trend(main_df_day)
hourly_rental_data = create_hourly_rental_trend(main_df_hour)

# Menyiapkan palette warna
set2_palette = sns.color_palette("Set2")

# Menampilkan visualisasi performa perusahaan per bulan
st.header('Rental Bike Dashboard :bike:')
st.subheader("Performa Perusahaan Tiap Bulan")

col1, col2, col3 = st.columns(3)
with col1:
    total_rental = monthly_data["Total peminjaman"].sum() if not monthly_data.empty else 0
    st.metric("Total peminjaman", value=total_rental)
with col2:
    total_rental = monthly_data["registered"].sum() if not monthly_data.empty else 0
    st.metric("Terdaftar", value=total_rental)
with col3:
    total_rental = monthly_data["casual"].sum() if not monthly_data.empty else 0
    st.metric("Kasual", value=total_rental)

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(monthly_data['Bulan'], monthly_data['Total peminjaman'], marker='o', color=set2_palette[1])
ax.set_xlabel("Bulan", fontsize=12)
ax.set_ylabel("Jumlah Penyewa", fontsize=12)
ax.tick_params(axis='x', rotation=45, labelsize=10)
ax.grid(axis='x', linestyle='--', alpha=0.5)
st.pyplot(fig)

# Menampilkan visualisasi peminjaman antar musim
st.subheader("Perbandingan Total Penyewa Antar Musim")
fig, ax = plt.subplots(figsize=(8, 5))
max_value = seasonal_data['count_rental'].max()
colors = [set2_palette[1] if val == max_value else set2_palette[2] for val in seasonal_data['count_rental']]
sns.barplot(x='season', y='count_rental', data=seasonal_data, palette=colors, ax=ax)
ax.set_xlabel("Musim", fontsize=12)
ax.set_ylabel("Total Penyewa", fontsize=12)
ax.set_title("Total peminjaman Sepeda Berdasarkan Musim", fontsize=14)
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}"))
st.pyplot(fig)

# Menampilkan visualisasi hubungan suhu, kelembapan, dan kecebapan angin terhadap peminjaman
st.subheader("Pengaruh Kondisi Lingkungan Terhadap peminjaman")
col1, col2, col3 = st.columns(3)
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
sns.regplot(x="temp", y="count_rental", data=main_df_day, scatter_kws={'alpha':0.5}, ax=axes[0], color=set2_palette[0])
sns.regplot(x="humidity", y="count_rental", data=main_df_day, scatter_kws={'alpha':0.5}, ax=axes[1], color=set2_palette[1])
sns.regplot(x="windspeed", y="count_rental", data=main_df_day, scatter_kws={'alpha':0.5}, ax=axes[2], color=set2_palette[2])
st.pyplot(fig)
with st.expander("Penjelasan Korelasi"):
    st.write("Suhu memiliki korelasi positif terhadap jumlah penyewa. Kelembapan dan kecepatan angin memiliki korelasi negatif yang lemah terhadap jumlah penyewa.")

# Menampilkan visualisasi penyewa terdaftar vs kasual
st.subheader("Pola Pengguna Terdaftar dan Pengguna Kasual")
tabs = st.tabs(["Pola peminjaman Sepeda per Hari", "Pola peminjaman Sepeda per Jam"])

with tabs[0]:
    st.subheader("Pola peminjaman Sepeda per Hari")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(weekly_rental_data['weekday'], weekly_rental_data['casual'], marker='o', linestyle='-', color=set2_palette[1], label='Casual')
    ax.plot(weekly_rental_data['weekday'], weekly_rental_data['registered'], marker='o', linestyle='-', color=set2_palette[2], label='Registered')
    ax.set_xlabel("Hari dalam Seminggu", fontsize=12)
    ax.set_ylabel("Jumlah Penyewa", fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.legend()
    st.pyplot(fig)

with tabs[1]:
    st.subheader("Pola peminjaman Sepeda per Jam")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(hourly_rental_data['hour'], hourly_rental_data['casual'], marker='o', linestyle='-', color=set2_palette[1], label='Casual')
    ax.plot(hourly_rental_data['hour'], hourly_rental_data['registered'], marker='o', linestyle='-', color=set2_palette[2], label='Registered')
    ax.set_xlabel("Jam dalam Sehari")
    ax.set_ylabel("Jumlah peminjaman")
    ax.legend()
    st.pyplot(fig)

# Menampilkan visualisasi peminjaman antar musim
st.subheader("Segmentasi Jumlah peminjaman Sepeda dengan Binning")
cluster_colors = {'Low': '#1f77b4', 'Medium': '#ff7f0e', 'High': '#d62728'}
fig, ax = plt.subplots(figsize=(12, 5))
sns.barplot(x='hour', y='count_rental', hue='Cluster', data=clustering, palette=cluster_colors, ax=ax)
ax.set_xlabel("Jam dalam Sehari")
ax.set_ylabel("Jumlah peminjaman")
ax.legend(title="Cluster")
st.pyplot(fig)

st.caption('Copyright (c) Cindy@LaskarAi 2024')