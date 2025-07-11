import time
import machine

ledBlau = machine.Pin(2, machine.Pin.OUT)
ledGruen = machine.Pin(20, machine.Pin.OUT)

def start():
    print("Programm gestartet")
    while True:
        ledBlau.value(1)
        ledGruen.value(0)
        time.sleep(0.5)
        ledBlau.value(0)
        ledGruen.value(1)
        time.sleep(0.5)
    print("-ENDE-")