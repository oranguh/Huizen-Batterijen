## Algoritmes

Hier zijn de algoritmes te vinden die we uiteindelijk gebruikt hebben voor onze
experimentatie. Sommige algoritmes hebben ook een 'pipeline' versie. Dat betekent
dat deze omgeschreven zijn zodat ze in een reeks van experimenten vanuit main.py
gerund kunnen worden. In de map Legacy_algorithms zijn oude algoritmes die we
niet meer gebruiken.

# Random solve

Dit algoritme legt net zo willekeurige verbindingen tussen batterijen en huizen
tot er een aantal (10000) geldige oplossingen is gevonden.

# Brabo solve

Dit is een branch 'n bound algoritme. In zekere zin is het een depth first met
pruning. Dit algoritme is nog niet efficiënt genoeg om tot het einde te laten runnen.
Als dat qua tijd had gekund, dan zou je de beste oplossing kunnen vinden.

# Hill climber

De hill climber wisselt vanuit een bepaalde geldige startpositie verbindingen van
huizen met batterijen om. Als na deze wissel de score beter wordt, dan wordt die
behouden. Dit gaat door totdat er geen verbeteringen meer optreden.

# Simulated Annealing (siman)

Dit algoritme lijkt op de hill climber, maar zal afhankelijk van de temperatuur
verslechteringen accepteren. De afkoeling kan bij ons lineair, exponentieel of
sigmoïdaal verlopen. In de pipeline is het sigmoïdaal, omdat dat de beste resultaten
lijkt op te leveren. 
