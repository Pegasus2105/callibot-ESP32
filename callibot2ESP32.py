# Modul: callibot2ESP32 für
# Calli:bot (Knotech-Chassi) mit ESP32 über I2C verbunden
# i2c.scan() --> zeigt folgende Ports: --> [32, 33, 34, 35, 36, 37, 38, 39]
# Ports: 34 bis 39 sind leider nicht dokumentiert oder vom ESP32?
# Version 1: 18.05.2020
# Version 2: 11.02.2023
# Autor: Wolfgang Rafelt

from machine import I2C, Pin
from time import sleep

class Callibot2(object):
    """Klasse für den Callibot des Calliope Mini, gesteuert von einem ESP32 über I2C-Bus."""

    def __init__(self):
        # i2c-Byte-Adressen des Chassis
        self.i2cAdrMotoren = 32
        self.i2cAdrAdapter = 33
        # Byte-Adressen des Motors
        self.motorLinks    = 0
        self.motorRechts   = 2
        # Geschwindigkeiten
        self.defaultSpeed  = 128								# voreingestellte Geschwindigkeit
        self.leftSpeed     = 0
        self.rightSpeed    = 0
        # LED
        self.ledrl         = 0									# rote LED vorn links
        self.ledrr         = 0									# rote LED vorn rechts
        # i2c Bus Initialisierung
        self.i2c = I2C(scl=Pin(22), sda=Pin(23), freq=400000)   # i2c-Bus Initialisierung
        self.i2c.start()										# definierter Anfangszustand
        # Speicherpuffer für i2c write-Anweisung
        self.buf = bytearray()

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# I2C-Funktionen
        
    def i2cStart(self):
        """Startet den I2C-Bus in eine definierten Anfangszustand."""
        
        self.i2c.start()									# definierten Anfangszustand herstellen

    def i2cStop(self):
        """Setzt den I2C-Bus zurück und stoppt ihn."""
        
        self.i2c.stop()

    def i2cSetMotor(self, buf):
        """Schreibt eine bestimmte Anzahl Bytes (buf) zum Motorbaustein über I2C."""
        
        self.i2cStart()										# definierten Anfangszustand herstellen
        try:
            self.i2c.writeto(self.i2cAdrMotoren, buf)
        except OSError:										# Betriebssystem Fehler ignorieren
            None											# bei schlechter Verbindung (timeout)

    def i2cSetAdapter(self, buf):							# I2C-Adapter der Platine
        """Schreibt eine bestimmte Anzahl Bytes (buf) in den Adapter über I2C."""
        
        self.i2cStart()										# definierten Anfangszustand herstellen
        try:
            self.i2c.writeto(self.i2cAdrAdapter, buf)
        except OSError:										# Betriebssystem Fehler ignorieren
            None											# bei schlechter Verbindung (timeout)

    def i2cReadAdapter(self, value):
        """Liest eine bestimmte Anzahl Bytes aus dem Adapter über I2C."""
        
        self.i2cStart()										# definierten Anfangszustand herstellen
        return self.i2c.readfrom(i2cAdrAdapter, value)		# Anzahl Bytes lesen

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Motorfunktionen

    def forward(self):
        """Startet beide Motoren des Callibot in Vorwärtsdrehung mit defaultSpeed-Wert."""
        
        self.setMotor(self.defaultSpeed)

    def backward(self):
        """Startet beide Motoren des Callibot in Rückwärtsdrehung mit defaultSpeed-Wert."""
        
        self.setMotor(self.defaultSpeed * (-1))

    def left(self):
        """Versetzt den Callibot in Linksdrehung um das linke Rad mit defaultSpeed-Wert rechts."""
        
        self.setMotorL(0)
        self.setMotorR(defaultSpeed)

    def right(self):
        """Versetzt den Callibot in Rechtsdrehung um das rechte Rad mit defaultSpeed-Wert links."""
        
        self.setMotorR(0)
        self.setMotorL(defaultSpeed)

    def leftArc(self, radius):
        None

    def rightArc(self, radius):
        None

    def getSpeedMotorL(self):
        '''Gibt die Geschwindigkeit des linken Motors zurück.

        Rückgabe: speed als Integerwert
        '''
        return self.leftSpeed

    def getMotorR(self):
        '''Gibt die Geschwindigkeit des rechten Motors zurück.

        Rückgabe: speed als Integerwert
        '''
        return self.rightSpeed

    def setSpeed(self, speed):
        """Setzt dden default speed Wert für die forward und bachward Funktionen."""
        
        self.defaultSpeed  = 128

    def setMotorL(self, speed):          # Motor links wird mit speed gesetzt
        """Setzt die Werte für den linken Motor des Chasis.

        Eingabe: speed als Integerwert von -255 bis 255.
        """
        if abs(speed) > 255:
            speed = 0
        self.leftSpeed = speed
        if speed == 0:
            self.stopMotorL()
        elif speed > 0:
            richtung = 0
            self.buf = bytearray([self.motorLinks, richtung, speed])
            self.i2cSetMotor(self.buf)
        elif speed < 0:
            richtung = 1
            self.buf = bytearray([self.motorLinks, richtung, speed])
            self.i2cSetMotor(self.buf)

    def setMotorR(self, speed):          # Motor rechts wird mit speed gesetzt
        """Setzt die Werte für den rechten Motor des Chasis.

        Eingabe: speed als Integerwert von -255 bis 255.
        """
        if abs(speed) > 255:
            speed = 0
        self.reightSpeed = speed
        if speed == 0:
            self.stopMotorR()
        elif speed > 0:
            richtung = 0
            self.buf = bytearray([self.motorRechts, richtung, speed])
            self.i2cSetMotor(self.buf)
        elif speed < 0:
            richtung = 1
            self.buf = bytearray([self.motorRechts, richtung, speed])
            self.i2cSetMotor(self.buf)


    def setMotor(self, speed):          # beide Motoren werden mit speed gesetzt
        """Setzt die Werte für die Motoren des Chasis.

        Eingabe: speed als Integerwert von -255 bis 255.
        """
        self.leftSpeed = speed
        self.rightSpeed = speed
        if speed == 0:
            self.stopMotor()
        else:
            self.setMotorL(speed)        
            self.setMotorR(speed)

    def stopMotorL(self):
        """Stoppt den linken Motor."""
        
        self.leftSpeed = 0
        self.buf = bytearray([self.motorLinks, 0, 0])
        self.i2cSetMotor(self.buf)

    def stopMotorR(self):
        """Stoppt den rechten Motor."""
        
        self.rightSpeed = 0
        self.buf = bytearray([self.motorRechts, 0, 0])
        self.i2cSetMotor(self.buf)

    def stopMotor(self):
        """Stoppt beide Motoren."""

        self.stopMotorL()
        self.stopMotorR()

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# vordere rote LED-Funktionen

    def getLedRot(self):
        """Ermittelt den Zustand der roten LED's aus Variablenwerten (nicht vom Adapter)."""
        
        return [self.ledrl, self.ledrr>>1]

    def setLedRot(self, ledrl, ledrr):
        """Setzt den Zustand der roten LED's.

        Eingabe: ledrl = 0, linke rote LED wird aus gesetzt
                 ledrr = 1, rechte rote LED wird eingeschaltet
        """

        self.ledrl = ledrl
        self.ledrr = ledrr<<1
        self.buf = bytearray([0, self.ledrl + self.ledrr])
        self.i2cSetAdapter(self.buf)

    def setLedRotLinksOn(self):
        """Schaltet linke rote LED ein."""
        
        self.ledrl = 1
        self.buf = bytearray([0, self.ledrl + self.ledrr])
        self.i2cSetAdapter(self.buf)

    def setLedRotLinksOff(self):
        """Schaltet linke rote LED aus."""
        
        self.ledrl = 0
        self.buf = bytearray([0, self.ledrl + self.ledrr])
        self.i2cSetAdapter(self.buf)

    def setLedRotRechtsOn(self):
        """Schaltet rechte rote LED ein."""

        self.ledrr = 2
        self.buf = bytearray([0, self.ledrl + self.ledrr])
        self.i2cSetAdapter(self.buf)

    def setLedRotRechtsOff(self):
        """Schaltet rechte rote LED aus."""
        
        self.ledrr = 0
        self.buf = bytearray([0, self.ledrl + self.ledrr])
        self.i2cSetAdapter(self.buf)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# vier RGB-LED unter dem Chassi Funktionen

    def setRGBLed(self, led, farbe, hell):
        """Methode setzt den Zustand einer RGB-Led.

            led = vornLinks    = 1
                  hintenLinks  = 2
                  vornRechts   = 3
                  hintenRechts = 4
            farbe = 0..7
            hell  = 0..16

        Daten für RGB-LEDs:
        Zusammensetzung eines RGB-Datenbytes:
        Bit (0..2) = Farbe (Wert 0..7)
        Bit 3      = nicht genutzt
        Bit (4..7) = Helligkeit (0 = aus, 15 Stufen)
        
        Das Farbspektrum der RGB-LEDs ist stark reduziert, um die Programmierung
        seitens der Schüler zu vereinfachen.
        Wert     Farbe
        0        schwarz (aus)
        1        grün
        2        rot
        3        gelb
        4        blau
        5        türkis
        6        violett
        7        weiß"""
        
        self.buf = bytearray([led, farbe + (hell<<4)])
        self.i2cSetAdapter(self.buf)
    
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Ultraschall Sensor Abfrage

    def getUltraschallSensor(self):
        """Methode liefert den 16-Bit Bytewert der Entfernung in mm."""
        
        us = self.i2cReadAdapter(3)     # 3 Byte einlesen
        uss = bytearray()                # 1. Byte: 
        uss.append(us[1])                # 2. Byte: niederwertiges Byte des Ultraschall-Sensors
        uss.append(us[2])                # 3. Byte: höherwertiges Byte des Ultraschall-Sensors
        return uss

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Linien Sensor Abfrage

    def getLinienSensor(self):           # 1 Byte einlesen
        """Methode liefert als Bytewert den Zustand der Liniensensoren.

        0=beide dunkel, 1=links dunkel, 2=rechts dunkel, 3=beide hell
        Bit[0]: linker Sensor: 0=dunkel, 1=hell
        Bit[1]: rechter Sensor: 0=dunkel, 1=hell"""
        
        ls = self.i2cReadAdapter(1)
        return ls
