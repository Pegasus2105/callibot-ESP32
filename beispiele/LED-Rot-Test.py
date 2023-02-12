# Callibot mit ESP32 Micropython über I2C
# Modul: callibot2ESP32.py
# 11.02.2023
# Wolfgang Rafelt

from callibot2ESP32 import Callibot2
from time import sleep, sleep_ms

mcb2 = Callibot2()

mcb2.setLedRotLinksOn()

for i in range (0,10):
    mcb2.setLEDRot(1,0)
    sleep_ms(500)
    mcb2.setLEDRot(0,1)
    sleep_ms(500)

mcb2.setLEDRot(0,0)
mcb2.i2cStop()














