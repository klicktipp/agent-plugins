# Die Werkzeuge dieses Skills — Wofür, Nicht, Stolperer

Den vollständigen Wortlaut jeder Beschreibung und jedes Parameters, wie der Server ihn veröffentlicht,
trägt [contracts.md](contracts.md); hier steht die Deutung.

Die Werkzeugbeschreibungen, die der Server ausliefert, sind **Verträge, keine Handbücher**: was ein
Werkzeug tut, was es nicht anfasst, und die Konsequenz eines Schreibzugriffs. Hier steht, woran man
sich stößt, wenn man eines einzeln in die Hand nimmt; der Ablauf steht in `../SKILL.md`.

`R` liest nur · `D` löscht oder ersetzt ohne Undo · `O` erreicht etwas außerhalb des Kontos · `I` ein
zweiter gleicher Aufruf ändert nichts mehr. Jedes Werkzeug nimmt optional `accountId` (ein
Unterkonto); weggelassen heißt das Konto des Zugangs.

| Werkzeug | | Wofür |
| --- | --- | --- |
| `email-newsletter-search` | R | Liste der Newsletter, filterbar nach Name, Status, zwei Zeitfenstern; Cursor-Seiten. Der Weg von einer Editor-URL zum Newsletter. |
| `email-newsletter-get` | R | Ein Newsletter mit Projektionen: `metadata`, `audience`, `deliveryConfiguration`, `deliveryStatus`, `audienceReach`, `conversionPixel`. Kein Inhalt — der ist `email-get` (Skill `email`). |
| `email-newsletter-draft-create` | | Entwurf anlegen: Name, Betreff, Pre-Header, optional `splitTest` (Skill `splittest`). Sendet nichts. |
| `email-newsletter-draft-update` | I | Name, Notiz, Betreff, Pre-Header, Zielgruppe eines Entwurfs. Betreff/Pre-Header machen `contentRevision` ungültig. |
| `email-newsletter-draft-delete` | D | Entwurf endgültig löschen. |
| `email-newsletter-delivery-configure` | I | Absender, Antwortadresse, Versanddomain, Signatur, Link-Tracking, KlickTipp-Kopfzeile. Prüft gegen die Listen, die es selbst mitliefert. |
| `email-newsletter-test-send` | DO | Eine echte Testmail an eine beliebige Adresse; der Empfänger wird Kontakt des Kontos und als Testempfänger getaggt. Trägt den **veröffentlichten** Inhalt — vorher `email-content-publish`. |
| `email-newsletter-send` | DO | **Sendet nicht** — bereitet vor und gibt die Bestätigungs-URL, die ein Mensch in KlickTipp klickt. Der Klick erreicht echte Empfänger. |
| `email-newsletter-cancel` | D | Einen terminierten oder eben angelaufenen Versand zurücknehmen — der Newsletter wird wieder Entwurf. Nur solange `canBeCancelled`; holt nichts zurück, was schon raus ist. ⚠ nicht auf Production |
| `email-signature-search` · `email-signature-get` | R | Signaturen, die unter einen Newsletter können, mit Absenderprofil — die Kandidaten für `signatureId`. ⚠ nicht auf Production |
| `email-signature-create` · `email-signature-update` · `email-signature-content-replace` · `email-signature-delivery-configure` | / I / DI / I | Signatur anlegen (auch als Kopie), Name/Notiz/Labels, Inhaltsblock komplett ersetzen, Tags und Absenderprofil. ⚠ nicht auf Production |

## Newsletter

### `email-newsletter-cancel`
**Wofür:** einen Versand zurücknehmen, der terminiert ist oder gerade anläuft; der Newsletter wird
wieder Entwurf und erreicht niemanden weiter. **Nicht:** löschen, und **nicht** zurückholen, was
schon versendet wurde. **Stolperer:** Nur solange `deliveryStatus.canBeCancelled` `true` ist —
danach wird abgelehnt, und die Meldung sagt, dass es zu spät ist statt so zu tun als ginge es.
Ein Entwurf wird mit einem eigenen Satz abgelehnt („kein Versand zum Abbrechen"), damit du die
beiden Fälle nicht verwechselst. Braucht dieselbe Berechtigung wie das Freigeben
(„Email marketing manager"). **Frag die Person vorher** — einen bewusst eingerichteten Versand
brichst du nicht auf eigene Einschätzung ab. Wieder aktivieren geht mit `email-newsletter-send`.
Die Antwort sagt ausdrücklich, dass bereits versendete Mails unterwegs bleiben; gib diesen Satz
weiter, statt nur „abgebrochen" zu melden.

### `email-newsletter-search`
**Wofür:** die Liste; Filter `query`, `status`, `createdFrom/Before`, `sendDateFrom/Before`; Seiten
über `cursor`. **Nicht:** Betreff, Inhalt, Zielgruppe, Statistik — das ist `email-newsletter-get`.
**Stolperer:** Ein Entwurf hat kein Versanddatum und fällt in kein `sendDate`-Fenster, auch wenn ein
Termin gesetzt und abgesagt wurde. Zeitfenster sind halboffen (`From` inklusiv, `Before` exklusiv)
und wollen einen UTC-Offset (`2026-09-01T10:00:00+02:00`). Der `cursor` kommt unverändert zurück,
mit denselben Filtern; nur die Seitengröße darf sich ändern. Eine Editor-URL nennt die *E-Mail*:
`emailId` abgleichen, nicht raten. Ein Splittest hat `emailId: null`.

### `email-newsletter-get`
**Wofür:** ein Newsletter mit den Projektionen, die du brauchst: `metadata` (Name, Notiz, Labels,
Betreff), `audience`, `deliveryConfiguration` (Absender, Antwortadresse, Signatur), `deliveryStatus`
(Stand des Versands), `audienceReach` (wie viele Kontakte er jetzt erreichen würde). Ohne `include`
nur Identität und Lebenszyklus. **Nicht:** der Körper — `email-get` mit `editorUrl` oder `emailId`.
**Stolperer:** Projektionen sind alles oder nichts; eine, die nicht bedient werden kann, lässt den
ganzen Aufruf scheitern. Bei einem Splittest sind `emailId`, `contentUrl` und `metadata.subject`
null, die Arme stehen in `splitTestVariants`, und `deliveryConfiguration` braucht eine `editorUrl`
daraus. `audienceReach` ist eine Messung, kein gespeicherter Wert — und die einzige Zahl, die „wie
viele Kontakte" beantwortet. `deliveryStatus` trägt `observedAt`: Bounces und Beschwerden kommen
nach dem Versand noch nach.

### `email-newsletter-draft-create`
**Wofür:** die Hülle — Name (eindeutig im Konto), Betreff, Pre-Header (≤ 120 Zeichen, kein HTML).
**Nicht:** Inhalt, Zielgruppe, Absender, Termin. **Stolperer:** Ohne Zielgruppe heißt Zielgruppe
*alle aktiven Kontakte* (`all_contacts`). Der Betreff kommt vom Menschen, nie erfunden — er ist die
Zeile, die jeder Empfänger sieht. Der Pre-Header ist kein Teil des Dokuments: ein HTML-Import kann
ihn nicht setzen, eine versteckte Vorschauzeile im HTML fällt beim Konvertieren weg. `splitTest`
ist unumkehrbar — in beide Richtungen — und braucht Premium; `conversions`/`revenue` zusätzlich den
Conversion-Pixel.

### `email-newsletter-draft-update`
**Wofür:** Name (≤ 250), Notiz (≤ 1000, nie an Empfänger), Betreff, Pre-Header, Zielgruppe,
UTM-Kampagnenname (≤ 120).
**Nicht:** Inhalt, Absender, Termin — und keinen Splittest (dessen Betreff:
`email-split-test-variant-update`). **Stolperer:** Betreff oder Pre-Header schreiben macht jede
vorher gelesene `contentRevision` ungültig — der nächste Inhalts-Write wird als „geändert"
abgewiesen. Die Zielgruppe ersetzt die alte komplett: `mode` ist `all_contacts`, `saved_audience`
(mit `audienceId`) oder `tag_conditions` (mit `includeTagIds`/`excludeTagIds`, je `…Match` `any`
oder `all`; zusammen höchstens 50 Tags). Ein leerer `preheader` entfernt ihn, ein weggelassener
lässt ihn stehen — das gilt für jedes Feld: weggelassen heißt behalten.

`utmCampaignName` ist der Name, den KlickTipp als `utm_campaign` an die getrackten Links hängt. Er
gehört zur Kampagne, deshalb steht er hier und nicht beim Versand-Werkzeug. Leerer String heißt
„zurück zu den kontoweiten UTM-Einstellungen"; weggelassen heißt behalten. Über 120 Zeichen wird
abgelehnt, bevor irgendetwas geschrieben wird.

### `email-newsletter-draft-delete`
**Wofür:** einen Entwurf endgültig entfernen. **Nicht:** geplante, laufende, versendete Newsletter.
**Stolperer:** Kein Papierkorb. Eine Namensähnlichkeit aus der Suche ist keine Zustimmung.

### `email-newsletter-delivery-configure`
**Wofür:** Absender, Antwortadresse, Versanddomain, Signatur, Link-Tracking und die
KlickTipp-Kopfzeile; sagt, was zum Versand noch fehlt.
**Nicht:** Termin, Aktivierung. **Stolperer:** Jeder der vier Absender-Werte hat einen `…Mode` —
`explicit` (dann den Wert daneben), `account_default` oder `signature_dispatch_profile`;
weggelassen heißt behalten. `signatureId: 0` heißt „KlickTipp wählt per Tagging" und ist kein
Eintrag der Signaturliste.

Dazu zwei Schalter aus dem Panel „Erweiterte Einstellungen" derselben Seite:

- `linkTracking` — `true` heißt **Tracking an** (KlickTipp schreibt die Links um und zählt Klicks).
  Achtung beim Lesen fremder Doku: die Spalte dahinter heißt `TurnOffTrackLink` und die App
  beschriftet die Checkbox „Link-Tracking deaktivieren" — das Werkzeug dreht das um, damit `true`
  das Naheliegende bedeutet. Ohne eigene Versanddomain lässt sich Tracking **nicht** abschalten;
  der Aufruf wird abgelehnt, genau wie die App die Checkbox dann ausgraut.
- `headerLinks` — `true` setzt KlickTipps eigene Zeile über den Inhalt: Browseransicht, Abmelden,
  Spam melden. Das ist der Weg zu genau diesen drei Links; es gibt dafür keine Bausteine. (Die App
  nennt den Schalter „Vorschau für GMail aktivieren", gespeichert als `ReportSpamEnabled` — beide
  Namen beschreiben nur einen Teil davon.)

Der Pre-Header ist **kein** Teil davon: er steht zwar in der Nachbarspalte, wird aber unabhängig
gerendert und mit `email-newsletter-draft-update` als `preheader` geschrieben.

Das Werkzeug lehnt ab, **bevor** es schreibt, und nennt dabei jedes Mal die Werte, die gingen:

- `senderEmail` muss in `availableSenderAddresses` stehen. Eine Adresse, die im Konto zwar existiert,
  aber nicht als Absender taugt, wird abgewiesen — früher wurde sie gespeichert und der Newsletter
  stand mit einem Absender da, der nicht senden kann.
- `senderDomain` muss in `availableSenderDomains` stehen. Ist die Liste **leer**, wählt dieses Konto
  gar keine Domain (KlickTipp bietet das Feld erst ab zwei gültigen Domains und mit der
  Whitelabel-Berechtigung) — dann `senderDomain` weglassen, nicht eine andere raten.
- Adresse und Domain müssen **zusammenpassen**. Geprüft wird das Ergebnis, nicht der Aufruf: wer nur
  die Adresse ändert, schleppt die alte Domain mit, und genau das wird abgelehnt. Die Meldung nennt
  die Domain, die dazugehört — beides in einem Aufruf schicken.

Beide Listen stehen in der Antwort jedes Aufrufs, und der aktuelle Stand in
`email-newsletter-get` mit `include: ["deliveryConfiguration"]` (`senderDomainMode`,
`senderDomain`). Lies sie, statt Adressen oder Domains zu raten.

### `email-newsletter-test-send`
**Wofür:** eine echte Mail an eine beliebige Adresse, über dieselbe Aktion wie der Testdialog der
Oberfläche. **Nicht:** ein Versand an die Zielgruppe, und kein Blick auf den Entwurf. **Stolperer:**
Der Empfänger wird als Kontakt mit dem Testempfänger-Tag angelegt oder markiert — eine
Schreiboperation am Konto, die Automationen starten kann, also vorher sagen. Die Mail trägt den
veröffentlichten Inhalt: ein nie veröffentlichter Body wird mit
`newsletter_send_content_publish_required` abgewiesen (erst `email-content-publish`), alles andere,
was die Oberfläche vor einem Test verlangt — Betreff, Pflicht-Tags im Inhalt — mit
`newsletter_send_not_ready`; beide nennen die Gründe in `details.missingRequirements` und die
Editor-URL. Wurde nach dem Veröffentlichen geändert, wird gesendet, und die Antwort trägt
`warnings`: der Test zeigt den älteren Stand.

### `email-newsletter-send`
**Wofür:** die Vorbereitung — Prüfung, Empfängerschätzung, Bestätigungs-URL. **Nicht:** senden. Nie.
**Stolperer:** Sag danach nicht „verschickt". Geänderter, nicht veröffentlichter Inhalt wird
abgewiesen — erst `email-content-publish`. `mode` ist Pflicht (`immediate` / `scheduled`, kein
Default); `scheduledAt` ist bei `scheduled` Pflicht, bei `immediate` verboten, und trägt seinen
UTC-Offset. Ändert sich ein gebundener Wert oder läuft die URL ab, neu vorbereiten.

## Signaturen — ⚠ nicht auf Production

Dort noch nicht freigeschaltet: „unknown tool" ist kein Fehler, die Freigabe steht aus. Auf
Staging heißt die Familie `email-signature-*` (sechs Werkzeuge); die zwei Lesewerkzeuge sind auf
manchen Ständen noch als `search-signatures` / `get-signature` unterwegs.

### `email-signature-search` · `email-signature-get`
**Wofür:** Signaturen samt Absenderprofil und ob sie unter einen Newsletter können. **Stolperer:** Die
Suche lässt Unbrauchbare weg (kein Inhalt, fehlende Pflichtplatzhalter, gesperrte Absenderadresse) —
`includeUnusable` zeigt sie mit Gründen. Der Signaturtext kommt nur mit `includeContent` (HTML,
Text, transaktionale Variante), er ist kilobytegroß.

### `email-signature-create`
**Wofür:** eine Signatur anlegen — mit eigenem `content` oder als Kopie einer Signatur des Kontos
(`sourceSignatureId`): `name` und `tagIds` ersetzen die Quellwerte, mitgegebener Inhalt und
Absenderfelder überschreiben die kopierten, die digitale Visitenkarte der Quelle bleibt erhalten;
weggelassene `notes`/`metaLabels` behalten bei einer Kopie die der Quelle. **Nicht:** Newsletter
ändern, Tags oder Absenderadressen anlegen — beides muss vorher existieren. **Stolperer:** `tagIds`
ist Pflicht und braucht mindestens einen Tag, der an keiner anderen Signatur hängt; ohne
`sourceSignatureId` ist `content` Pflicht. Dazu die Platzhalterregeln unten. Die Antwort meldet nur
**Flags** (HTML da, Text da, transaktional da), nicht den Inhalt — lesen mit `email-signature-get`
und `includeContent: true`.

### `email-signature-update`
**Wofür:** Name, Notiz, Labels. **Nicht:** Inhalt, Tags, Absender. **Stolperer:** Die
Standardsignatur lässt sich nicht umbenennen. Leerer String löscht die Notiz, leeres Array die
Labels; weggelassen heißt behalten.

### `email-signature-content-replace`
**Wofür:** den **kompletten** Inhaltsblock ersetzen — HTML, Text und transaktionale Fassung — über
denselben Konvertierungs-, Prüf- und Speicherweg wie die App. **Nicht:** Name, Notiz, Labels, Tags,
Absenderprofil, Visitenkarte. **Stolperer:** Kein Undo. Transaktionale Felder ändern sich nur, wenn
das Konto sie nutzen darf. Die Antwort meldet Flags, nicht den Inhalt.

### `email-signature-delivery-configure`
**Wofür:** Tags und Absenderprofil einer Signatur. **Stolperer:** `tagIds` ersetzt die Liste; eine
normale Signatur braucht mindestens einen Tag, jeder Tag darf nur an einer Signatur hängen, nur die
Standardsignatur darf eine leere Liste. `senderProfile` nimmt Absendername und die im Konto
konfigurierten Adressen/Domains; die Antwort-Optionen gelten auch für CC, BCC und Empfänger; leere
Strings leeren optionale Felder, weggelassene bleiben.

### Die Platzhalterregeln für Signaturinhalt
Sie gelten für `create` und `content-replace` gleich, und der Server weist ab, was sie verletzt:

- **Normales HTML** braucht `%Link:Unsubscribe%` als `href` eines Links und die Adressplatzhalter
  `%User:FirstName%`, `%User:LastName%`, `%User:Street%`, `%User:Zip%`, `%User:City%`,
  `%User:Country%`. Konten, die Adressangaben weglassen dürfen, sind von den Adressplatzhaltern
  befreit — vom Abmeldelink nicht.
- **Text (plain)** braucht dieselben Platzhalter; der Abmelde-Platzhalter darf als Text stehen. Ein
  mitgegebener Text wird getrimmt und **nur gespeichert, wenn das Konto Textbearbeitung erlaubt**;
  sonst — auch wenn er fehlt oder leer ist — wird er ignoriert und aus dem HTML neu erzeugt. Erwarte
  also nicht, dass gelieferter Text unverändert zurückkommt, wenn diese Fähigkeit fehlt. Das HTML
  bleibt HTML.
- **Transaktionales HTML** braucht die Adressplatzhalter und darf `%Link:Unsubscribe%` **nicht**
  enthalten. `%Link:SubscriberInfo%` ist empfohlen, nicht Pflicht.

Die transaktionale Fassung ist kein Randfall, sondern der Grund, warum es sie gibt: sie geht an
Erstkontakte (SOI-Bestätigung), wo ein Abmeldelink von einem noch unbestätigten Abo abmelden würde.
Biete sie beim Anlegen einer Signatur aktiv an, statt zu warten, bis jemand danach fragt — siehe
[SKILL.md](../SKILL.md), Abschnitt 4.

## Antwortformen

Sechs Werkzeuge veröffentlichen ein **Output-Schema** (JSON Schema), das ein Client gegen
`structuredContent` prüfen kann: die beiden Leser, Import, Veröffentlichen, Prüfen und
`email-row-add`. Für alle anderen steht die Form der Antwort hier — und auch für die sechs ist
diese Seite die ausführlichere Quelle, weil ein Schema Felder benennt, aber nicht erklärt.
Jede Antwort kommt als `structuredContent` und als dieselbe kompakte JSON im Text. Ein `*`
markiert Felder, die immer da sind; alles andere ist nur da, wenn es angefordert wurde oder
zutrifft. Nicht angeforderte Projektionen **fehlen**, statt `null` zu sein.

### `email-newsletter-get`

Grundfelder: `accountId*`, `newsletterId*`, `emailId*` (null bei einem Splittest — jeder Arm hat
seine eigene E-Mail), `createdAt*`, `newsletterStatus*` (`draft` · `scheduled` · `outgoing` ·
`sent`), `usageType*` (`newsletter` · `newsletter-split-test`), `emailEditor*` (`drag-and-drop` ·
`rich-text` · null beim Splittest), `isSplitTest*`, `splitTestVariants` (Arme mit `emailId`,
`label`, `name`, `subject`, `editorUrl`; null ohne Splittest), `editUrl*`, `contentUrl*` (null beim
Splittest), `scheduleUrl*`, `statisticsUrl*`.

Projektionen: `metadata` (Name, Notiz, Labels, Betreff, `utmCampaignName`), `audience`,
`deliveryConfiguration` (Absender, Antwortadresse, Signatur) — die zusätzlich `tracking` mitliefert
—, und die beiden mit fester Form:

Die `deliveryConfiguration` trägt vier Paare aus Modus und Wert: `senderNameMode`/`senderName`,
`senderEmailMode`/`senderEmail`, `replyToEmailMode`/`replyToEmail` und
`senderDomainMode`/`senderDomain`, dazu `signature`. Der Wert ist nur bei Modus `explicit` gesetzt,
sonst `null` — er wird erst beim Versand aufgelöst.

**`tracking`** kommt zusammen mit `deliveryConfiguration` (dieselbe Seite der App, ein Panel
tiefer): `linkTracking*` (true = Tracking an) und `headerLinks*` (true = Browseransicht, Abmelden
und Spam melden stehen über dem Inhalt).

**`deliveryStatus`** — `observedAt*` (wann gelesen; Bounces und Beschwerden kommen nach dem Versand
noch nach), `name*`, `newsletterStatus*`, `dispatchConfigured*`, `mode*` (`immediate` ·
`scheduled` · null solange kein Versand eingerichtet ist, nie ein leerer String), `sendDate*` (null
für einen Entwurf, auch wenn ein Termin gesetzt und abgesagt wurde), `sendProcessFinishedAt*`,
`estimatedRecipients*`, die elf Zähler `sentCount`, `failedCount`, `totalOpenCount`,
`uniqueOpenCount`, `totalClickCount`, `uniqueClickCount`, `hardBounceCount`, `softBounceCount`,
`spamBounceCount`, `spamComplaintCount`, `unsubscriptionCount` (alle ≥ 0; `total…` zählt
Ereignisse, `unique…` Personen; `spamComplaintCount` steckt auch in `unsubscriptionCount`, weil eine
Beschwerde abmeldet — **nicht addieren**), `canBeCancelled*` (sagt, ob `email-newsletter-cancel`
den Versand noch zurücknehmen kann), `missingRequirements*` (Liste in
Worten, leer wenn nichts fehlt), `readyToSend*`, `scheduleUrl*`, `statisticsUrl*`.

**`audienceReach`** — `minRecipients*` (sicher erreicht), `maxRecipients*` (höchstens),
`observedAt*` (eine Momentaufnahme: zwischen Messung und Versand melden sich Kontakte an und ab).

### Die zwei Ablehnungen

Eine Ablehnung kommt mit `isError: true` und einer von zwei Formen:

- **Inhaltsfehler:** `{ "error": { "code", "message", "remediation", "details" } }` — `code` ist
  der maschinenlesbare KlickTipp-Code, `remediation` sagt, wer handeln muss (`get_again`,
  `use_klicktipp_editor`, `change_document`, `change_html`, `retry_later`,
  `ask_user_before_retry`, …), `details` ist immer ein Objekt, notfalls leer. Gib den Code weiter.
- **Splittest-Ablehnung:** `{ "code": "split_test_not_supported", "isSplitTest": true, "appUrl",
  "newsletterId", "message" }` — die Operation kann keinen Arm adressieren; `appUrl` sagt, wo die
  Arme in KlickTipp bearbeitet werden. Nichts wurde verändert.
