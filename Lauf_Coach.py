import time 
from datetime import datetime
import sys
import json
import os

woche_laeufe = []

week_days = [
            "Montag", 
            "Dienstag", 
            "Mittwoch", 
            "Donnerstag", 
            "Freitag", 
            "Samstag", 
            "Sonntag"
]

tage_id = {
            "Montag": "mo",
            "Dienstag": "di", 
            "Mittwoch": "mi", 
            "Donnerstag": "do", 
            "Freitag": "fr", 
            "Samstag": "sa", 
            "Sonntag": "so"
}

DATEI_NAME = "lauf_daten.json"


def daten_laden():
    if os.path.exists(DATEI_NAME):
        with open(DATEI_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    return []  


def daten_speichern():
    with open(DATEI_NAME, "w", encoding="utf-8") as f:
        json.dump(woche_laeufe, f, ensure_ascii=False, indent=4)

def exit_manager():
    while True:
        print("Möchtest du das Programm beenden (e) oder zum Hauptmenü zurückkehren (b)?")
        repeat = input("Antwort: ")

        if repeat.isdigit():
            print("Bitte keine Zahlen, sondern nur 'e' (Programm beenden) oder 'r' (Lauf hinzufügen) eingeben.")
            continue

        if repeat == "e":
            print("Programm wird beendet.")
            sys.exit()

        if repeat == "b":
            return True

        print("Bitte nur 'e' (Programm beenden) oder 'r' (Lauf hinzufügen) eingeben.")
        continue

def pace_berechnen(dauer, distanz):
    pace_dezimal = dauer/distanz 
    return pace_dezimal

def pace_umwandeln(dauer, distanz):
    pace = pace_berechnen(dauer, distanz)

    pace_min = int(pace)
    pace_s = int((pace - pace_min)*60)

    return (f"Pace: {pace_min:02d}:{pace_s:02d} min/km")

def total_km_total_min():
    ges_km = 0
    ges_min = 0

    for daten in woche_laeufe:
        ges_km += daten["distanz"]
        ges_min += daten["dauer"]

    return (f"Total-km: {ges_km}, Total-min: {ges_min}")

def week_day_manager():
    if not woche_laeufe:
        print("\nDu hast bisher noch keine Läufe gespeichert.")
        return

    while True:
        print("\nNach welchem Wochentag möchtest du deine Läufe filtern?")
        tag = input("Antwort: ").strip().capitalize()

        if tag in week_days:
            gefundene_laeufe = [lauf for lauf in woche_laeufe if lauf["tag"] == tag]

            if gefundene_laeufe:
                print(f"\n--- Läufe am {tag} ---")
                for lauf in gefundene_laeufe:
                    pace_real = pace_umwandeln(lauf["dauer"], lauf["distanz"])
                    print(
                        f"Datum: {lauf['datum']} | Dauer: {lauf['dauer']:.1f}"
                        f" min | Distanz: {lauf['distanz']:.2f} km |"
                        f" {pace_real}"
                    )
            else:
                print(f"Am {tag} wurden keine Läufe aufgezeichnet.")

            break  
        else:
            print("Ungültiger Wochentag. Bitte gib einen Wochentag wie 'Montag ein.")    

def schnellster_lauf():
    if not woche_laeufe:
        print("\nEs wurden noch keine Läufe gespeichert.")
        return

    bester_lauf = min(
        woche_laeufe,
        key=lambda lauf: pace_berechnen(lauf["dauer"], lauf["distanz"]),
    )

    pace_str = pace_umwandeln(bester_lauf["dauer"], bester_lauf["distanz"])

    print("\n--- SCHNELLSTER LAUF ---")
    print(
        f"Tag: {bester_lauf['tag']} ({bester_lauf['datum']}) | "
        f"Dauer: {bester_lauf['dauer']:.1f} min | "
        f"Distanz: {bester_lauf['distanz']:.2f} km | "
        f"{pace_str}\n"
    )

def input_lauf_data():
    lauf_daten = {}

    while True:
        tag = input("Tag (Wochentag): ")
            
        if tag.isdigit():
            print("Bitte keine Zahlen, nur Wochentage eingeben.")
            continue
            
        tag = tag.strip().capitalize()

        if tag in week_days:
            kuerzel = tage_id[tag]
            lauf_daten["tag"] = tag
            break

        print("Bitte nur Wochentage eingeben.")
        continue

    while True:
        datum = input("Datum (aa.bb.cccc): ").strip()
    
        try:
            datetime.strptime(datum, "%d.%m.%Y")
    
            lauf_daten["datum"] = datum
            break
    
        except ValueError:
            print("Ungültiges Datenformat. Bitte beachte das Format '(aa.bb.cccc)'.")
            continue
    
    while True:   
        dauer = input("Dauer (min): ").strip()
    
        try:
            dauer = float(dauer)

            if dauer <= 0:
                print("Dauer in min muss größer als 0 min sein.")
                continue

            lauf_daten["dauer"] = dauer
            break

        except ValueError:
            print("Bitte nur Zahlen eingeben.")
            continue
    
    while True:
        distanz = input("Distanz (km): ").strip()

        try:
            distanz = float(distanz)

            if distanz <= 0:
                print("Distanz in km muss größer als 0 km sein.")
                continue

            lauf_daten["distanz"] = distanz
            break

        except ValueError:
            print("Bitte nur Zahlen eingeben.")

    lauf_daten["kuerzel"] = kuerzel
    return lauf_daten

def hauptmenue():
    global woche_laeufe
    woche_laeufe = daten_laden() 

    while True:
        print("Möchtest du neue Laufdaten eintragen (a), deine Läufe ansehen (s), Laufstatistiken ansehen (b) oder das Programm beenden (e).")
        antwort = input("Antwort: ")

        if antwort.isdigit():
            print("Bitte nur 'a' (hinzufügen), 's' (Läufe ansehen) oder 'e' (abbrechen) eingeben.")
            continue

        if antwort == "a":
            lauf_dictionary = input_lauf_data()
            woche_laeufe.append(lauf_dictionary)
            daten_speichern()
            print("Lauf erfolgreich gespeichert!")
            continue

        if antwort == "e":
            print("Vorgang wird abgebrochen.")
            time.sleep(1)
            antwort = exit_manager()

            if antwort == True:
                continue

        if antwort == "s":
            if woche_laeufe:
                print("\n--- ALLE GESPEICHERTEN LÄUFE ---")
                for lauf in woche_laeufe:
                    tag = lauf["tag"]
                    datum = lauf["datum"]
                    dauer = lauf["dauer"]
                    distanz = lauf["distanz"]

                    pace_real = pace_umwandeln(dauer, distanz)

                    print(
                        f"Tag: {tag} | Datum: {datum} | Dauer: {dauer:.1f} min |"
                        f" Distanz: {distanz:.2f} km | {pace_real}"
                        )
                    
            else:
                print("Du hast bisher keine Läufe gespeichert.")

            continue

        elif antwort == "b":
            while True:
                print("Möchtest du die 'Gesamtkilometer und Gesamtzeit' (g), 'schnellster Lauf' (f) 'Wochentagfilter' (w) ansehen oder das Programm beenden (e)?")
                statistik = input("Antwort: ")

                if statistik.isdigit():
                    print("Bitte keine Zahlen, sondern nur 'g' (Gesamtkilometer und Gesamtzeit),'f' (schnellster Lauf') oder 'w' (Wochentagfilter) eingeben.")
                    continue

                if statistik == "g":
                    value = total_km_total_min()
                    print(f"{value}")
                    continue

                if statistik == "f":
                    schnellster_lauf()
                    continue

                if statistik == "w":
                    week_day_manager() 
                    continue

                if statistik == "e":
                    exit = exit_manager()

                    if exit == True:
                        break
                        
                print("Bitte nur 'g' (Gesamtkilometer und Gesamtzeit),'f' (schnellster Lauf') oder 'w' (Wochentagfilter) eingeben.")
                continue

            continue

        print("Bitte nur 'a' (hinzufügen), 's' (Läufe ansehen) oder 'e' (Programm abbrechen) eingeben.")
        continue


print("Deine Laufcoach-App.")
input("Drücke 'Enter' zum starten.")
time.sleep(2)
hauptmenue()