# Inhalt ersetzen — ein Vorgehen

Der häufigste Auftrag und der, bei dem am meisten kaputtgeht: „hier ist der neue Text, setz ihn in
den Newsletter ein". Das ist passiert: ein Agent hat eine Trennlinie, den Video-Button, eine
Zwischenüberschrift und einen Absatz entfernt, weil die Textdatei sie nicht erwähnte. Der Auftrag
war „Text ersetzen", das Ergebnis war ein anderes Design.

**Die Faustregel:** Nach einer Textersetzung hat der Newsletter **dieselbe Anzahl und Reihenfolge
von Bausteinen wie vorher**, nur mit anderem Text. Weicht dein Ergebnis davon ab, war es keine
Textersetzung — und dann muss der Nutzer vorher zugestimmt haben.

## Der Ablauf

1. **`email-get` mit `contentOutline`.** Nicht `content`: du brauchst uuid, Art und den aktuellen
   Wert jedes schreibbaren Feldes, und genau das ist die Outline — bei einem Viertel der Bytes.
2. **Die Zuordnung aufschreiben, bevor du schreibst.** Welcher Abschnitt der Quelle gehört zu
   welcher uuid? Mach daraus eine Liste, und zwar vollständig: auch die Bausteine, für die die
   Quelle nichts hergibt, und die Teile der Quelle, für die es keinen Baustein gibt.
3. **Die Fälle benennen, die keine reine Ersetzung sind** (siehe unten) und den Nutzer
   entscheiden lassen, bevor irgendetwas geschrieben wird.
4. **Schreiben.** Alle Textbausteine in **einem** `email-text-write` — es nimmt eine Liste. Ein
   Button bekommt sein `label`/`href` mit `email-button-write`, ein Bild seine `src`/`alt` mit
   `email-image-write`.
5. **Berichten, was du nicht angefasst hast**, nicht nur was du geändert hast.
6. **Veröffentlichen** mit `email-content-publish`, wenn der Nutzer es will — sonst bleibt es
   Entwurf, und das ist auch in Ordnung.

## Die vier Fälle, die kein reines Ersetzen sind

| Fall | Was zu tun ist |
| --- | --- |
| Die Quelle hat **weniger** Text als der Newsletter Bausteine | Der Reihe nach füllen, was zu füllen ist, und die übrigen **benennen**: „drei Absätze und eine Zwischenüberschrift haben keinen neuen Text; ich habe sie unverändert gelassen. Sollen sie raus?" |
| Die Quelle hat **mehr** Text als Bausteine da sind | Hinzufügen (`email-paragraph-add` und Geschwister), nicht Absätze zusammenziehen. Der neue Baustein braucht das Markup seines Nachbarn als Vorlage. |
| Die Quelle nennt **eine andere Art** — aus einem Absatz soll eine Überschrift werden | Eine Art lässt sich nicht schreiben: entfernen und neu anlegen, und dem Nutzer sagen, dass der alte Baustein dabei verschwindet. |
| Die Quelle nennt **Gestaltung** — „mach die Überschrift blau" | Farbe im Text steckt im Markup (`email-text-write`), Hintergrund und Abstand sind die Style-Werkzeuge. Zwei verschiedene Wege, nicht raten. |

## Was nie Teil einer Textersetzung ist

Trennlinie, Abstand, Bild, Video, Button, Menü, Icons, Social-Links, Tabelle und die Add-ons tragen
keinen Fließtext, den eine Textquelle ersetzen könnte. Sie werden bei „Text ersetzen" **weder
entfernt noch verschoben**. Ein Button bekommt höchstens ein neues `label`/`href`, wenn die Quelle
eines nennt.

`email-block-remove` nur auf ausdrückliche Bitte, je Baustein benannt. Nie, weil etwas „übrig" ist,
„leer wirkt" oder „nicht mehr passt". Es gibt kein Undo.

## Wenn stattdessen das ganze Design neu ist

Dann ist es keine Ersetzung, sondern ein Import: `email-content-import` mit dem HTML. Das ist der
einzige Weg für ein Design, das **nur** als HTML existiert — und er kostet, was `importWarnings`
in der Leseantwort auflistet. Lies das dem Nutzer vor, **bevor** du importierst. Schick niemals
geändertes HTML durch den Import, um eine Änderung anzubringen.

## Vor dem Veröffentlichen

`email-content-check` läuft in einem Aufruf über den ganzen Körper: Bilder ohne Alternativtext,
Buttons ohne Ziel, leere Textbausteine, nie konfigurierte Add-ons, zu geringer Kontrast, fehlende
Fuß-Platzhalter. Gib die Befunde weiter, statt still zu reparieren — ein blasser Text kann so
gewollt sein. Ein unkonfiguriertes Add-on ist die Ausnahme, die du gar nicht reparieren kannst:
seine Auswahl trifft der Nutzer im Editor.
