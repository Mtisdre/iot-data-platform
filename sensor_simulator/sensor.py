import os
import time
import random
import requests
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get API URL from environment variable (fallback to local)
API_URL = os.environ.get("API_URL", "http://127.0.0.1:5050/data")

print(f"📡 Sending data to: {API_URL}")

while True:
    data = {
        "temperature": round(random.uniform(20, 30), 2),
        "humidity": round(random.uniform(40, 70), 2)
    }
    try:
        response = requests.post(API_URL, json=data)
        if response.status_code in (200, 201):
            print(f"✅ Data sent: {data}")
        else:
            print(f"❌ Failed to send data: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Error: {e}")
    time.sleep(5)
