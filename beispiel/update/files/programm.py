def start():
    print("Programm gestartet")
    while True:
        ledBlau.value(1)
        time.sleep(0.5)
        ledBlau.value(0)
        time.sleep(0.5)
    print("-ENDE-")