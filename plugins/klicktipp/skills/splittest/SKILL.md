---
name: splittest
description: Splittests (A/B-Tests) in KlickTipp — anlegen, Testarme hinzufuegen und kopieren, Betreffzeilen je Arm setzen, Arme entfernen, und was sich aendert, sobald ein Newsletter einer ist. Nutze diesen Skill, wenn ein Splittest, A/B-Test oder Variantentest angelegt oder geaendert werden soll, wenn "zwei Betreffzeilen testen" oder "welche Version kommt besser an" gefragt ist, wenn Testarme, Varianten oder ein Gewinner zur Sprache kommen, und immer dann, wenn ein Werkzeug einen Newsletter mit "split_test_not_supported" oder "is not a split test" abweist — das ist fast nie ein Fehler, sondern die falsche Adressierung. Fuer den normalen Newsletter-Lebenszyklus ist der Skill `newsletter` zustaendig, fuer den Inhalt eines Arms der Skill `email`.
prerequisites: None
---

# KlickTipp Splittests

Ein Splittest verschickt mehrere Fassungen derselben Aussendung an einen Teil der Zielgruppe,
misst eine Weile, und schickt dann die erfolgreichere an den Rest.

## Die eine Sache, die alles andere erklärt

**Ein Splittest-Newsletter hat keine einzelne E-Mail.** Jeder Testarm *ist* eine eigene E-Mail.

Daraus folgt fast jede Besonderheit unten. `emailId` und `contentUrl` sind `null`.
`email-newsletter-draft-update` weist einen Betreff ab — er hätte keinen Arm, zu dem er gehört.
Jeder Arm wird über seine eigene `editorUrl` angesprochen, die `email-newsletter-get` in
`splitTestVariants` zurückgibt.

Wenn ein Werkzeug mit `split_test_not_supported` antwortet, ist das **kein Fehler**: es sagt, dass
die Anfrage an den Newsletter ging, wo sie an einen Arm gehört hätte. Die Antwort enthält eine
`appUrl` für den Fall, dass etwas nur in der App geht.

## Anlegen — und warum nur dort

`email-newsletter-draft-create` nimmt ein `splitTest`-Objekt:

| Feld | Bedeutung |
| --- | --- |
| `testSizePercent` | 2–98. Anteil der Zielgruppe, der die Testarme bekommt. Der Schieberegler in der App deckt genau diese Spanne ab und steht anfangs auf 20. |
| `testDurationHours` | 1–27777 Stunden. Die App bietet dieselbe Spanne als Stunden, Tage oder Monate an. |
| `winnerBy` | `opens` (höchste Öffnungsrate), `clicks` (meiste eindeutige Klicks), `conversions` (meiste eindeutige Conversions), `revenue` (höchster Umsatz). |

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

**Genau ein Arm** — der mit dem Betreff aus dem `draft-create`. Ein Test braucht mindestens zwei,
und bis dahin lässt sich nichts verschicken. Die Antwort sagt das selbst: `needsMoreVariants: true`.

## Die Arme

Die Arm-Werkzeuge sprechen **die Kampagne** an, nicht den Newsletter: sie nehmen `campaignId`, und
woraufhin die ID auflöst, entscheidet über den Typ. Es gibt bewusst keinen zweiten Parameter, der
die Kampagnenart nennt — das wären zwei Angaben, die sich widersprechen können.

| Was | Womit |
| --- | --- |
| Testgröße, Zeitraum, Gewinner-Kriterium ändern | `email-split-test-configure` |
| Arm hinzufügen (leer oder als Kopie) | `email-split-test-variant-add` |
| Betreff, Pre-Header, Name eines Arms | `email-split-test-variant-update` |
| Arm entfernen | `email-split-test-variant-remove` |
| Inhalt eines Arms | Skill `email`, über die `editorUrl` dieses Arms |

Jede dieser Antworten enthält den **ganzen** Test, nicht nur den berührten Arm: Hinzufügen und
Entfernen verteilen die Anteile neu, eine Antwort über einen einzelnen Arm wäre für die anderen
schon überholt.

### Kopieren, nicht leer anlegen

`copyFromEmailId` ist fast immer richtig. Ein kopierter Arm bringt den Inhalt des Originals mit,
und dann wird genau die eine Sache geändert, um die es geht.

**Ein leerer Arm gegen eine fertige E-Mail misst nichts** — der Unterschied wäre der gesamte
Inhalt, und das Ergebnis sagt nur, dass Menschen lieber eine E-Mail mit Inhalt lesen. Leer anlegen
ergibt Sinn, wenn die Arme wirklich unabhängig entstehen sollen.

### Ein Test testet eine Sache

Das ist keine Regel des Werkzeugs, sondern der Grund, warum man testet. Zwei Arme, die sich in
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

Ein **gestarteter** Test lässt seine Arme nicht mehr ändern — sie beschreiben, was schon verschickt
wurde. Und der **letzte** Arm lässt sich nicht entfernen.

`variant-remove` löscht die E-Mail dieses Arms **mit ihrem Inhalt**, und diese Werkzeuge machen das
nicht rückgängig. Zeig vorher, welcher Arm gemeint ist: Label und Betreff stehen in
`splitTestVariants`.

## Lesen

`email-newsletter-get` liefert `splitTestVariants` — pro Arm `emailId`, `label` (das „A", „B", das
auch die App zeigt), `name`, `subject` und `editorUrl`.

Für einen Splittest sind `emailId`, `contentUrl` und `metadata.subject` **null**, und
`deliveryConfiguration` gehört zu einem Arm: sie wird ohne `editorUrl` abgewiesen, statt für einen
Arm beantwortet zu werden, den niemand gewählt hat.

## Was nicht über diese Werkzeuge geht

- Absender, Antwortadresse und Signatur **pro Arm** — das ist die App.
- Testversand und Aktivierung eines Splittests.
- Den Gewinner vorzeitig küren oder das Kriterium nachträglich ändern.
- Einen bestehenden Newsletter in einen Splittest verwandeln, oder umgekehrt.

In all diesen Fällen: sag es klar und verweise auf die `appUrl` aus der Antwort.
