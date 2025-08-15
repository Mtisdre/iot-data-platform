#!/bin/bash

echo "🌍 Choose mode: "
echo "1) Local"
echo "2) Cloud"
read -p "Enter choice (1 or 2): " choice

# Sanal ortamı aktif et
source .venv/bin/activate

# .env'den API_URL seç
if [ "$choice" == "1" ]; then
    export API_URL=$(grep API_URL_LOCAL .env | cut -d '=' -f2)
elif [ "$choice" == "2" ]; then
    export API_URL=$(grep API_URL_CLOUD .env | cut -d '=' -f2)
else
    echo "❌ Invalid choice. Exiting."
    exit 1
fi

# Process ID'leri takip etmek için dizi
PIDS=()

# Script durdurulduğunda çalışacak temizleme fonksiyonu
cleanup() {
    echo ""
    echo "🛑 Stopping all processes..."
    for pid in "${PIDS[@]}"; do
        kill $pid 2>/dev/null
    done
    exit 0
}
trap cleanup SIGINT

if [ "$choice" == "1" ]; then
    echo "🖥 Starting local backend..."
    cd backend
    python app.py &
    PIDS+=($!)
    cd ..
    sleep 3

    echo "🚀 Starting sensor simulator (local)..."
    python sensor_simulator/sensor.py &
    PIDS+=($!)

    echo "📊 Starting Streamlit dashboard (local)..."
    streamlit run dashboard.py &
    PIDS+=($!)

elif [ "$choice" == "2" ]; then
    echo "🚀 Starting sensor simulator (cloud)..."
    python sensor_simulator/sensor.py &
    PIDS+=($!)

    echo "📊 Starting Streamlit dashboard (cloud)..."
    streamlit run dashboard.py &
    PIDS+=($!)
fi

# Tüm başlatılan process'ler bitene kadar bekle
wait
