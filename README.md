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
mogelijk zijn. In eerste instantie passen we passen we dit toe op de configuraties
van batterijen in drie voorbeeldwijken. Vervolgens verplaatsen we batterijen om
goedkopere configuraties te krijgen. Ten slotte plaatsen we zelfs batterijen met
verschillende typen om uiteindelijk een energienetwerk aan te leggen terwijl we
de kosten zo laag mogelijk houden.

![alt text](http://heuristieken.nl/wiki/images/b/b7/Wijk1.png)

## Aan de slag (Getting Started)

### Vereisten (Prerequisites)

Deze codebase is volledig geschreven in [Python3.6.3](https://www.python.org/downloads/). In requirements.txt staan alle benodigde packages om de code succesvol te draaien. Deze zijn gemakkelijk te installeren via pip dmv. de volgende instructie:

```
pip install -r requirements.txt
```

### Structuur (Structure)

In map Code staan alle Python-scripts. Binnen deze map staat de map Helper_Functions
en de map Algorithms. Binnen Algorithms staat ook een map Legacy_algorithms, waar
algoritmes in staan die we wel gebruikt hebben, maar waar we betere alternatieven
voor hebben gemaakt.

In de map Data staan de huizen en de batterijen voor de drie wijken. Beiden hebben
een locatie in het grid en de huizen hebben daarbij een maximale output en de
batterijen een maximale capaciteit.

Ten slotte staan in de map Results de resultaten die voor de verschillende algoritmes
zijn gevonden. Daarbij is er ook een map Figures waarin belangrijke resultaten
in tabellen en figuren zijn uitgebeeld.  

### Test (Testing)

TO DO (hoe instrueren we de gebruik omtrent het gebruik van onze code?)

```
python main.py
```

## Auteurs (Authors)

* Marco Heuvelman
* Lucas Lumeij
* Niels van Opstal

## Dankwoord (Acknowledgments)

* Bart van Baal
* Daan van den Berg
* StackOverflow
* Minor Programmeren van de UvA
