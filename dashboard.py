import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style
sns.set(style='darkgrid')

# Load data
hours_df = pd.read_csv("hour_clean.csv")

# Convert 'date' column to datetime and extract 'month' and 'year'
hours_df['date'] = pd.to_datetime(hours_df['date'])
hours_df['month'] = hours_df['date'].dt.month
hours_df['year'] = hours_df['date'].dt.year

# Sidebar for selecting options
st.sidebar.header("Pilih Opsi:")
selected_year = st.sidebar.selectbox('Pilih Tahun:', hours_df['year'].unique())

# Filter data based on selected year
filtered_data = hours_df[hours_df['year'] == selected_year]

# Line chart for bike usage trend
plt.figure(figsize=(12, 6))
for season in filtered_data['season'].unique():
    season_data = filtered_data[filtered_data['season'] == season]
    plt.plot(season_data['month'], season_data['count'], label=season, marker='o')

plt.xlabel('Bulan')
plt.ylabel('Jumlah Pengguna')
plt.title(f'Penggunaan Sepeda per Bulan Tahun {selected_year} berdasarkan Musim')
plt.legend()
plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
st.pyplot()

# Bar chart for seasonal pattern
seasonal_pattern = filtered_data.groupby('season')['count'].mean()
seasonal_pattern.index = ['Spring', 'Summer', 'Fall', 'Winter']
st.bar_chart(seasonal_pattern)
st.header('Pola Musiman dalam Penggunaan Sepeda')
st.write('Musim')
st.write('Jumlah Rata-rata Sepeda')

# Display data table
st.header("Tabel Data")
st.write(filtered_data)

# Display heatmap for hourly usage
st.header("Peta Panas Penggunaan Sepeda per Jam")
hourly_usage = filtered_data.pivot_table(values='count', index='season', columns='hour')
fig, ax = plt.subplots()
sns.heatmap(hourly_usage, cmap='YlGnBu', ax=ax)
st.pyplot(fig)
