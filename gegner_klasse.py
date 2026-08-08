import random

class Gegner:
    def __init__(self, name, leben, schaden, ausweichen):
        self.name = name
        self.leben = leben
        self.schaden = schaden
        self.ausweichen = ausweichen

    def schlage_andere(self, opfer):
        wuerfel = random.randint (0, 101)

        if wuerfel < opfer.ausweichen:
            print(f"\n{opfer.name} ist ausgewichen.\n")

        else:
            opfer.leben = opfer.leben - self.schaden
            print(f"\n{opfer.name} konnte dem Angriff von {self.name} nicht ausweichen.\n")
            print(f"\n{self.name} verursacht {self.schaden} Schaden.\n")
            print(f"\n{opfer.name} verliert {self.schaden} Leben und hat noch {opfer.leben} Leben.\n")

troll = Gegner("Der Troll", 250, 35, 60)
drache = Gegner("Der Drache", 500, 70, 5)
gegner = [troll, drache]

while troll.leben > 0 and drache.leben > 0:   
    angreifer = random.choice(gegner)

    if angreifer == troll:
        verteidiger = drache

    else:
        verteidiger = troll

    angreifer.schlage_andere(verteidiger)

print("\nDer Kampf ist vorbei.\n")

if troll.leben <= 0:
    print("Der Drache hat gewonnen.\n")

else:
    print("Der Troll hat gewonnen.\n")

