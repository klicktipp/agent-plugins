# email-erstellung

Erzeugt E-Mail-HTML, das der **HTML-Import des KlickTipp-E-Mail-Editors** möglichst verlustfrei in
bearbeitbare Drag-and-Drop-Blöcke zurückverwandelt.

## Wozu

Der HTML-Import des KlickTipp-Editors ist kein allgemeiner HTML-Parser: er mappt vorhandene
Struktur auf die Blocktypen, die er kennt, und macht aus allem anderen bestenfalls etwas
Ähnliches. HTML, das nicht auf diese Erwartung hin geschrieben wurde, landet als eine große,
unteilbare Textwüste im Editor — importiert, aber nicht mehr bearbeitbar.

Dieser Skill kodiert, welche Struktur der Importer erwartet, welche Editor-Elemente sich per HTML
überhaupt stabil erzeugen lassen und welche man besser nach dem Import von Hand ergänzt.

## Was er nicht kann

- **Keine Landingpages, keine Webseiten.** Die Importer-API ist auf E-Mail-Templates ausgelegt.
- **Kein natives Editor-JSON.** HTML-Import und das native Editor-Format sind nicht dasselbe; nicht
  jedes Element der linken Editor-Leiste lässt sich per HTML vorerzeugen.
- **Keine Garantie für Spezial-Widgets.** Eine Klasse wie `video_block` macht aus dem HTML kein
  vollwertiges natives Widget. Für belastbare Vorlagen zählt nur die Menge der als „sehr gut
  geeignet" markierten Blöcke.

## Prüfen, ob es funktioniert hat

Der Import ist erst dann gelungen, wenn das Ergebnis im Editor **in einzelne Blöcke zerfällt**,
nicht wenn es nur richtig aussieht. Nach dem Import im KlickTipp-Editor:

1. Einen Textblock anklicken — er muss einzeln selektierbar sein.
2. Einen Block verschieben — die Zeilen-/Spaltenstruktur muss erhalten bleiben.
3. Speichern — fehlt der Pflicht-Footer (`%User:Signature%`, `%Link:SubscriberInfo%`,
   `%Link:Unsubscribe%`), schlägt genau hier die Speicherung fehl.
4. KlickTipp-Variablen gegenprüfen: der Importer interpretiert sie nicht, sie überleben nur als
   Text. Ob sie im KlickTipp-Kontext auflösen, zeigt sich erst nach dem Speichern.

## Quelle

Aus der internen Vorlage für den KlickTipp-HTML-Generator übernommen und in das Skill-Format
dieses Repositories gebracht.
