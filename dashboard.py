import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

API_URL = "http://127.0.0.1:5000/data"

st.title("IoT Sensor Data Dashboard")

# API'den veri çek
try:
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        if data:
            df = pd.DataFrame(data)
            st.write("### Son Veriler", df.tail(10))

            # Grafik
            fig, ax = plt.subplots()
            ax.plot(df['timestamp'], df['temperature'], label='Temperature (°C)', color='red')
            ax.plot(df['timestamp'], df['humidity'], label='Humidity (%)', color='blue')
            ax.set_xlabel("Time")
            ax.set_ylabel("Values")
            ax.legend()
            plt.xticks(rotation=45)
            st.pyplot(fig)
        else:
            st.warning("Henüz veri yok.")
    else:
        st.error(f"API hatası: {response.status_code}")
except Exception as e:
    st.error(f"Bağlantı hatası: {e}")
