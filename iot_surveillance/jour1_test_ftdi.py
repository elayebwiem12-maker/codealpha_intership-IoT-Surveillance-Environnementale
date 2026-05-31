from pyftdi.ftdi import Ftdi

print("=== Test connexion FTDI ===")
print("Devices connectés :\n")
Ftdi.show_devices()
print("\nSi tu vois 'ftdi://ftdi:232h/1' → ton adaptateur est reconnu ✓")
