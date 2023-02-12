# callibot-ESP32
Modul zur Steuerung eines Callibot der Firma Knotech mit einem ESP32 und micropython über den I2C-Bus.

Dieses Modul erlaubt es einen Callibot der Firma Knotech über einen ESP32 Mikrokontroller anzusprechen und verschiedene Funktionen des Callibot zu steuern. Dazu muss das Modul "callibot2ESP32.py" auf den ESP32 hochgelden werden. Der ESP32 Mikrocontroller wiederum muss mit micropython firmware bestückt sein. Weiterhin muss der ESP32 mit der Callibot Stromversorgung und dem I2C-Bus grove-Stecker verbunden werden. Ein einfacher Schaltplan und Foto ist mit hinterlegt. Das Modul definiert die Klasse Callibot2, die wiederum alle Methoden zur Initialisierung, Motor- und Adaptersteuerung bereit stellt.

Import: from callibot2ESP32 import *

Im eigenen Programm selbst wird eine Instanz der Klasse callibot2 erzeugt über die man Zugriff auf alle Methoden bekommt.
Eine Übersicht zu den implementierten Methoden finden Sie in Dokomentaionsdatei.
Hier eine einfache Anwendung. Der Callibot fährt 2 Sekunden vorwärts und danach 2 Sekunden rückwärts.

from callibot2ESP32 import *
from time import sleep_ms


mcb2 = Callibot2()      # mcb2 als Instanz der Klasse Callibot2

mcb2.forward()          # geradeaus vorwärts fahren mit defaultSpeed, Wert: 128

sleep_ms(2000)          # 2 Sekunden fahren

mcb2.stopMotor()      # Motoren stoppen

sleep_ms(1000)        # 1 Sekunde stehen

mcb2.backward()       # geradeaus rückwärts fahren mit defaultSpeed, Wert: 128

sleep_ms(2000)        # 2 Sekunden fahren

mcb2.stopMotor()

mcb2.i2cStop()        # I2C-Bus schließen
