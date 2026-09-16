# Die Werkzeuge dieses Skills — Wofür, Nicht, Stolperer

Den vollständigen Wortlaut jeder Beschreibung und jedes Parameters, wie der Server ihn veröffentlicht,
trägt [contracts.md](contracts.md); hier steht die Deutung.

Die Werkzeugbeschreibungen, die der Server ausliefert, sind **Verträge, keine Handbücher**. Hier
steht, woran man sich stößt, wenn man eines einzeln in die Hand nimmt; der Ablauf steht in
`../SKILL.md`. `R` liest nur · `D` löscht ohne Undo · `I` ein zweiter gleicher Aufruf ändert nichts
mehr.

**⚠ Nicht auf Production** — dort noch nicht freigeschaltet. Wer auf Production arbeitet und eines
aufruft, bekommt „unknown tool"; das ist kein Fehler, sondern die Freigabe steht aus.

| Werkzeug | | Wofür |
| --- | --- | --- |
| `email-split-test-get` | R I | Den ganzen Test lesen — über `campaignId` **oder** die `emailId` eines Arms. |
| `email-split-test-variant-add` | | Testarm anlegen, leer oder als Kopie (`copyFromEmailId`). |
| `email-split-test-variant-update` | I | Name, Betreff, Pre-Header **eines Arms** — die einzige Stelle dafür. |
| `email-split-test-variant-remove` | D | Arm entfernen; seine E-Mail ist damit weg. |
| `email-split-test-configure` | I | Testgröße, Zeitraum, Gewinner-Kriterium. Nicht: ob es ein Splittest ist. |

Der Splittest selbst entsteht bei `email-newsletter-draft-create` mit `splitTest` (Skill
`newsletter`); die vier Schreibwerkzeuge nehmen `campaignId`, und die ID entscheidet über die
Kampagnenart — `email-split-test-get` nimmt wahlweise auch die `emailId` eines Arms. Jedes nimmt
optional `accountId` (ein Unterkonto).

### `email-split-test-get`
**Wofür:** den Test ansehen, ohne ihn anzufassen — `testSizePercent`, `testDurationHours`,
`winnerBy`, `hasStarted`, dazu jeden Arm mit `emailId`, `label`, `name`, `subject` und `editorUrl`,
sowie `variantCount`, `sharePerVariantPercent` und `needsMoreVariants`.

**Zwei Wege hinein, genau einer pro Aufruf.** `campaignId` ist der Test selbst. `emailId` ist **ein
Arm** — die Zahl aus der Editor-URL, die jemand gerade offen hat — und die Antwort sagt, zu welchem
Test er gehört und welche Geschwister er hat. Das ist der Weg von einer E-Mail zurück zum Test und
damit zu `editorUrl` und `campaignId`, mit denen sich beide bearbeiten lassen. Beide zusammen werden
abgewiesen: sie können verschiedene Tests meinen, und dieses Werkzeug wählt nicht aus.

**Nicht:** die Ergebnisse des laufenden Tests — die stehen in der App, `statisticsUrl` aus
`email-newsletter-get` führt hin. **Stolperer:** Dieselbe Antwort geben auch die vier
Schreibwerkzeuge zurück; wer gerade eines aufgerufen hat, braucht diesen Aufruf nicht noch einmal.
Eine Kampagne, die kein Splittest ist, wird abgewiesen statt mit einem leeren Test beantwortet.

### `email-split-test-variant-add`
**Wofür:** zweiter und weiterer Arm. **Nicht:** die Test-Einstellungen. **Stolperer:** Fast immer
`copyFromEmailId` (die `emailId` eines Arms aus `splitTestVariants`) — eine Kopie trägt den Inhalt
des Originals und ist der Weg, *eine* Änderung zu messen; ein leerer Arm gegen einen fertigen misst
nichts. Nach dem Start gesperrt.

### `email-split-test-variant-update`
**Wofür:** Name, Betreff, Pre-Header (≤ 120 Zeichen; leer entfernt, weggelassen behält) **eines
Arms**, adressiert per `emailId` aus `splitTestVariants`. **Nicht:** der Körper (Baustein-Werkzeuge
über die `editorUrl` des Arms, Skill `email`). **Stolperer:** Macht die `contentRevision` dieses
Arms ungültig. Nach dem Start gesperrt. Ein leerer Betreff wird abgewiesen — und ein Betreff kommt
vom Menschen, nie erfunden.

### `email-split-test-variant-remove`
**Wofür:** Arm entfernen. **Stolperer:** Die E-Mail des Arms ist damit weg, ohne Undo. Der letzte Arm
bleibt. Nach dem Start gesperrt. Vorher zeigen, welcher Arm gemeint ist — Label und Betreff.

### `email-split-test-configure`
**Wofür:** `testSizePercent` (2–98, der Anteil der Zielgruppe für die Arme; der Rest bekommt den
Gewinner), `testDurationHours` (1–27777; die App bietet dieselbe Spanne als Stunden, Tage oder
Monate), `winnerBy` (`opens` = höchste Öffnungsrate, `clicks` = meiste eindeutige Klicks,
`conversions`, `revenue`). Weggelassen heißt behalten. **Nicht:** ob es ein Splittest ist.
**Stolperer:** `conversions`/`revenue` nur mit Conversion-Pixel, sonst abgewiesen. Nach dem Start
gesperrt.
