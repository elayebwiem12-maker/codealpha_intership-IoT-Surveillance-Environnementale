import paho.mqtt.client as mqtt
import sqlite3
from datetime import datetime

def init_db():
    """Créer la base de données si elle n'existe pas."""
    conn = sqlite3.connect('sensor.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS readings (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp   TEXT,
            temperature REAL,
            humidity    REAL
        )
    ''')
    conn.commit()
    conn.close()

def save_reading(temp, humidity):
    """Sauvegarder une lecture dans SQLite."""
    conn = sqlite3.connect('sensor.db')
    conn.execute(
        'INSERT INTO readings (timestamp, temperature, humidity) VALUES (?, ?, ?)',
        (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), temp, humidity)
    )
    conn.commit()
    conn.close()

# Stockage temporaire
data = {"temp": None, "humidity": None}

def on_message(client, userdata, msg):
    value = float(msg.payload.decode())
    topic = msg.topic

    if topic == "sensor/temperature":
        data["temp"] = value
        print(f"Reçu temp     : {value}°C")

    elif topic == "sensor/humidity":
        data["humidity"] = value
        print(f"Reçu humidity : {value}%")

    # Sauvegarder quand on a les deux valeurs
    if data["temp"] is not None and data["humidity"] is not None:
        save_reading(data["temp"], data["humidity"])
        print(f"✓ Sauvegardé dans sensor.db\n")
        data["temp"]     = None
        data["humidity"] = None

init_db()

client = mqtt.Client()
client.on_message = on_message
client.connect("localhost", 1883)
client.subscribe("sensor/#")

print("=== Subscriber MQTT démarré ===")
print("En attente de données sur sensor/#...\n")
client.loop_forever()
