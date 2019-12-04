#Studienarbeit TEAM3 (Prof. Dr. Saller) 
Kreuzkorrelationen von Maschinendaten

Änderungen/Changelog seit Übergabe des Codes Jahrgang 2016: 
-
##### PDF Ausgabe
+ Maschinennummern und Zeiträume (sowie in den Dateinamen)
+ Höchster Peakwert + x-Achsen Angabe wird ausgegeben
+ Auto-Entscheidung über das Drucken von PDF Dateien (bei geringen Peak Kurven)

##### CSV Quelldatei
- Maschinen mit einer geringen Anzahl an Zustandsänderunngen werden nun automatisch ignoriert (<= 4 Zustandsänderungen)

##### Übergabe von Parametern: 
Aufruf: 
> python automated_script.py [ORDNER: der CSV Datei] [INT: Sekundenbreite der Kreuzkorrelation] [FLOAT: Mindestwert der Korrelation für Automatisches Aussortieren niederwertiger Korrelationen]

Beispielaufruf: 
>python automated_script.py ./sourceFiles 1000 0.2


TODO: 
-
- Automatisierte Kategorisierung von PDF Dateien im Dateisystem (große/kleine Bandbreite, wiederholende Frequenzen, etc.)
- Performance Optimierungen
- Auswertung des MaxValues zweier Maschinen in eine Datenbank um mehrere Tage einfacher vergleichen zu können

