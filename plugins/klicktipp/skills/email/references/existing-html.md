# Bestehendes HTML bearbeiten, und HTML für den Import schreiben

Wann du hier landest: dir liegt fertiges E-Mail-HTML vor — aus einer Agentur, einem anderen Werkzeug,
einer Datei — und es soll geändert oder importiert werden. Für einen Newsletter, der als Dokument
schon existiert, ist das der falsche Weg; dann führt `replace-email-editor-content-from-email` oder
`replace-email-editor-content-from-document` verlustfrei ans Ziel.

Liegt bereits E-Mail-HTML vor, ist die Aufgabe eine Inhaltsänderung, kein Redesign. Ändere
ausschließlich das, was inhaltlich beauftragt wurde. Das übrige Dokument bleibt Zeichen für
Zeichen identisch.

Was Inhalt ist und geändert werden darf:

- Texte, Überschriften, Listeneinträge, Tabellenzellen, eine sichtbare Vorschauzeile im Dokument.
  (Das **Pre-Header-Feld** der E-Mail liegt nicht im Dokument — es wird über
  `update-newsletter-draft` gesetzt, Feld `preheader`.)
- Button-Labels und Link-Ziele, `href`, `alt`-Texte, Bild-URLs.
- KlickTipp-Variablen und Systemlinks.

Was Design ist und unangetastet bleibt:

- Struktur und Reihenfolge von Zeilen, Spalten und Blöcken; Spaltenanzahl und -breiten.
- Alle Klassen, inklusive der `block-[n]`-Nummerierung, und alle Attribute wie `width`, `align`,
  `cellpadding`.
- Inline-Styles, Farben, Schriftarten, Schriftgrößen, Zeilenhöhen, Padding, Abstände, Rahmen.
- Spacer, Divider, Wrapper-Tabellen — auch scheinbar überflüssige.

Zusätzlich gilt beim Bearbeiten:

- Kein Aufräumen nebenbei: keine Neuformatierung des Codes, keine Umsortierung von Attributen,
  keine Vereinheitlichung von Styles, kein Entfernen „unnötiger" Verschachtelung, keine
  Neunummerierung von Blöcken.
- Verstößt das vorhandene HTML gegen Regeln dieses Skills, etwa eine `http`-Bild-URL, ein
  Background-Image oder ein `menu_block`: nicht eigenmächtig umbauen, sondern nach dem Code-Block
  in einem Satz benennen. Ausnahme sind Fehler, die Import oder Speicherung zwingend brechen —
  fehlender `DOCTYPE`, fehlendes `<meta charset="UTF-8">`, fehlende Pflicht-Footer-Variablen sowie
  invalides HTML wie ein nicht geschlossenes oder überkreuztes Tag. Diese korrigieren und die
  Korrektur benennen.
- Braucht der neue Inhalt mehr Platz, als das Layout hergibt, wird der Text angepasst, nicht das
  Layout. Geht das nicht sinnvoll, den Konflikt benennen und nach der gewünschten Layoutänderung
  fragen.
- Design nur ändern, wenn es ausdrücklich verlangt ist, zum Beispiel „mach den Button grün",
  „zwei Spalten statt einer" oder „mehr Abstand über der Überschrift". Dann genau diese Änderung
  umsetzen und nichts darüber hinaus.
- Ist unklar, ob eine Anweisung Inhalt oder Design meint, als Inhalt behandeln und die
  Design-Frage stellen.

Wenn kein bestehendes HTML vorliegt, gestaltest du frei nach den Regeln unten.

## Inhalt

- Import-HTML schreiben
- Was der Import tut, meldet und kostet

## Import-HTML schreiben

Sobald du HTML erzeugst, das durch `replace-email-editor-content-from-html` geht — beim Bearbeiten vorhandenen
E-Mail-HTMLs oder wenn du fremdes HTML importfähig machst —, **lies zuerst `references/html-authoring.md`**.
Dort stehen die zwingenden Regeln: Grundgerüst, das Zwölfer-Grid, die Blockklassen des Editors,
was mit CSS und Bildern erlaubt ist, die KlickTipp-Variablen, der Pflicht-Footer, valides HTML und
der Qualitätscheck vor der Ausgabe.

Sie sind nicht optional und nicht zusammenfassbar: HTML, das sie verletzt, importiert der Editor
entweder gar nicht oder als einen Klumpen, der sich nicht mehr bearbeiten lässt. Verlass dich
nicht darauf, sie zu kennen — sie sind fünf Bildschirmseiten lang, und der Unterschied steckt in
den Details.

Für Änderungen über die Bausteinwerkzeuge gelten sie **nicht**: dort wird nichts konvertiert.

## Was der Import tut, meldet und kostet

**Was `importWarnings` in einer Leseantwort sagt.** Es ist die Kostenliste **eines HTML-Imports** auf
genau diesen Newsletter — und nur dafür. Sie gilt nicht für das Bearbeiten: dort wird nichts
konvertiert, also verliert kein Baustein Gestaltung oder Bearbeitbarkeit. Lies sie dem Nutzer vor,
**bevor** du importierst, nie als Kommentar zu einer Änderung. Leer heißt: eine Konvertierung würde
hier nichts kosten.

**Ein Import über bestehenden Inhalt wird beim ersten Aufruf abgewiesen** — mit Absicht. Die
Antwort zählt auf, wie viele Zeilen und Bausteine der Newsletter hat und welcher Art sie sind, und
ändert nichts. Erst ein zweiter Aufruf mit `replaceExistingContent: true` konvertiert. Zeig dem
Nutzer diese Liste und lass ihn entscheiden: ein Import über einen gestalteten Newsletter nimmt
jeden Baustein, sein Layout und die Identität jedes Blocks mit, und es gibt kein Zurück. Ein leerer
Entwurf braucht keine Bestätigung.

**Der Import veröffentlicht nicht.** Er speichert den Entwurf; der Versandinhalt ändert sich erst
durch `publish-newsletter-email-content`. Die Antwort nennt genau das in `nextAction` — lies es, statt nach
dem Import „fertig" zu melden.

**Was ein HTML-Import kostet** (`replace-email-editor-content-from-html`). Ein Import
nimmt gerendertes HTML und nie das Dokument; je Baustein kommt zurück: Trennlinie als
gestaltete Linie, Menü als Links, Social-Links und Icons als Bilder mit Links, Tabelle als
einfaches Markup, Video als Vorschaubild mit Link, eigenes HTML, Karussell, Merge-Inhalt und
Add-ons (Countdown, Kontaktkarte, Wowing-Video, Signatur) als ihr gerendertes Ergebnis;
Web-Fonts, Zeilen-Hintergrundbilder und eigene Kopfbereich-Styles fallen weg.

**Nach dem Import sagen die `warnings` des Ergebnisses, was diese eine Konvertierung wirklich
gekostet hat** — nicht als Vorhersage, sondern gezählt auf beiden Seiten. Immer dabei: das Layout
ist neu gebaut, Zeilen, Spalten und Abstände sind danach die des Editors, und es stehen
Abstandhalter darin, die niemand geschickt hat. Dazu je eine Zeile mit Zahlen für Trennlinien,
Listen, Tabellen, Bilder und Videos, die nicht als eigener Baustein zurückkamen, samt dem Werkzeug
zum Nachziehen. Eine Tabelle, deren Zellen als `Zelle AZelle B` zusammenlaufen, steht genau dort.
Gib diese Zeilen weiter; ein „Import hat geklappt" ohne sie ist die Meldung, die den Nutzer den
Verlust erst im Editor entdecken lässt.

**Sag vorher nicht zu, was aus einem HTML wird.** Die Konvertierung macht ein externer Dienst; was
aus einer Tabelle oder einer Trennlinie wird, entscheidet nicht KlickTipp, und es kann sich ändern,
ohne dass hier etwas neu ausgeliefert wird. Die Aufzählung weiter oben ist deshalb eine Erwartung,
kein Vertrag — verbindlich ist immer erst der Bericht **nach** dem Import. Formuliere entsprechend:
„so etwas überlebt die Konvertierung erfahrungsgemäß nicht" vor dem Aufruf, und die gemessenen
Zeilen danach.

Der Import lässt **Name, Betreff und Pre-Header unberührt** — er schreibt nur das Dokument. Ein
`<title>` im importierten HTML landet nirgends, eine versteckte Preheader-Zeile wirft der Konverter
weg. Name, Betreff und Pre-Header setzt der Skill `newsletter` über seine eigenen Werkzeuge.

Und Entscheidungen wie KI-Blöcke sind nach einem Import **weg**: sie stehen nicht im HTML, kein
Vorgehen deinerseits kann sie erhalten — sag das ausdrücklich, bevor du importierst. Im Dokument stehen sie dagegen sehr wohl, und
ein Bearbeiten lässt sie unangetastet: das ist der Grund, einen gestalteten Newsletter nie über HTML
zu ändern.

**Die Liste ist eine Untergrenze, keine vollständige Aufzählung.** Nicht enthalten, aber
nachgewiesen: Abstände, Rahmen, Rundungen und Inline-Farben bleiben nicht erhalten, Innenabstände
verschieben sich mit jedem Durchlauf weiter, und das Layout wird normalisiert — Spaltenzahl,
zusätzliche Abstandsblöcke und eine geänderte Inhaltsbreite sind vorgekommen. Gib diesen Satz mit
weiter: eine Liste, die vollständig klingt, ist schlimmer als keine.
