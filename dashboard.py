import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import time

API_URL = "https://iot-data-platform.onrender.com/data"

st.set_page_config(page_title="IoT Sensor Dashboard", layout="wide")

st.title("IoT Sensor Data Dashboard")

# Auto-refresh interval (seconds)
refresh_interval = 10
st.caption(f"⏳ Auto-refresh every {refresh_interval} seconds")

# Refresh mechanism
placeholder = st.empty()

while True:
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            if data:
                df = pd.DataFrame(data)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df = df.sort_values(by='timestamp')

                with placeholder.container():
                    st.write("### Latest Sensor Readings", df.tail(10))

                    # Anomaly detection
                    latest = df.iloc[-1]
                    alerts = []
                    if latest['temperature'] > 28:
                        alerts.append(f"🌡️ High temperature: {latest['temperature']}°C")
                    if latest['humidity'] < 45:
                        alerts.append(f"💧 Low humidity: {latest['humidity']}%")

                    if alerts:
                        st.error("⚠️ ALERTS:\n" + "\n".join(alerts))
                    else:
                        st.success("✅ All readings within safe range.")

                    # Plot
                    fig, ax = plt.subplots()
                    ax.plot(df['timestamp'], df['temperature'], label='Temperature (°C)', color='red')
                    ax.plot(df['timestamp'], df['humidity'], label='Humidity (%)', color='blue')
                    ax.set_xlabel("Time")
                    ax.set_ylabel("Values")
                    ax.legend()
                    plt.xticks(rotation=45)
                    st.pyplot(fig)

            else:
                st.warning("No sensor data available yet.")
        else:
            st.error(f"API error: {response.status_code}")
    except Exception as e:
        st.error(f"Connection error: {e}")

    time.sleep(refresh_interval)
