import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns 
import streamlit as st 
from babel.numbers import format_currency 
sns.set_theme(style='dark')

def create_weather_ride_df(df):
    weather_ride_df = df.groupby(by=["weather_situation", "temp"]).agg({
    "count" : "sum"
    })
    weather_ride_df = weather_ride_df.reset_index()

    weather_ride_df.rename(columns={
        "weather_situation": "weather",
        "temp" : "temperature"
    }, inplace=True)
    return weather_ride_df
    


def create_daily_ride_df(df):
    bike_df = df[['work_day', 'casual', 'registered']] 
    daily_ride_df = pd.melt(bike_df, id_vars='work_day', var_name='user status', value_name='count' )
    daily_ride_df = daily_ride_df.reset_index()
    return daily_ride_df

# Load data csv
all_df = pd.read_csv("main_data.csv")

# Mengurutkan dataframe berdasarkan date dan memastikan tipenya datatime
datetime_columns = ["date"]
all_df.sort_values(by="date", inplace=True)
all_df.reset_index(inplace=True)

for columns in datetime_columns:
    all_df[columns] = pd.to_datetime(all_df[columns])
    
## Membuat komponen filter membuat widget input date yang di tempatkan pada sidebar
min_date = all_df["date"].min()
max_date = all_df["date"].max()

with st.sidebar:
    start_date, end_date = st.date_input(
        label = 'Range Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
    main_df = all_df[(all_df["date"] >= str(start_date)) &
                     (all_df["date"] <= str(end_date))]
    
    weather_ride_df = create_weather_ride_df(main_df)
    daily_ride_df = create_daily_ride_df(main_df)

# melengkapi Dashboard dengan Visualisasi Data
st.header('Bike Ride Sharing Dashboard')
st.subheader('Number of Rider by Weather and Temp')


fig = plt.figure(figsize=(9,4))

sns.scatterplot(x='temperature', y='count', data=weather_ride_df, hue='weather')

plt.xlabel("Temp (C)")
plt.ylabel('Jumlah sewa')

plt.tight_layout()

st.pyplot(fig)

st.subheader('Daily Ride')

fig = plt.figure(figsize=(9,6))
sns.boxplot(data=daily_ride_df, x='work_day', y='count',hue="user status", showfliers=False, palette='magma')
st.pyplot(fig)
