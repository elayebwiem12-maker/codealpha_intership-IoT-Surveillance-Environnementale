from pyftdi.i2c import I2cController
import paho.mqtt.client as mqtt
import time
from datetime import datetime

# === Connexion capteur SHT30 via FTDI ===
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

# === Connexion broker MQTT ===
client = mqtt.Client()
client.connect("localhost", 1883)

print("=== Publication MQTT démarrée ===")
print("Topics : sensor/temperature | sensor/humidity")
print("(Ctrl+C pour arrêter)\n")

try:
    while True:
        t, h = read_sht30()
        now = datetime.now().strftime('%H:%M:%S')

        client.publish("sensor/temperature", t)
        client.publish("sensor/humidity", h)

        print(f"[{now}] Publié → temp: {t}°C | humidity: {h}%")
        time.sleep(5)

except KeyboardInterrupt:
    print("\nArrêt propre.")
    ctrl.close()
    client.disconnect()
