from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
CORS(app)

# Veritabanı ayarı
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'sensor_data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model
class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.String, nullable=False)

with app.app_context():
    db.create_all()

@app.route("/data", methods=["POST"])
def receive_data():
    data = request.get_json()
    if not data or "temperature" not in data or "humidity" not in data:
        return jsonify({"error": "Invalid data"}), 400

    entry = SensorData(
        temperature=data["temperature"],
        humidity=data["humidity"],
        timestamp=datetime.utcnow().isoformat()
    )
    db.session.add(entry)
    db.session.commit()

    return jsonify({"message": "Data saved", "data": {
        "temperature": entry.temperature,
        "humidity": entry.humidity,
        "timestamp": entry.timestamp
    }}), 201

@app.route("/data", methods=["GET"])
def get_data():
    records = SensorData.query.all()
    return jsonify([
        {
            "temperature": r.temperature,
            "humidity": r.humidity,
            "timestamp": r.timestamp
        } for r in records
    ]), 200

if __name__ == "__main__":
    app.run(debug=True)
