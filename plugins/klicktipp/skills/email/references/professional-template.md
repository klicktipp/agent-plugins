# Die Vorlagen

Drei importfertige E-Mails in `../assets/`, **kein** Pflichtsatz von dreien: sie sind
Ausgangspunkte, keine Schablonen. Welche du nimmst, entscheidet die Aufgabe.

| Datei | Wofür | Zeilen |
| --- | --- | --- |
| `professional-template.html` | der Allrounder: Vorspann, Bild, Fließtext mit Liste, Button, zwei Spalten, Fuß | 8 |
| `template-announcement.html` | **eine** Nachricht, **ein** Ziel: Ankündigung, Einladung, Produktstart | 5 |
| `template-digest.html` | mehrere Themen nebeneinander: Rundbrief, Monatsrückblick, Lesetipps | 6 |

Die zwei kürzeren sind aus denselben Zeilen gebaut wie der Allrounder — dieselbe Mechanik,
andere Zusammenstellung und ein anderes Farbklima. Was unten über Anpassen, Werte und Grenzen
steht, gilt für alle drei.

## Wähle selbst

Welche der drei es wird, entscheidest **du** aus dem Auftrag — leg keine Auswahl vor und frag
nicht nach. Eine Ankündigung, eine Einladung, ein Produktstart: `template-announcement.html`. Ein
Rundbrief mit mehreren Themen: `template-digest.html`. Alles andere: der Allrounder. Nenne
hinterher in einem Satz, welche du genommen hast und warum; wer anderer Meinung ist, sagt es dann
— und hat etwas Fertiges vor sich statt einer Rückfrage.

Dasselbe gilt für alles Gestalterische darunter: Farbklima, Reihenfolge und Anzahl der Zeilen,
Typoskala, Bildauswahl. Gefragt wird nur, wo etwas verloren geht (ein Import über bestehenden
Inhalt, ein entfernter Baustein) oder wo eine Rechtsfrage dranhängt (die Lizenz eines Stockfotos
schränkt erkennbare Personen ein).

## Sei nicht die Vorlage

**Zwei Newsletter desselben Kunden sollen nicht wie derselbe Newsletter aussehen.** Die Vorlagen
lösen die Mechanik — Grid, Abstände, Fußzeile, importsichere Bausteine —, nicht die Gestaltung.
Die kommt von dir, und dafür gibt es Spielraum:

- **Die Zeilen sind Bausteine, keine Reihenfolge.** Lass weg, was die Aufgabe nicht braucht,
  wiederhole, was sie mehrfach braucht, stell um, wo es der Inhalt verlangt. Ein Rückblick mit
  fünf Themen ist fünfmal dieselbe Zeile.
- **Die Farben gehören zur Marke, nicht zur Vorlage.** Grundfarbe, Akzent für Button und Links,
  der Wechsel heller Flächen — nimm, was die Marke des Kunden vorgibt, oder frag danach. Die drei
  Dateien zeigen drei Farbklimata; keines ist gesetzt.
- **Die Typoskala darf mitwandern**, solange sie eine Skala bleibt: ein Verhältnis zwischen H1,
  H2 und Fließtext, nicht fünf Größen ohne Ordnung.
- **Bildsprache entscheidet mehr als Layout.** Ein Foto über die volle Breite wirkt anders als drei
  kleine — such danach, statt den Platzhalter nur zu ersetzen.

Was **nicht** zur Kreativität gehört, weil es nicht Geschmack ist, sondern Mechanik: das
Grundgerüst, die Zwölfer-Spalten, die Blockklassen, die Inline-Styles, die Pflicht-Platzhalter im
Fuß und die Beschränkung auf die importsicheren Bausteinarten. Wer daran dreht, bekommt keinen
eigenen Stil, sondern einen Newsletter, den der Editor nicht mehr bearbeiten kann.

Und die eine Regel, die keine Geschmacksfrage ist: **eine E-Mail wirkt professionell durch
Abstände und eine konsequente Typografie, nicht durch Dekoration.** Kein Rahmen, kein Schatten,
keine Farbfläche, die nach Vorlage aussieht.

## Der Allrounder im Detail

`../assets/professional-template.html` ist die vollständigste der drei. Sie ist der
**Ausgangspunkt für eine Generierung**: Struktur, Abstände, Typografie und Farben stehen, du
tauschst Inhalte. Das ist der schnellere und sicherere Weg als ein Template von null zu schreiben —
jede Regel aus `SKILL.md` ist hier schon eingehalten.

Das Template verwendet **ausschließlich** Bausteine der Stufe „sehr gut per HTML-Import geeignet":
Überschrift, Absatz, Bild, Button, Liste, Abstand. Keine Trennlinie, kein Menü, keine Social-Icons,
kein Video, keine Tabelle, kein eigenes HTML — genau die Elemente, die der Importer verlässlich in
bearbeitbare Blöcke zurückverwandelt. Wer eines der unsicheren Elemente braucht, ergänzt es nach
dem Import im Editor.

## Aufbau

| Zeile | Inhalt | Hintergrund |
| --- | --- | --- |
| 1 | Vorschauzeile — ein Satz, der im Postfach neben dem Betreff mitläuft | `#F9FAFB` |
| 2 | Logo, H1, Vorspann | `#FFFFFF` |
| 3 | Bild über die volle Breite | `#FFFFFF` |
| 4 | Anrede, Absätze, H2, Liste | `#FFFFFF` |
| 5 | Button | `#FFFFFF` |
| 6 | zwei Spalten mit H3 und Kurztext | `#F9FAFB` |
| 7 | Abstand und Schlussabsatz | `#FFFFFF` |
| 8 | Fußzeile mit Signatur und Pflichtlinks | `#F9FAFB` |

Die abwechselnden Hintergründe sind die ganze Gestaltung: kein Rahmen, keine Schatten, keine
Farbflächen, die nach Vorlage aussehen. Eine E-Mail wirkt professionell durch Abstände und eine
konsequente Typografie, nicht durch Dekoration.

## Werte, die zusammengehören

Wenn du etwas änderst, ändere es überall — eine halb umgestellte Skala sieht schlechter aus als die
ursprüngliche.

**Typografie** (`Helvetica, Arial, sans-serif`, in jeder Regel wiederholt, weil E-Mail-Clients keine
Vererbung garantieren):

| Rolle | Größe / Zeilenhöhe | Farbe |
| --- | --- | --- |
| H1 | 30 / 38, `700` | `#111827` |
| H2 | 20 / 28, `700` | `#111827` |
| H3 (Spalten) | 17 / 24, `700` | `#111827` |
| Vorspann | 18 / 28 | `#4B5563` |
| Fließtext | 16 / 26 | `#374151` |
| Text in Spalten | 15 / 24 | `#4B5563` |
| Vorschauzeile | 12 / 18 | `#6B7280` |
| Fußzeile | 13 / 20 bzw. 12 / 20 | `#6B7280` / `#9CA3AF` |

**Farben:** Akzent `#2563EB` (Button und Links), Seitenhintergrund `#F3F4F6`, Inhaltsflächen
`#FFFFFF` und `#F9FAFB`. Eine eigene Markenfarbe ersetzt `#2563EB` an genau zwei Stellen —
Button-Hintergrund und Linkfarbe im Fließtext. Prüfe dabei den Kontrast zu Weiß: unter 4,5:1 wird
weiße Buttonschrift unleserlich, dann gehört dunkler Text auf den Button.

**Abstände** — eine Skala aus 8, 12, 16, 24, 32 und 40, und nichts dazwischen:

| Wo | Wert |
| --- | --- |
| links und rechts, durchgehend | 40px |
| zwischen zwei Abschnitten | 32px |
| Überschrift zu ihrem Absatz | 8–12px |
| Absatz zu Absatz | 16px |
| Liste nach unten | 24px |
| zweispaltige Zeile: außen / zur Mitte | 40px / 20px |
| Abstandsblock vor dem Schlussabsatz | 24px |

Zwei Fallen, in die eine gewachsene Vorlage regelmäßig läuft: **Abstände addieren sich.** Der
Innenabstand einer farbigen Zeile und der Abstandsblock der nächsten stehen untereinander — 32px
plus 32px sind 64px und sehen wie ein Fehler aus. Nach einer farbigen Fläche also höchstens 24px.
Und in der zweispaltigen Zeile ist der Abstand zur Mitte **halb** so groß wie der nach außen; wird
er kleiner, kleben die Spalten, wird er gleich groß, wirkt die gestapelte Ansicht auf dem Telefon
schief.

## Was du ersetzt

- **Texte** in den `<h1>`, `<h2>`, `<h3>`, `<p>` und `<li>`. Länge grob halten: eine H1 über zwei
  Zeilen bricht das Verhältnis zum Vorspann.
- **Logo** (`https://placehold.co/360x80/...`) und **Bild** (`https://placehold.co/1200x600/...`)
  gegen echte URLs **aus dem Konto**. Woher sie kommen, in dieser Reihenfolge: `email-image-search`
  durchsuchen — Logo, Produktfoto, Teambild liegen in der Mediathek und in keinem Stockarchiv —,
  sonst `email-image-stock-search` (Pexels und Pixabay, dieselben Archive wie im Editor) und das
  gewählte Foto mit `sourceUrl` und `fileName` durch `email-image-upload` schicken; eigenes
  Material lädst du direkt hoch.

  **Das muss vor dem Import passieren**, und der Grund steht schon hier: Bilder werden beim Import
  **nicht** in den Dateimanager geladen, sondern von ihrer Quelle geladen. Eine Provider-URL im
  Template bleibt also für immer eine Provider-URL — jedes Empfängerpostfach kontaktiert einen
  Dritten, und die E-Mail bricht an dem Tag, an dem das Foto dort verschwindet. Eine interne oder
  passwortgeschützte URL bleibt im Editor leer.

  Das Bild ist mit `width="600"` und `max-width:600px` doppelt begrenzt; ein Motiv mit 1200px
  Breite bleibt auf Retina-Displays scharf.
- **`alt`-Texte** — ein Satz, der das Bild ersetzt, keine Dateibezeichnung. Rund ein Drittel aller
  Empfänger sieht Bilder erst nach einem Klick.
- **Button**: `href` und Beschriftung. Eine E-Mail hat **einen** Button; ein zweiter halbiert die
  Klickrate des ersten.
- **Links** im Fließtext: `href` und ein sprechender Linktext. Nie „hier klicken".

## Was du nicht anfasst

- **Die vier Platzhalter der Fußzeile**: `%User:Signature%`, `%Link:Unsubscribe%`,
  `%Link:SubscriberInfo%`, `%Link:WebBrowser%`. Der erste ist die gesetzlich nötige
  Absenderkennzeichnung und wird beim Versand durch die Kontosignatur ersetzt; ohne ihn oder ohne
  Abmeldelink wird ein Versand abgelehnt. Sie bleiben **wörtlich und unaufgelöst** stehen.
- **Die Klassennamen** `nl-container`, `row`, `row-content stack`, `column column-1/2`, `pad` und
  die `*_block`-Klassen. Sie sind die Namen, an denen der Importer die Blöcke erkennt; ein geänderter
  Name macht aus einem bearbeitbaren Block eine Textwüste.
- **Die Tabellenstruktur.** Jeder Inhalt liegt in seiner eigenen `<table>` mit Block-Klasse. Zwei
  Absätze in einer Tabelle sind im Editor ein Block, den niemand einzeln verschieben kann.
- **`width:600px`** auf `row-content`. 600px ist die Breite, mit der alle Clients rechnen.
- **Inline-Styles.** Das `<style>`-Element im `head` trägt nur den Reset; alles Sichtbare steht
  inline am Element. Eine Klasse im Kopfbereich überlebt weder den Import noch Outlook.

## Anpassungen, die sich lohnen

- **Zeile weglassen:** die ganze `<table class="row row-N">` samt Inhalt löschen. Die Nummerierung
  muss nicht lückenlos sein.
- **Zeile wiederholen:** eine `row` kopieren und die Nummer erhöhen — so entstehen mehrere
  Textabschnitte oder mehrere Bilder.
- **Einspaltig statt zweispaltig:** in Zeile 6 die zweite `<td class="column column-2">` löschen und
  bei der ersten `width="100%"` setzen, Padding rechts auf 40px.
- **Drei Spalten:** nur mit sehr kurzen Texten, `width="33.3333%"`, Klassen `column-1` bis
  `column-3`. Ab vier Spalten nur noch Zahlen oder Icons.
- **Dunkles Design:** Seitenhintergrund `#0F1117`, Flächen `#161925` und `#0B0D13`, Überschriften
  `#FFFFFF`, Fließtext `#D1D5DB`, gedämpfter Text `#A3AAB8`. Wichtig: **jede** Textfarbe explizit
  setzen — ein Client, der eine fehlende Farbe auf Schwarz voreinstellt, macht die E-Mail
  unlesbar. Und das Logo braucht eine Variante, die auf dunklem Grund funktioniert.

## Nach dem Import prüfen

1. Ist jeder Abschnitt ein **eigener** Block, den man im Editor anklicken und verschieben kann? Ein
   Abschnitt, der als eine Textwüste ankommt, ist der eine Fehler, den dieses Template vermeidet —
   und der Hinweis, dass die Struktur einer Zeile verändert wurde.
2. Stehen die vier Platzhalter noch wörtlich da, unaufgelöst?
3. Werden Logo und Bild angezeigt, oder ist die URL nicht öffentlich erreichbar?
4. Ist der Button ein Button-Block und kein verlinkter Text?
5. Stimmen die Innenabstände? Der Importer normalisiert Paddings, und mit jedem weiteren
   HTML-Durchlauf verschieben sie sich weiter. Kleine Korrekturen im Editor sind normal — dafür ist
   der Import auch nur der **Eingang**: jede weitere Änderung läuft danach über die Block-Werkzeuge
   (`email-paragraph-add`, `email-text-write`, `email-image-write`, die `*-style-write`-Familie) und
   kostet keinen weiteren HTML-Durchlauf.

## Was das Template bewusst nicht hat

- **Keine versteckte Preheader-Zeile.** Das übliche `display:none`-Element kommt beim Import
  unvorhersehbar zurück — im schlechtesten Fall als sichtbarer leerer Block. Statt dessen steht in
  Zeile 1 eine sichtbare, gestaltete Vorschauzeile, die denselben Zweck erfüllt und ein
  bearbeitbarer Block ist.
- **Kein VML-Button für Outlook.** Der `<a>`-Button mit Padding wird von Outlook rechteckig statt
  rund dargestellt, sonst korrekt. Die VML-Variante rundet dort mit, kommt aber als eigenes
  HTML-Element durch den Import und ist dann nicht mehr als Button bearbeitbar. Runde Ecken in
  Outlook sind das nicht wert; wer sie braucht, ergänzt den Button im Editor.
- **Keine Web-Fonts.** Sie fallen beim Import weg, und ein Fallback, der erst im Postfach greift,
  ist keine Gestaltung. `Helvetica, Arial, sans-serif` sieht überall gleich aus.
- **Keine Hintergrundbilder in Zeilen.** Fallen beim Import ebenfalls weg.
