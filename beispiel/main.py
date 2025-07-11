import network
import time
import machine
from secrets import *
import ujson
import urequests
import programm

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    print("[INFO] Verbinde mit WLAN...")

    # Warten auf Verbindung (max. 10 Sekunden)
    for i in range(20):
        if wlan.isconnected():
            break
        time.sleep(0.5)

    if not wlan.isconnected():
        print("[FEHLER] Keine WLAN-Verbindung möglich!")
        machine.reset()  # Neustart oder alternativ: Fehlerzustand

    print("[INFO] WLAN verbunden mit:", wlan.ifconfig()[0])
    return wlan

def get_local_version():
    try:
        with open("version.json", "r") as f:
            data = ujson.load(f)
            return data.get("version", "0.0.0")
    except Exception as e:
        print("[WARNUNG] Konnte version.json nicht lesen:", e)
        return "0.0.0"  # Fallback, falls Datei fehlt oder fehlerhaft ist


# Aufruf der Funktion zum aufbauen einer WLAN Verbindung
wlan = connect_wifi()

# lokale Version anzeigen
local_version = get_local_version()
print("[INFO] Lokale Version:", local_version)

def check_for_update(local_version, json_url):
    try:
        print("[INFO] Lade Update-Informationen von", json_url)
        response = urequests.get(json_url)
        if response.status_code != 200:
            print("[FEHLER] HTTP-Fehler:", response.status_code)
            return None
        update_data = ujson.loads(response.text)
        response.close()

        if update_data["required_version"] != local_version:
            print("[INFO] Kein Update notwendig")
            return None

        print("[INFO] Update verfügbar:", update_data["version"])
        return update_data

    except Exception as e:
        print("[FEHLER] Fehler beim Laden der Update-Daten:", e)
        return None

def download_files(file_list):
    for entry in file_list:
        filename = entry.get("filename")
        url = entry.get("url")
        try:
            print(f"[INFO] Lade {filename} von {url}")
            r = urequests.get(url)
            if r.status_code == 200:
                with open(filename, "w") as f:
                    f.write(r.text)
                print(f"[OK] {filename} erfolgreich gespeichert.")
            else:
                print(f"[FEHLER] HTTP {r.status_code} beim Laden von {url}")
            r.close()
        except Exception as e:
            print(f"[FEHLER] Fehler beim Laden von {filename}:", e)


# Beispielaufruf:
json_url = "https://raw.githubusercontent.com/StefanDraeger/Micropython-OTA-Update/main/beispiel/update/update.json"
update_info = check_for_update(local_version, json_url)

if update_info:
    download_files(update_info["files"])

programm.start()
