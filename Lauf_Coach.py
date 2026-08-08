from datetime import datetime
import json
import os
import sys
import time

woche_laeufe = []

week_days = [
    "Montag",
    "Dienstag",
    "Mittwoch",
    "Donnerstag",
    "Freitag",
    "Samstag",
    "Sonntag",
]

tage_id = {
    "Montag": "mo",
    "Dienstag": "di",
    "Mittwoch": "mi",
    "Donnerstag": "do",
    "Freitag": "fr",
    "Samstag": "sa",
    "Sonntag": "so",
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
        print(
            "\nMöchtest du das Programm beenden (e) oder zum Hauptmenü zurückkehren (b)?"
        )
        repeat = input("Antwort: ").strip()

        if repeat.isdigit():
            print(
                "\n[!] Bitte keine Zahlen, sondern nur 'e' (Programm beenden) oder 'b' (zum Hauptmenü) eingeben."
            )
            continue

        if repeat == "e":
            print("\nProgramm wird beendet. Bis zum nächsten Lauf!")
            sys.exit()

        if repeat == "b":
            return True

        print(
            "\n[!] Bitte nur 'e' (Programm beenden) oder 'b' (zum Hauptmenü) eingeben."
        )
        continue


def pace_berechnen(dauer, distanz):
    pace_dezimal = dauer / distanz
    return pace_dezimal


def pace_umwandeln(dauer, distanz):
    pace = pace_berechnen(dauer, distanz)

    pace_min = int(pace)
    pace_s = int((pace - pace_min) * 60)

    return f"Pace: {pace_min:02d}:{pace_s:02d} min/km"


def total_km_total_min():
    ges_km = 0
    ges_min = 0

    for daten in woche_laeufe:
        ges_km += daten["distanz"]
        ges_min += daten["dauer"]

    return f"Total-km: {ges_km:.2f} km | Total-min: {ges_min:.1f} min"


def week_day_manager():
    if not woche_laeufe:
        print("\n[!] Du hast bisher noch keine Läufe gespeichert.")
        return

    while True:
        print("\nNach welchem Wochentag möchtest du deine Läufe filtern?")
        tag = input("Antwort: ").strip().capitalize()

        if tag in week_days:
            gefundene_laeufe = [
                lauf for lauf in woche_laeufe if lauf["tag"] == tag
            ]

            if gefundene_laeufe:
                print(f"\n=================== LÄUFE AM {tag.upper()} ===================")
                for lauf in gefundene_laeufe:
                    pace_real = pace_umwandeln(
                        lauf["dauer"], lauf["distanz"]
                    )
                    print(
                        f"Datum: {lauf['datum']} | Dauer: {lauf['dauer']:.1f} min | "
                        f"Distanz: {lauf['distanz']:.2f} km | {pace_real}"
                    )
                print("=========================================================\n")
            else:
                print(f"\n[!] Am {tag} wurden keine Läufe aufgezeichnet.")

            break
        else:
            print(
                "\n[!] Ungültiger Wochentag. Bitte gib einen Wochentag wie 'Montag' ein."
            )


def schnellster_lauf():
    if not woche_laeufe:
        print("\n[!] Es wurden noch keine Läufe gespeichert.")
        return

    bester_lauf = min(
        woche_laeufe,
        key=lambda lauf: pace_berechnen(lauf["dauer"], lauf["distanz"]),
    )

    pace_str = pace_umwandeln(bester_lauf["dauer"], bester_lauf["distanz"])

    print("\n=================== SCHNELLSTER LAUF ===================")
    print(
        f"Tag: {bester_lauf['tag']} ({bester_lauf['datum']}) | "
        f"Dauer: {bester_lauf['dauer']:.1f} min | "
        f"Distanz: {bester_lauf['distanz']:.2f} km | "
        f"{pace_str}"
    )
    print("========================================================\n")


def input_lauf_data():
    lauf_daten = {}

    print("\n--- NEUEN LAUF EINTRAGEN ---")

    while True:
        tag = input("Tag (Wochentag): ")

        if tag.isdigit():
            print("\n[!] Bitte keine Zahlen, nur Wochentage eingeben.")
            continue

        tag = tag.strip().capitalize()

        if tag in week_days:
            kuerzel = tage_id[tag]
            lauf_daten["tag"] = tag
            break

        print("\n[!] Bitte nur Wochentage eingeben.")
        continue

    while True:
        datum = input("Datum (dd.mm.yyyy): ").strip()

        try:
            datetime.strptime(datum, "%d.%m.%Y")

            lauf_daten["datum"] = datum
            break

        except ValueError:
            print(
                "\n[!] Ungültiges Datumsformat. Bitte beachte das Format '(dd.mm.yyyy)'."
            )
            continue

    while True:
        dauer = input("Dauer (min): ").strip()

        try:
            dauer = float(dauer)

            if dauer <= 0:
                print("\n[!] Dauer in min muss größer als 0 min sein.")
                continue

            lauf_daten["dauer"] = dauer
            break

        except ValueError:
            print("\n[!] Bitte nur Zahlen eingeben.")
            continue

    while True:
        distanz = input("Distanz (km): ").strip()

        try:
            distanz = float(distanz)

            if distanz <= 0:
                print("\n[!] Distanz in km muss größer als 0 km sein.")
                continue

            lauf_daten["distanz"] = distanz
            break

        except ValueError:
            print("\n[!] Bitte nur Zahlen eingeben.")

    lauf_daten["kuerzel"] = kuerzel
    return lauf_daten


def hauptmenue():
    global woche_laeufe
    woche_laeufe = daten_laden()

    while True:
        print("\n---------------------- HAUPTMENÜ ----------------------")
        print("Möchtest du:")
        print("  [a] Neue Laufdaten eintragen")
        print("  [s] Alle Läufe ansehen")
        print("  [b] Laufstatistiken ansehen")
        print("  [e] Programm beenden")
        print("-------------------------------------------------------")
        antwort = input("Antwort: ").strip().lower()

        if antwort.isdigit():
            print(
                "\n[!] Bitte nur 'a' (hinzufügen), 's' (ansehen), 'b' (Statistiken) oder 'e' (beenden) eingeben."
            )
            continue

        if antwort == "a":
            lauf_dictionary = input_lauf_data()
            woche_laeufe.append(lauf_dictionary)
            daten_speichern()
            print("\n[✓] Lauf erfolgreich gespeichert!")
            continue

        if antwort == "e":
            print("\nVorgang wird abgebrochen...")
            time.sleep(1)
            antwort = exit_manager()

            if antwort == True:
                continue

        if antwort == "s":
            if woche_laeufe:
                print("\n=================== ALLE GESPEICHERTEN LÄUFE ===================")
                for lauf in woche_laeufe:
                    tag = lauf["tag"]
                    datum = lauf["datum"]
                    dauer = lauf["dauer"]
                    distanz = lauf["distanz"]

                    pace_real = pace_umwandeln(dauer, distanz)

                    print(
                        f"Tag: {tag:<10} | Datum: {datum} | Dauer: {dauer:5.1f} min | "
                        f"Distanz: {distanz:5.2f} km | {pace_real}"
                    )
                print("================================================================\n")

            else:
                print("\n[!] Du hast bisher keine Läufe gespeichert.")

            continue

        elif antwort == "b":
            while True:
                print("\n-------------------- STATISTIKEN --------------------")
                print("Was möchtest du ansehen?")
                print("  [g] Gesamtkilometer & Gesamtzeit")
                print("  [f] Schnellster Lauf")
                print("  [w] Wochentagfilter")
                print("  [e] Zurück zum Hauptmenü / Beenden")
                print("-----------------------------------------------------")
                statistik = input("Antwort: ").strip().lower()

                if statistik.isdigit():
                    print(
                        "\n[!] Bitte keine Zahlen, sondern nur 'g', 'f', 'w' oder 'e' eingeben."
                    )
                    continue

                if statistik == "g":
                    value = total_km_total_min()
                    print("\n=================== GESAMTSTATISTIK ===================")
                    print(f"{value}")
                    print("=======================================================\n")
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

                print(
                    "\n[!] Bitte nur 'g' (Gesamt), 'f' (Schnellster), 'w' (Filter) oder 'e' eingeben."
                )
                continue

            continue

        print(
            "\n[!] Bitte nur 'a' (hinzufügen), 's' (ansehen), 'b' (Statistiken) oder 'e' (beenden) eingeben."
        )
        continue


print("\n==========================================")
print("          DEINE LAUFCOACH-APP             ")
print("==========================================")
input("Drücke 'Enter', um zu starten...")
time.sleep(1)
hauptmenue()