from pyftdi.i2c import I2cController

print("=== Scanner I2C ===")
print("Scan de toutes les adresses I2C...\n")

ctrl = I2cController()
ctrl.configure('ftdi://ftdi:232h/1')  # changer si ton URL est différente

capteurs_trouves = []

for addr in range(0x08, 0x78):
    try:
        port = ctrl.get_port(addr)
        port.read(1)
        print(f"✓ Capteur trouvé à l'adresse : 0x{addr:02X}")
        capteurs_trouves.append(addr)
    except:
        pass

if not capteurs_trouves:
    print("Aucun capteur trouvé. Vérifie le câblage SDA/SCL.")
else:
    print(f"\n{len(capteurs_trouves)} capteur(s) trouvé(s).")
    print("0x44 = SHT30 | 0x76 = BMP280")

ctrl.close()
