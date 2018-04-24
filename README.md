# Mijn Project

Er zijn tegenwoordig steeds meer huizen die zonnepanelen op het dak hebben. Dit
is een goede zaak, aangezien we zo minder afhankelijk van fossiele brandstoffen
worden. Echter een (luxe)probleem van deze zonnepanelen is dat er soms meer zonne-energie
binnenkomt dan gebruikt wordt. Deze energie kan niet worden teruggegeven aan het
net, dus moet worden opgeslagen op grote batterijen. Deze batterijen worden in de
wijken geplaatst en de huizen moeten hierop worden aangesloten. Hierbij is sprake
van een aantal complicaties. Ten eerste hebben de batterijen een maximum capaciteit
en de huizen een maximum output. De output van de huizen mag de capaciteit van een
batterij niet overschrijden. Ten tweede is het aanleggen van kabels tussen de huizen
en de batterijen kostbaar, dus deze kabels moeten zo kort mogelijk zijn. Concluderend,
de batterijen moeten allen gekoppeld zijn aan een batterij (een huis mag niet aan
twee batterijen) en de afstanden tussen de huizen en de batterijen moeten zo kort
mogelijk zijn. In eerste instantie passen we passen we dit toe op voorbeeldwijken,
later verplaatsen we en voegen we batterijen toe. Ten slotte ontwerpen we zelf
voorbeeldwijken.

![alt text](http://heuristieken.nl/wiki/images/b/b7/Wijk1.png)

## Aan de slag (Getting Started)

### Verseisten (Prerequisites)

Deze codebase is volledig geschreven in [Python3.6.3](https://www.python.org/downloads/). In requirements.txt staan alle benodigde packages om de code succesvol te draaien. Deze zijn gemakkelijk te installeren via pip dmv. de volgende instructie:

```
pip install -r requirements.txt
```

### Structuur (Structure)

Alle Python scripts staan in de folder Code. In de map Data zitten alle input waardes en in de map resultaten worden alle resultaten opgeslagen door de code.

### Test (Testing)

Om de code te draaien met de standaardconfiguratie (bv. brute-force en voorbeeld.csv) gebruik de instructie:

```
python main.py
```

## Auteurs (Authors)

* Marco Heuvelman
* Lucas Lumeij
* Niels van Opstal

## Dankwoord (Acknowledgments)

* Bart van Baal
* StackOverflow
* Minor Programmeren van de UvA
