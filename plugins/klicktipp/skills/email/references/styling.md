# Gestaltung

Wann du hier landest: Farben, Abstände, Rahmen, Breiten, Ausrichtung oder Schrift sollen sich ändern.
Für eine reine Textänderung brauchst du diese Datei nicht — dafür reicht `email-text-write`, das die
Gestaltung nicht anfasst.

**Gestaltung geht inzwischen — in benannten Werten, nie in CSS.** Vier Ebenen für alles, was jeder
Baustein hat (Seite, Zeile, Spalte, Baustein), und drei Werkzeuge für das, was **nur eine Art** hat:
die Höhe eines Abstands, Linie und Breite einer Trennlinie, das Aussehen eines Buttons. Ein
artgebundenes Werkzeug auf einer anderen Art wird abgelehnt — eine Überschrift hat keine Höhe.
Zusammen setzen sie Farben, Innenabstände, Rahmen, Ausrichtung, Breiten, Eckenradien und die
Sichtbarkeit je Gerät. Eine Farbe ist
`#RRGGBB`, `#RGB` oder `transparent`, ein Abstand eine ganze Pixelzahl 0–400, eine Breite 320–1440,
ein Rahmen `1px solid #000000`. Eine CSS-Deklaration wird abgelehnt — sie könnte
`background-image: url(...)` in die E-Mail tragen. Jedes Werkzeug schreibt nur, was du benennst;
alles andere bleibt. Style-Schreibungen sind **absolut**: „mach den Hintergrund weiß" braucht keine
Lesung, „acht Pixel mehr Abstand" schon — dafür ist `styleOutline` da.

**Im `styleOutline` trägt ein Baustein zwei Karten.** `style` sind Außenabstand und Ausrichtung, die
jeder Baustein hat; `kindStyle` ist das, was nur diese Art hat — die Höhe eines Abstandhalters, die
Linie einer Trennlinie, der ganze Look eines Buttons. Getrennt, weil beide ein `paddingTop` führen
und das nicht derselbe Abstand ist: einmal um den Button herum, einmal darin. `kindStyle` ist `null`
bei jeder Art ohne eigenes Stil-Werkzeug. Eine leere Karte heißt „hier ist nichts gesetzt", nicht
„hier geht nichts": der Editor legt seine Voreinstellungen erst beim Rendern an, nicht ins Dokument.

Was weiterhin **nicht** geht, sagst du offen, statt es zu umgehen: die Schriftart, die Spaltenbreiten
einer bestehenden Zeile (die Spalten einer Zeile sind gleich breit; eine schiefe Teilung entsteht im
Editor), eine Zeile entfernen, und die **Breite eines Bildes oder Videos** — die steckt im Dokument
in zwei gekoppelten Werten plus einem Klassen-Token, und eines davon allein zu setzen bringt Editor
und Darstellung auseinander; dafür ist der Editor der Weg. Auch die Typografie eines Textbausteins
gehört nicht hierher: sie steckt in seinem eigenen Markup, also in `email-text-write` — sie an zwei
Stellen anzubieten hieße, zwei Antworten auf eine Frage zu haben.

**Welches Feld welche Bausteinart hat, welches Werkzeug es schreibt und worauf bei ihr zu achten
ist, steht je Baustein in `references/blocks/` — eine Datei je Art.** Lies die eine, um die es
geht, statt alle. Der Index ist `references/blocks/README.md`.
