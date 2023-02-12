# Callibot mit ESP32 Micropython über I2C
# Modul: callibot2ESP32.py
# 11.02.2023
# Wolfgang Rafelt

from callibot2ESP32 import *
from time import sleep_ms

# Hauptprogramm
# Anfahren und beschleunigen
# danach bis Stillstand verzögern

mcb2 = Callibot2()
mcb2.setSpeed(100)
for i in range(255):
    mcb2.setMotor(i)
    sleep_ms(10)
mcb2.stopMotor()
for i in range(255, -1, -1):
    mcb2.setMotor(i)
    sleep_ms(10)
sleep_ms(1000)
mcb2.i2cStop()
