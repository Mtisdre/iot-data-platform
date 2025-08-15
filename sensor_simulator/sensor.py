import requests
import random
import time

API_URL = "http://127.0.0.1:5000/data"

def generate_sensor_data():
    temperature = round(random.uniform(20.0, 30.0), 2)  # 20-30°C
    humidity = round(random.uniform(40.0, 70.0), 2)     # %40-70 nem
    return {"temperature": temperature, "humidity": humidity}

if __name__ == "__main__":
    while True:
        data = generate_sensor_data()
        try:
            response = requests.post(API_URL, json=data)
            if response.status_code == 201:
                print(f"Data sent: {data}")
            else:
                print(f"Failed to send data: {response.text}")
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(5)  # 5 saniyede bir veri gönder
