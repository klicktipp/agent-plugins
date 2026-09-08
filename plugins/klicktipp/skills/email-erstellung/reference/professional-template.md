# Professionelles E-Mail-Template

`professional-template.html` ist eine vollständige, importfertige E-Mail. Sie ist der
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
  gegen echte, öffentlich erreichbare HTTPS-URLs. Bilder werden beim Import **nicht** in den
  Dateimanager geladen, sondern von ihrer Quelle geladen — eine interne oder passwortgeschützte URL
  bleibt im Editor leer. Das Bild ist mit `width="600"` und `max-width:600px` doppelt begrenzt; ein
  Motiv mit 1200px Breite bleibt auf Retina-Displays scharf.
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
   der Import auch nur der **Eingang**: jede weitere Änderung läuft danach über
   `email-newsletter-content-edit` und kostet nichts mehr.

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
