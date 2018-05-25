## Helper functies

Hier staan de functies die het runnen van de algoritmes mogelijk maken.

Een aantal taken die deze functies vervullen:
* Het uitlezen van de data
* Het maken van het grid
* Het plaatsen van batterijen
* Het uitlezen van oplossingen
* Het maken van plots


Belangrijkste scripts zijn degene die direct met de pipeline te maken hebben
en worden ook gebruikt in main

* batterytype_profiles:
    maakt alle 26 mogelijke combinaties voor batterijen

* battery_placer_for_pipeline:
  plaatst batterijen op een grid via een Hillclimber

* smart_grid:
  bevat het SmartGrid class met veel handige methods
