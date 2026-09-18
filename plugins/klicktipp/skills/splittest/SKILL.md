---
name: splittest
description: Splittests (A/B-Tests) in KlickTipp — anlegen, Varianten hinzufuegen und kopieren, Betreffzeilen je Variante setzen, Varianten entfernen, und was sich aendert, sobald ein Newsletter einer ist. Nutze diesen Skill, wenn ein Splittest, A/B-Test oder Variantentest angelegt oder geaendert werden soll, wenn "zwei Betreffzeilen testen" oder "welche Version kommt besser an" gefragt ist, wenn Varianten oder ein Gewinner zur Sprache kommen, und immer dann, wenn ein Werkzeug einen Newsletter mit "split_test_not_supported" oder "is not a split test" abweist — das ist fast nie ein Fehler, sondern die falsche Adressierung. Fuer den normalen Newsletter-Lebenszyklus ist der Skill `newsletter` zustaendig, fuer den Inhalt einer Variante der Skill `email`.
prerequisites: None
---

# KlickTipp Splittests

Ein Splittest verschickt mehrere Fassungen derselben Aussendung an einen Teil der Zielgruppe,
misst eine Weile, und schickt dann die erfolgreichere an den Rest.

## Die eine Sache, die alles andere erklärt

**Ein Splittest-Newsletter hat keine einzelne E-Mail.** Jede Testvariante *ist* eine eigene E-Mail.

Daraus folgt fast jede Besonderheit unten. `emailId` und `contentUrl` sind `null`.
`email-newsletter-draft-update` weist einen Betreff ab — er hätte keine Variante, zu der er gehört.
Jede Variante wird über ihre eigene `editorUrl` angesprochen, die `email-newsletter-get` in
`splitTestVariants` zurückgibt.

Wenn ein Werkzeug mit `split_test_not_supported` antwortet, ist das **kein Fehler**: es sagt, dass
die Anfrage an den Newsletter ging, wo sie an eine Variante gehört hätte. Die Antwort enthält eine
`appUrl` für den Fall, dass etwas nur in der App geht.

## Anlegen — und warum nur dort

`email-newsletter-draft-create` nimmt ein `splitTest`-Objekt:

| Feld | Bedeutung |
| --- | --- |
| `testSizePercent` | 2–98. Anteil der Zielgruppe, der die Testvarianten bekommt. Der Schieberegler in der App deckt genau diese Spanne ab und steht anfangs auf 20. |
| `testDurationHours` | 1–27777 Stunden. Die App bietet dieselbe Spanne als Stunden, Tage oder Monate an. |
| `winnerBy` | `opens` (höchste Öffnungsrate), `clicks` (meiste eindeutige Klicks), `conversions` (meiste eindeutige Conversions), `revenue` (höchster Umsatz). |

**Alle drei sind Pflicht, und KlickTipp hat für keines davon einen Standardwert.** Was der Nutzer
nicht genannt hat, entscheidest *du* — und diese drei Werte entscheiden, welcher Anteil echter
Empfänger eine Testversion bekommt, wie lange gewartet wird und woran der Gewinner festgemacht wird.
Das ist keine Gestaltungsfrage, bei der du vorangehen sollst, sondern eine Festlegung über die
Zielgruppe.

**Frag die drei in *einer* Frage ab, bevor du anlegst.** Nur wenn der Nutzer nicht antworten will
oder „mach einfach" sagt, wählst du selbst — und nennst deine Wahl dann als *deine* Wahl.
**Nenne eigene Werte nie „Standardwerte".** Genau das ist passiert: ein Test wurde mit 20 %, 24
Stunden und Öffnungsrate angelegt und die drei als Standard gemeldet, obwohl niemand sie gesetzt
hatte. Nachträglich änderbar sind sie über `email-split-test-configure` — aber nur, solange der Test
nicht gestartet ist, und der Nutzer muss wissen, dass er etwas zu ändern hat.

Ein Anhaltspunkt, falls du wählen musst: der Schieberegler der App steht anfangs auf 20 %. Für Dauer
und Kriterium gibt es keine Entsprechung — die stellt in der App immer ein Mensch ein.

### Zwei Berechtigungen, die vorher greifen

**Splittests sind ein Premium-Feature.** Ein Konto ohne `klicktipp premium` bekommt eine Absage,
bevor irgendetwas angelegt wird — dann bleibt nur der normale Newsletter.

**`conversions` und `revenue` brauchen zusätzlich den Conversion-Pixel.** Beide werden darüber
gemessen; ohne ihn lässt die App sie gar nicht erst im Dropdown erscheinen, und die Werkzeuge
weisen sie ab. `opens` und `clicks` stehen immer zur Verfügung.

Frag also nicht nach einem Kriterium, das das Konto nicht messen kann — und wenn eine Absage kommt,
ist das keine Fehlfunktion, sondern die Ausstattung des Kontos.

Alle drei lassen sich später mit `email-split-test-configure` ändern, solange der Test nicht
gestartet ist.

**Diese Entscheidung fällt beim Anlegen und nie danach — in beide Richtungen.** Der Test ist ein
eigenes Objekt, an das die Kampagne bei der Erzeugung gebunden wird. Ein normaler Newsletter wird
keiner mehr, und ein Splittest hört nicht auf, einer zu sein. Wer es nachträglich will, legt neu an.

Frag also **vorher**, wenn jemand „zwei Betreffzeilen ausprobieren" sagt und noch kein Newsletter
existiert. Ist er schon da, ist das die schlechte Nachricht, die früh gehört werden will.

Alle drei Felder gehören zusammen; fehlt eins, wird abgewiesen, bevor irgendetwas entsteht.

### Was danach da ist

**Genau eine Variante** — die mit dem Betreff aus dem `draft-create`. Ein Test braucht mindestens zwei,
und bis dahin lässt sich nichts verschicken. Die Antwort sagt das selbst: `needsMoreVariants: true`.

## Die Varianten

Die Varianten-Werkzeuge sprechen **die Kampagne** an, nicht den Newsletter: sie nehmen `campaignId`, und
woraufhin die ID auflöst, entscheidet über den Typ. Es gibt bewusst keinen zweiten Parameter, der
die Kampagnenart nennt — das wären zwei Angaben, die sich widersprechen können.

| Was | Womit |
| --- | --- |
| Den Test ansehen: Einstellungen, Varianten, ob er läuft | `email-split-test-get` |
| Von einer Variante zurück zum Test finden | `email-split-test-get` mit `emailId` |
| Testgröße, Zeitraum, Gewinner-Kriterium ändern | `email-split-test-configure` |
| Variante hinzufügen (leer oder als Kopie) | `email-split-test-variant-add` |
| Betreff, Pre-Header, Name einer Variante | `email-split-test-variant-update` |
| Variante entfernen | `email-split-test-variant-remove` |
| Inhalt einer Variante | Skill `email`, über die `editorUrl` dieser Variante |

Jede dieser Antworten enthält den **ganzen** Test, nicht nur die berührte Variante: Hinzufügen und
Entfernen verteilen die Anteile neu, eine Antwort über eine einzelne Variante wäre für die anderen
schon überholt.

### Kopieren, nicht leer anlegen

`copyFromEmailId` ist fast immer richtig. Eine kopierte Variante bringt den Inhalt des Originals mit,
und dann wird genau die eine Sache geändert, um die es geht.

**Eine leere Variante gegen eine fertige E-Mail misst nichts** — der Unterschied wäre der gesamte
Inhalt, und das Ergebnis sagt nur, dass Menschen lieber eine E-Mail mit Inhalt lesen. Leer anlegen
ergibt Sinn, wenn die Varianten wirklich unabhängig entstehen sollen.

**`copyFromEmailId` ist die `emailId` einer Variante *dieses* Tests** — aus `splitTestVariants`, nicht
die ID des Newsletters, der als Vorlage gedient hat. Ein fremder Newsletter wird abgewiesen mit
„Email … is not a test variant of campaign …". Das ist kein Fehler des Werkzeugs, sondern die falsche
Zahl: `email-split-test-get` (oder `email-newsletter-get`) nennt die richtigen.

### Den Inhalt einer Variante in einem Zug schreiben

Eine Variante ist eine E-Mail, und sein Körper entsteht über den Skill `email` mit der `editorUrl` dieser
Variante. **Dafür `email-content-import` nehmen, nicht Baustein für Baustein.**

Der Grund ist nicht Geschwindigkeit, sondern das Ergebnis: Ein Block, der einzeln hinzugefügt wird,
übernimmt sein Aussehen vom **ersten Block gleicher Art in der Spalte** — nicht vom Nachbarn über
der Einfügestelle. Zehn Absätze nacheinander eingefügt bekommen deshalb alle dasselbe Padding, und
der Rhythmus des Entwurfs, dessen Abstände sich von Abschnitt zu Abschnitt unterscheiden, ist weg.
Trenner und Zwischenüberschriften, die eine Vorlage zwischen ihren Textblöcken hat, entstehen dabei
ohnehin nicht.

`email-content-import` baut das Dokument in einem Aufruf und in einer Revision. Danach einzelne
Stellen mit `email-text-write` ändern — das schreibt in vorhandene Blöcke und rührt die Gestaltung
nicht an. Die `*-add`-Werkzeuge sind für einen einzelnen zusätzlichen Block gedacht, nicht dafür,
eine E-Mail zusammenzusetzen.

Das gilt für jede E-Mail, fällt bei Splittests aber besonders auf: Variante A wird importiert, Variante B
kopiert, und jede nachträgliche Baustein-Reihe macht die beiden Varianten in etwas unterschiedlich, das
der Test nicht messen wollte.

### Ein Test testet eine Sache

Das ist keine Regel des Werkzeugs, sondern der Grund, warum man testet. Zwei Varianten, die sich in
Betreff *und* Inhalt *und* Absendezeit unterscheiden, liefern eine Zahl, aus der niemand ableiten
kann, was sie verursacht hat. Wenn jemand mehrere Änderungen auf einmal will, sag es — und lass
ihn entscheiden.

Der häufigste Fall ist der Betreff, und dafür reicht: kopieren, dann
`email-split-test-variant-update` mit dem neuen `subject`.

### Einstellungen nachträglich ändern

`email-split-test-configure` schreibt genau die drei Felder, die der Dialog in KlickTipp zeigt:
`testSizePercent`, `testDurationHours`, `winnerBy`. Weggelassenes bleibt, wie es ist; ein Aufruf
ohne eine einzige Änderung wird abgewiesen.

Was sich hier **nicht** ändern lässt, ist, ob die Kampagne überhaupt ein Splittest ist — das steht
beim Anlegen fest.

### Zwei Sperren

Ein **gestarteter** Test lässt seine Varianten nicht mehr ändern — sie beschreiben, was schon verschickt
wurde. Und der **letzte** Variante lässt sich nicht entfernen.

`variant-remove` löscht die E-Mail dieser Variante **mit ihrem Inhalt**, und diese Werkzeuge machen das
nicht rückgängig. Zeig vorher, welche Variante gemeint ist: Label und Betreff stehen in
`splitTestVariants`.

## Lesen

**Jede Variante bringt ihre `contentRevision` mit.** Du musst sie also **nicht** einzeln lesen, bevor
du in sie schreibst: `email-newsletter-get` beziehungsweise `email-split-test-get` liefert neben
`editorUrl` gleich den Token, an den jeder Schreibvorgang gebunden ist. Das spart pro Variante einen
Aufruf — und ein Aufruf kostet 15–30 Sekunden, fast alles davon Denkzeit des Modells. Lies eine
Variante nur, wenn du ihren **Inhalt** brauchst (Bausteine ändern, uuids holen); zum Befüllen einer
frisch angelegten Variante brauchst du ihn nicht.

**`email-split-test-get` zeigt den Test als Ganzes** und schreibt nichts: `testSizePercent`,
`testDurationHours`, `winnerBy`, `hasStarted`, dazu jede Variante und `needsMoreVariants`. Das ist die
Antwort auf „wie ist der Test eingestellt" und der Blick, bevor etwas geändert wird. Dieselbe
Antwort liefern auch die vier Schreibwerkzeuge — wer gerade eines aufgerufen hat, hat sie schon.

Es nimmt `campaignId` **oder** die `emailId` einer Variante, genau eines von beiden. Der zweite Weg ist
der Rückweg: Wer nur eine E-Mail vor sich hat — die Zahl aus einer Editor-URL — bekommt den Test
dahinter samt `campaignId` und den `editorUrl` aller Varianten und kann von dort aus weiterarbeiten. Ohne
ihn führte von einer Variante kein Weg zurück zum Test.

`email-newsletter-get` liefert `splitTestVariants` — pro Variante `emailId`, `label` (das „A", „B", das
auch die App zeigt), `name`, `subject` und `editorUrl`. Für die Varianten allein reicht das; die
Einstellungen des Tests stehen dort nicht.

Für einen Splittest sind `emailId`, `contentUrl` und `metadata.subject` **null**, und
`deliveryConfiguration` gehört zu einer Variante: sie wird ohne `editorUrl` abgewiesen, statt für eine
Variante beantwortet zu werden, den niemand gewählt hat.

## Was nicht über diese Werkzeuge geht

- Absender, Antwortadresse und Signatur **pro Variante** — das ist die App.
- Testversand und Aktivierung eines Splittests.
- Den Gewinner vorzeitig küren oder das Kriterium nachträglich ändern.
- Einen bestehenden Newsletter in einen Splittest verwandeln, oder umgekehrt.

In all diesen Fällen: sag es klar und verweise auf die `appUrl` aus der Antwort.

**Der Abschluss gehört der App, und das ändert sich auch nicht**, wenn diese Werkzeuge überall
verfügbar sind. `email-newsletter-delivery-configure`, `email-newsletter-test-send` und
`email-newsletter-send` weisen einen Splittest in *jeder* Umgebung ab — nicht weil etwas fehlt,
sondern weil keines von ihnen eine Variante auswählen kann. Der Weg von hier ist also: anlegen, Varianten
bauen, Inhalte schreiben — und für Absender, Testversand und Freigabe in die Oberfläche wechseln.
Kündige einen Splittest deshalb nie als „verschicke ich dir" an.

## Die Werkzeuge im Einzelnen

Die vier Variante- und Einstellungs-Werkzeuge mit Wertebereichen und Stolperern stehen in
[references/tools.md](references/tools.md); ihre veröffentlichten Verträge Wort für Wort, mit jedem
Parameter, in [references/contracts.md](references/contracts.md).
