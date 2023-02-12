# ESP32 auf Knotech-Chassi
# Modul für Klasse: Chassis
# 18.05.2020, neu:11.02.2023
# Wolfgang Rafelt

from callibot2ESP32 import *
from time import sleep_ms

# Hauptprogramm
# geradeaus fahren
mcb2 = Callibot2()
mcb2.forward()
sleep_ms(2000)
mcb2.stopMotor()
sleep_ms(1000)
mcb2.backward()
sleep_ms(2000)
mcb2.stopMotor()
mcb2.i2cStop()
