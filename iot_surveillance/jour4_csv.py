from pyftdi.i2c import I2cController
import time
import csv
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

# Créer le fichier CSV avec les en-têtes
with open('sensor_data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['timestamp', 'temperature', 'humidity'])

print("=== Enregistrement CSV démarré ===")
print("Fichier : sensor_data.csv")
print("(Ctrl+C pour arrêter)\n")

try:
    while True:
        t, h = read_sht30()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        print(f"[{now}]  Temp: {t}°C  |  Humidité: {h}%")

        with open('sensor_data.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([now, t, h])

        time.sleep(10)

except KeyboardInterrupt:
    print("\nArrêt. Données sauvegardées dans sensor_data.csv")
    ctrl.close()
