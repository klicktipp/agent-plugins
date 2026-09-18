# Eine neue E-Mail entstehen lassen

Wann du hier landest: der Körper einer E-Mail soll **neu entstehen** — es gibt noch keine Gestaltung,
die du übernehmen könntest, oder du musst sie selbst schreiben. Geht es nur darum, eine vorhandene
Gestaltung hineinzuholen, steht der kurze Weg in `SKILL.md` und du brauchst diese Datei nicht.

**Zuerst die Frage, die alles andere entscheidet: Gibt es die Gestaltung schon irgendwo?**

- Als **andere E-Mail dieses Kontos** — die letzte Ausgabe, eine Vorlagen-Mail → `email-content-copy`.
  Ein Aufruf.
- Als **Bee-Dokument** — Vorlage, Export → `email-content-document-import`. Ein Aufruf.
- **Nur als HTML** — von einer Agentur, aus einem anderen Werkzeug → `email-content-import`. Ein
  Aufruf, plus die Konvertierungskosten aus `importWarnings`.

Nur wenn **nichts** davon existiert, entsteht der Körper wirklich neu — und auch dann gehört er in
einen Aufruf: schreib das Dokument selbst (`references/document-skeleton.json` für die Form,
`references/bee-simple-schema/` für die Felder) und leg es mit `email-content-document-import` ab.

**Warum das keine Stilfrage ist.** Jeder Werkzeugaufruf kostet 15–30 Sekunden, davon das meiste
nicht im Server, sondern im Modell davor. Eine E-Mail aus fünfzehn Bausteinen zusammenzusetzen sind
fünfzehn Runden plus Zeilen und Gestaltung — gemessene Läufe landen so bei über zehn Minuten, für
ein Ergebnis, das ein einziger Import in unter einer Minute erreicht.

**Baustein für Baustein** (`email-row-add`, dann je Baustein ein `email-<art>-add`) bleibt der Weg
für den **einzelnen zusätzlichen** Block in einem Entwurf, der schon steht — nicht für einen ganzen
Körper. Und es ist die Notlösung, wenn ein Dokument nicht zustande kommt: sag dem Nutzer dann, dass
es länger dauert.

Was ein neu entstehender Körper **nicht** von selbst mitbringt, ist Gestaltung. Ein leerer Entwurf
hat keinen Baustein, von dem ein neuer sein Aussehen abschauen könnte — jeder Block landet mit
seinem Startzustand, und ohne Gegenmaßnahme sieht das Ergebnis zusammengewürfelt aus, egal wie gut
die Texte sind. Setz
Typografie, Abstände und Farben deshalb selbst, und zwar **für alle Bausteine gemeinsam**:
`email-page-style-write` für die Seite, `email-row-style-write` je Zeile, `email-block-style-write`
für den einzelnen Block. Eine E-Mail wirkt professionell durch Abstände und konsequente
Typografie, nicht durch Dekoration; eine halb umgestellte Skala sieht schlechter aus als gar keine.

Zwei Dinge gehören dabei auf die richtige Ebene:

**Die Schriftart setzt du einmal auf der Seite**, mit `fontFamily` in `email-page-style-write` —
nicht je Baustein. Die Bausteine stehen im Startzustand auf `inherit`, greifen die Seitenvorgabe
also von selbst. Angeboten sind die Systemschriften der Auswahl im Editor, unter **genau den
Namen, die dort stehen**: `Arial`, `Courier`, `Georgia`, `Helvetica Neue`, `Lucida Sans`, `Tahoma`,
`Times New Roman`, `Trebuchet MS`, `Verdana` sowie die beiden japanischen `ヒラギノ角ゴ Pro W3`
und `メイリオ`. Du nennst den **Namen**, nicht den Stack — die Ausweichkette schreibt der Server.
`Helvetica` und `Courier New` werden weiter angenommen; sie standen früher in der Liste.

**Eine Webschrift wie Montserrat oder Roboto kannst du nicht setzen**, obwohl der Editor sie
anbietet: die braucht zusätzlich einen Eintrag in `page.body.webFonts` mit einer Google-Fonts-URL,
damit der Editor den `<link>` erzeugt. Ohne den fällt sie beim Empfänger still auf eine
Systemschrift zurück, und niemand sieht es. Deshalb stehen die acht — Bitter, Droid Serif, Lato,
Montserrat, Open Sans, Roboto, Source Sans Pro, Ubuntu — hier gar nicht zur Wahl, statt als Namen,
die nichts tun. Wer eine davon will, setzt sie im KlickTipp-Editor.

**Die Ausrichtung der ganzen E-Mail** ist `contentAlign` — `left`, `center` oder `right` — im
selben Werkzeug, neben `contentWidth`. Sie entscheidet, wo die Nachricht steht, wenn das Fenster
breiter ist als sie; mit den Ausrichtungen *innerhalb* eines Blocks (`textAlign` in
`email-block-style-write`) hat sie nichts zu tun. Ein neuer Entwurf startet mit dem
Standarddokument, nicht mit dem Aussehen eines anderen Newsletters — wer eine Vorlage nachbaut,
setzt Breite, Ausrichtung und Schrift also selbst.

**Einen Rahmen um eine Zeile setzt du auf der Zeile**, mit `borderTop`/`-Right`/`-Bottom`/`-Left`
in `email-row-style-write` — nicht auf ihren Spalten. Ein Rahmen je Spalte zeichnet eine Box je
Spalte, mit sichtbaren Nähten dazwischen, statt einer Linie um die ganze Zeile. Dasselbe gilt für
den Innenabstand: `paddingTop` und Geschwister auf der Zeile halten den Inhalt von der Kante der
Zeile weg, die Spalten-Variante nur von der Kante der Spalte.

Liegt bereits HTML vor — von einer Agentur, aus einem anderen Werkzeug —, ist
`email-content-import` der Weg dafür (siehe „Bestehendes HTML bearbeiten" und die zwingenden
Regeln in `references/html-authoring.md`). **Schreib aber kein HTML, nur um es dann zu
importieren.** Die Konvertierung kostet, was `importWarnings` auflistet, und was du gerade gebaut
hast, ist bereits ein Dokument — die Bausteinwerkzeuge kommen ohne Umweg ans Ziel.

### So generierst du eine

1. **Entscheide selbst, ohne Rückfrage** — Reihenfolge der Zeilen, Farben, Bildsprache. Der
   Auftrag sagt, worum es geht; daraus folgt die Gestaltung. Sag hinterher in einem Satz, was du
   entschieden hast — das kann der Nutzer korrigieren und hat dann etwas Fertiges vor sich statt
   einer Frage. **Das gilt für Gestaltung, nicht für Festlegungen über die Zielgruppe**: Betreff,
   Empfängerkreis, Versandzeitpunkt und die Einstellungen eines Splittests fragst du ab, statt sie
   zu wählen — und was du am Ende doch selbst gewählt hast, nennst du als deine Wahl und nie als
   Standardwert.
2. **Den ganzen Körper in einem Aufruf ablegen** — nach der Routing-Frage oben. Schreibst du das
   Dokument selbst, ist `references/blocks/` trotzdem die Quelle dafür, was jede Bausteinart an
   Feldern trägt (`blocks/README.md` ist der Index); die Add-Werkzeuge und das Dokument kennen
   dieselben Felder. Nur wenn es bausteinweise sein muss: `email-row-add`, dann die Bausteine
   darin — Überschrift, Absatz, Bild, Button, Liste, Abstand als Grundausstattung.
3. **Gestaltung setzen, zusammenhängend.** Seite, Zeilen, Blöcke — mit den Style-Werkzeugen aus
   dem Absatz oben, nicht Block für Block nach Gefühl.
4. **Die Fußzeile gehört in jede E-Mail**: Abmeldelink und Anbieterkennzeichnung. Wer sie vergisst,
   bekommt sie spätestens vom `email-content-check` vorgehalten — besser vorher.
5. **Bilder besorgen — in dieser Reihenfolge.** Erst `email-image-search`: Logo, Produktfoto,
   Teambild liegen in der Mediathek des Kontos und in keinem Stockarchiv. Das Werkzeug **listet
   auf, es sucht nicht** — es gibt eine Seite der Bibliothek heraus, und mit `nextCursor` holst du
   die nächste. Eine Suchanfrage nimmt es nicht, weil der Speicher Dateinamen kennt und keine
   Motive: „Auto" hätte nie ein Foto eines Autos gefunden. Lies also eine Seite und wähl daraus.
   Findet sich dort nichts, `email-image-stock-search` — dieselben freien Archive (Pexels,
   Pixabay), die auch der Editor anbietet. Eigenes Material kommt über `email-image-upload` herein.

   **Eine Stock-URL darf nicht in den Newsletter.** Gib `sourceUrl` und `fileName` des gewählten
   Fotos an `email-image-upload-from-url` und nimm die URL, die zurückkommt. Eine fremde URL lässt jedes
   Postfach einen Dritten kontaktieren und bricht an dem Tag, an dem das Foto dort verschwindet.

   Zwei Dinge, die dich sonst blamieren: Die Stock-Suche kommt **nie leer zurück** — zu einer
   Anfrage ohne Treffer liefert sie unverwandte Fotos. Schau an, was gekommen ist, und sag, was es
   zeigt, statt es als Fund zu präsentieren. Und **lass den Nutzer wählen**: die Lizenz verlangt
   keine Namensnennung, schränkt aber erkennbare Personen ein — das ist seine Entscheidung.
6. **`email-content-check`**, bevor veröffentlicht wird — und die Befunde weitergeben, statt still
   zu reparieren.

**Wo trotzdem gefragt wird**, weil es nicht Gestaltung ist: bevor ein Import bestehenden Inhalt
ersetzt, bevor ein Baustein entfernt wird, und bei der Wahl eines Stockfotos — dessen Lizenz
schränkt erkennbare Personen ein, und das ist die Entscheidung des Nutzers. Gestaltung entscheidest
du, Verluste und Rechte entscheidet er.
