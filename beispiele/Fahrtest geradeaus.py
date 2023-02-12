# Callibot mit ESP32 Micropython über I2C
# Modul: callibot2ESP32.py
# 11.02.2023
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
