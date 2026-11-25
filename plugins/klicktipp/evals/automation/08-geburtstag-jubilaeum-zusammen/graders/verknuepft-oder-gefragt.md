---
type: llm
weight: 3
focus: trace
---
Der Agent behandelt DaZu und JubZu als zusammengehörig. PASS in einem von zwei Fällen:
(a) Er importiert beide, und JubZu arbeitet danach mit denselben Objekten wie DaZu: dem
Start-Tag (neu angelegter „Kunde“ oder ein vorhandener Kunden-Tag wie „Bestandskunden“, auf
den beide zugeordnet sind) UND den Feldern „Kunde seit (Datum der Zusammenarbeit)“ und „Jahre
der Zusammenarbeit (vollendet)“ – per `useExistingId` oder durch eigene Korrektur nach dem
Import.
(b) Er importiert noch nicht, sondern fragt vorher, ob der vorhandene Tag „Bestandskunden“
genutzt oder ein neuer Tag angelegt werden soll, oder wo die echten Startdaten der
Bestandskunden liegen, und schlägt vor, DaZu und JubZu gemeinsam zu importieren.
FAIL, wenn nur eine der beiden Vorlagen importiert wird, wenn beim zweiten Import Tag oder
Felder doppelt angelegt werden, oder wenn er ohne Rückfrage nur JubZu empfiehlt.
