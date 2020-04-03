#Studienarbeit TEAM3 (Prof. Dr. Saller) 
Kreuzkorrelationen von Maschinendaten

Änderungen/Changelog seit Übergabe des Codes Jahrgangs 2016: 
siehe Studienarbeit von Vulte und Stöcker 2020 Kapitel "Implementierung". 


##### Installation von abhängigen Bibliotheken: 

> pip install matplotlib

> pip install numpy

> pip install mysql-connector-python

> pip install XlsxWriter

> pip install networkx

##### Aufruf des "automated_script.py"  + Übergabe von Parametern: 
Aufruf: 
> python automated_script.py [ORDNER: der CSV Datei] [INT: Sekundenbreite der Kreuzkorrelation] [FLOAT: Mindestwert der Korrelation für Automatisches Aussortieren niederwertiger Korrelationen] [ggf. Name der Zieltabelle in einer SQL Datenbank]

Beispielaufruf: 
>python automated_script.py ./sourceFiles 1000 0.2 u1Database

##### Aufruf des "script_automated_presentation.py"  + Übergabe SQL Befehl : 

Aufruf: 
> python script_automated_presentation.py [ggf. SQL Befehl]

Beispielaufruf: 
> python script_automated_presentation.py "SELECT * FROM u1 WHERE score>=0.3 AND ymax>=0.3"

