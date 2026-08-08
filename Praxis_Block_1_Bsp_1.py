tarife = {
    101: {"name": "Basic", "preis": 19.99},
    102: {"name": "Premium", "preis": 39.99}
}

mitglieder = {
    1: {"name": "Torkin", "tarif_id": 102},
    2: {"name": "Elora", "tarif_id": 101},
    3: {"name": "Garrick", "tarif_id": 102}
}
for mitglied_id, daten in mitglieder.items():
    mitglied_name = daten["name"]
    mitglied_t_id = daten["tarif_id"]

    t_details = tarife[mitglied_t_id]

    tarif_name = t_details["name"]
    tarif_preis = t_details["preis"]
    
    print(f"{mitglied_name} hat die Mitglieder-ID {mitglied_id} und hat den {tarif_name} Tarif im Wert von {tarif_preis} € gebucht.")