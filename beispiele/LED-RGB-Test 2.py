# Callibot mit ESP32 Micropython über I2C
# Modul: callibot2ESP32.py
# 11.02.2023
# Wolfgang Rafelt

from callibot2ESP32 import Callibot2
from time import sleep, sleep_ms

mcb2 = Callibot2()

for i in range(1,8):            # alle 8 Farben
    for j in range(1,5):        # alle 4 RGB-Led
        mcb2.setRGBLed(j,i,7)	# einschalten
        sleep_ms(500)
        mcb2.setRGBLed(j,0,0)	# ausschalten
        sleep_ms(500)
mcb2.i2cStop()














