from pyftdi.i2c import I2cController
import time
import sqlite3
from datetime import datetime

# Connexion via FTDI
ctrl = I2cController()
ctrl.configure('ftdi://ftdi:232h/1')
slave = ctrl.get_port(0x44)

def read_sht30():
    """Lit la température et humidité depuis le capteur SHT30 via I2C."""
    slave.write([0x2C, 0x06])
    time.sleep(0.5)
    data = slave.read(6)
    temp     = -45 + (175 * ((data[0] << 8 | data[1]) / 65535.0))
    humidity = 100 * ((data[3] << 8 | data[4]) / 65535.0)
    return round(temp, 2), round(humidity, 2)

def init_db():
    """Créer la base de données et la table si elle n'existe pas."""
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

init_db()
print("=== Base de données prête ===")
print("Fichier : sensor.db")
print("(Ctrl+C pour arrêter)\n")

try:
    while True:
        t, h = read_sht30()
        now = datetime.now().strftime('%H:%M:%S')
        print(f"[{now}]  Temp: {t}°C  |  Humidité: {h}%")
        save_reading(t, h)
        time.sleep(10)

except KeyboardInterrupt:
    print("\nArrêt propre.")
    ctrl.close()
