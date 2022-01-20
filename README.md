# SCRUMTODOL

Das Akronym steht für supercoole wirklich nützliche Mini-TODO-Liste bei der man verschiedene Buckets hat und gewisse Fälligkeitsdaten festlegen kann.**.

## Installation

Installieren Sie zuallererst Flask, falls die noch nicht geschehen ist. Der Server läuft im Debug-Modus und kann durch Eingabe von ```python3 app.py``` in der Konsole gestartet werden.
Die App sollte nun laufen. In der Konsole sollte eine Adresse und ein Port zu sehen sein, der beim Öffnen die Web-App anzeigt, dieser sollte folgendermassen lauter ```http://127.0.0.1:5000/backlog```.

## Fähigkeiten und Verwendung

Die App ist in der Lage, Aufgaben zu speichern und sie in einer SCRUM-ähnlichen Weise abzuarbeiten. Dazu gibt es auch eine Darstellung welche einer Übersicht über die verschiedenen Aufgaben gibt
Dabei gibt es vier Kategorien:

1. Backlog: Wird als "ToDo-Bucket/Eimer" verwendet. Alles, was erledigt werden muss, kommt dort hinein.
2. Aktiv: Enthält alle ToDo-Elemente, an denen man gerade arbeitet.
3. Erledigt: Enthält alle Aufgaben, die man erfolgreich abgeschlossen hat.
4. Archivieren: Wenn der "Erledigt"-Eimer ziemlich voll ist, kann man die Aufgaben archivieren.
5. Statistik: Hierbei werden alle Aufgaben die sich in den verschiedenen Buckets, zusammengerechnet und in einer Abbildung grafisch dargestellt.

Merkmale:

- Hinzufügen von Aufgaben
- Verschieben von Objekten von einem Bucket zum nächsten
- Ändern von Objekten
- Löschen von Objekten
- Festlegen von Fälligkeitsterminen und Anzeigen eines Erinnerungssymbols für den Artikel, wenn er
  - überfällig ist (rotes Abzeichen)
  - morgen fällig (gelbe Plakette)
  - heute fällig (gelbe Plakette)
- Berechnung der Aufgaben und grafische Darstellung in Form eines Balkens.

Begrenzungen:

- Es gibt keine Möglichkeit, Aufgaben rückwärts zu verschieben.

## Projektidee

Ich hatte die Idee zu diesem Projekt, weil ich gerne plane und ich denke, dass SCRUM ein guter Weg ist, um strukturiert zu planen.
Das Ziel dieses einfachen, aber effektiven Projekts ist, dass es in der Zukunft auf die eine oder andere Weise nützlich sein soll.
Zum Beispiel, das ich mir einige Aufgaben aufgeben kann und diese auch zeitgerecht abarbeiten bzw einhalten kann. Dazu kommt das ich immer einen Einblick in meine Statistik habe
