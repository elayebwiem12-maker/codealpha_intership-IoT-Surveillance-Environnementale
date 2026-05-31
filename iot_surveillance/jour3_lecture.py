from pyftdi.i2c import I2cController
import time

# Connexion via FTDI
ctrl = I2cController()
ctrl.configure('ftdi://ftdi:232h/1')
slave = ctrl.get_port(0x44)  # adresse SHT30

def read_sht30():
    """Lit la température et humidité depuis le capteur SHT30 via I2C."""
    slave.write([0x2C, 0x06])   # commande mesure high repeatability
    time.sleep(0.5)
    data = slave.read(6)        # lire 6 octets
    temp     = -45 + (175 * ((data[0] << 8 | data[1]) / 65535.0))
    humidity = 100 * ((data[3] << 8 | data[4]) / 65535.0)
    return round(temp, 2), round(humidity, 2)

print("=== Lecture capteur SHT30 ===")
print("(Ctrl+C pour arrêter)\n")

try:
    while True:
        t, h = read_sht30()
        print(f"Température : {t}°C  |  Humidité : {h}%")
        time.sleep(5)
except KeyboardInterrupt:
    print("\nArrêt propre.")
    ctrl.close()
