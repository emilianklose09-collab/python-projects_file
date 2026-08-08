class Ticket:

    def __init__(self, kennzeichen):
        self.kennzeichen = kennzeichen
        self.bezahlt = False
        self.preis = 5.0
        self.bereits_bezahlt = 0.0

    def bezahlen(self, eingezahlt):
        self.bereits_bezahlt += eingezahlt

        if self.bereits_bezahlt == self.preis:
            self.bezahlt = True
            print(
                f"\nTicket für das Kennzeichen '{self.kennzeichen}' wurde"
                " vollständig bezahlt. Gute Fahrt!"
            )

        elif self.bereits_bezahlt > self.preis:
            self.bezahlt = True
            rueckgeld = self.bereits_bezahlt - self.preis
            print(
                f"\nTicket für '{self.kennzeichen}' wurde bezahlt. Sie"
                f" bekommen {rueckgeld:.2f} € Rückgeld. Gute Fahrt!"
            )

        else:
            self.bezahlt = False
            zu_zahlen = self.preis - self.bereits_bezahlt
            print(
                f"\nSie haben bereits {self.bereits_bezahlt:.2f} € eingezahlt."
                f" Es fehlen noch {zu_zahlen:.2f} €."
            )


erlaubte_autos = ["HH-AB-123", "SK-EK-456"]

while True:
    kz_kunde = input("\nKennzeichen angeben (oder 'e' zum Beenden): ").strip().upper()

    if kz_kunde == "E":
        print("System wird heruntergefahren.")
        break

    if kz_kunde in erlaubte_autos:
        ticket_kunde = Ticket(kz_kunde)

        while True:
            antwort = (
                input("\nMöchten Sie jetzt bezahlen? (j/n): ").strip().lower()
            )

            if antwort == "j":
                try:
                    eingezahlt = float(input("Betrag eingeben (€): "))
                    if eingezahlt <= 0:
                        print(
                            "Bitte geben Sie einen Betrag größer als 0 € ein."
                        )
                        continue

                    ticket_kunde.bezahlen(eingezahlt)

                    if ticket_kunde.bezahlt:
                        break

                except ValueError:
                    print(
                        "Ungültige Eingabe. Bitte geben Sie eine Zahl ein (z."
                        " B. 5 oder 2.50)."
                    )
                    continue

            elif antwort == "n":
                print("\nAusfahrt verweigert. Bitte bezahlen Sie Ihr Ticket.")
                break

            else:
                print("Bitte antworten Sie mit 'j' für Ja oder 'n' für Nein.")

    else:
        print(
            "\nKennzeichen nicht im System registriert.\nBitte geben Sie erneut"
            " Ihr Kennzeichen ein, falls es sich um einen Eingabefehler"
            " handelt.\nZulässiges Format z. B.: HH-AB-123\n"
        )