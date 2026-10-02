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
| `search-newsletters` | R | Liste der Newsletter, filterbar nach Name, Status, zwei Zeitfenstern; Cursor-Seiten. Der Weg von einer Editor-URL zum Newsletter. |
| `get-newsletter` | R | Ein Newsletter mit Projektionen: `metadata`, `audience`, `deliveryConfiguration`, `deliveryStatus`, `audienceReach`, `conversionPixel`. Kein Inhalt — der ist `get-email-editor-content` (Skill `email`). |
| `create-newsletter-draft` | | Entwurf anlegen: Name, Betreff, Pre-Header, optional `splitTest` (Skill `splittest`). Sendet nichts. |
| `update-newsletter-draft` | I | Name, Notiz, Betreff, Pre-Header, Zielgruppe eines Entwurfs. Betreff/Pre-Header machen `contentRevision` ungültig. |
| `delete-newsletter-draft` | D | Entwurf endgültig löschen. |
| `configure-newsletter-delivery` | I | Absender, Antwortadresse, Versanddomain, Signatur, Link-Tracking, KlickTipp-Kopfzeile. Prüft gegen die Listen, die es selbst mitliefert. |
| `send-newsletter-test` | DO | Eine echte Testmail an eine beliebige Adresse; der Empfänger wird Kontakt des Kontos und als Testempfänger getaggt. Trägt den **veröffentlichten** Inhalt — vorher `publish-newsletter-email-content`. Beim Splittest mit `messageId` je Variante. |
| `prepare-newsletter-dispatch` | DO | **Sendet nicht** — bereitet vor und gibt die Bestätigungs-URL, die ein Mensch in KlickTipp klickt. Der Klick erreicht echte Empfänger. |
| `cancel-newsletter-dispatch` | D | Einen terminierten oder eben angelaufenen Versand zurücknehmen — der Newsletter wird wieder Entwurf. Nur solange `canBeCancelled`; holt nichts zurück, was schon raus ist. |
| `search-signatures` | R | Die Signaturen, mit denen sich gerade senden lässt; `includeUnusable` zeigt die übrigen mit Gründen. Kein Text. |
| `get-signature` | R | Eine Signatur: Absenderprofil, Tags, Visitenkarte, Nutzbarkeit; `includeContent` holt HTML, Plain und transaktionalen Text. |
| `create-signature` | O | Neu mit `content` oder als Kopie mit `sourceSignatureId`; braucht mindestens ein freies Tag und die Pflichtplatzhalter. |
| `update-signature` | I | Name, Notiz, Labels, Visitenkarte. Nie Text, Tags oder Absender. |
| `replace-signature-content` | DOI | Den Text ersetzen — HTML und Plain ganz, ohne Undo. |
| `configure-signature-delivery` | OI | Tags und Absenderprofil einer Signatur; die Versanddomain wird aus der Absenderadresse abgeleitet. |
| `list-sender-domains` | R | Die Absenderdomains des Kontos mit Prüfstand; liest gespeicherten Stand, fragt kein DNS. |
| `get-sender-domain` | R | Eine Domain: Verifizierung, Nutzbarkeit, letzte Prüfanfrage, die Absenderadressen darunter. |
| `get-sender-domain-dns-setup` | R | Die DNS-Einträge, die die Domain braucht, und der zuletzt gemessene Ist-Stand je Eintrag. |
| `create-sender-domain` | | Eine Domain registrieren — unverifiziert, nicht Standard, sendet nichts. |
| `request-sender-domain-dns-check` | O | Eine frische DNS-Prüfung anstoßen, asynchron und mit Wartezeit je Domain. |

## Inhalt

- Newsletter
- Signaturen
- Absenderdomains
- Antwortformen

## Newsletter

### `cancel-newsletter-dispatch`
**Wofür:** einen Versand zurücknehmen, der terminiert ist oder gerade anläuft; der Newsletter wird
wieder Entwurf und erreicht niemanden weiter. **Nicht:** löschen, und **nicht** zurückholen, was
schon versendet wurde. **Stolperer:** Nur solange `deliveryStatus.canBeCancelled` `true` ist —
danach wird abgelehnt, und die Meldung sagt, dass es zu spät ist statt so zu tun als ginge es.
Ein Entwurf wird mit einem eigenen Satz abgelehnt („kein Versand zum Abbrechen"), damit du die
beiden Fälle nicht verwechselst. Braucht dieselbe Berechtigung wie das Freigeben
(„Email marketing manager"). **Frag die Person vorher** — einen bewusst eingerichteten Versand
brichst du nicht auf eigene Einschätzung ab. Wieder aktivieren geht mit `prepare-newsletter-dispatch`.
Die Antwort sagt ausdrücklich, dass bereits versendete Mails unterwegs bleiben; gib diesen Satz
weiter, statt nur „abgebrochen" zu melden.

### `search-newsletters`
**Wofür:** die Liste; Filter `query`, `status`, `createdFrom/Before`, `sendDateFrom/Before`; Seiten
über `cursor`. **Nicht:** Betreff, Inhalt, Zielgruppe, Statistik — das ist `get-newsletter`.
**Stolperer:** Ein Entwurf hat kein Versanddatum und fällt in kein `sendDate`-Fenster, auch wenn ein
Termin gesetzt und abgesagt wurde. Zeitfenster sind halboffen (`From` inklusiv, `Before` exklusiv)
und wollen einen UTC-Offset (`2026-09-01T10:00:00+02:00`). Der `cursor` kommt unverändert zurück,
mit denselben Filtern; nur die Seitengröße darf sich ändern. Eine Editor-URL nennt die *E-Mail*:
`emailId` abgleichen, nicht raten. Ein Splittest hat `emailId: null`.

### `get-newsletter`
**Wofür:** ein Newsletter mit den Projektionen, die du brauchst: `metadata` (Name, Notiz, Labels,
Betreff), `audience`, `deliveryConfiguration` (Absender, Antwortadresse, Signatur), `deliveryStatus`
(Stand des Versands), `audienceReach` (wie viele Kontakte er jetzt erreichen würde). Ohne `include`
nur Identität und Lebenszyklus. **Nicht:** der Körper — `get-email-editor-content` mit `editorUrl` oder `emailId`.
**Stolperer:** Projektionen sind alles oder nichts; eine, die nicht bedient werden kann, lässt den
ganzen Aufruf scheitern. Bei einem Splittest sind `emailId`, `contentUrl` und `metadata.subject`
null, die Varianten stehen in `splitTestVariants`, und `deliveryConfiguration` braucht eine `editorUrl`
daraus. `audienceReach` ist eine Messung, kein gespeicherter Wert — und die einzige Zahl, die „wie
viele Kontakte" beantwortet. `deliveryStatus` trägt `observedAt`: Bounces und Beschwerden kommen
nach dem Versand noch nach.

### `create-newsletter-draft`
**Wofür:** die Hülle — Name (eindeutig im Konto), Betreff, Pre-Header (≤ 120 Zeichen, kein HTML).
**Nicht:** Inhalt, Zielgruppe, Absender, Termin. **Stolperer:** Ohne Zielgruppe heißt Zielgruppe
*alle aktiven Kontakte* (`all_contacts`). Der Betreff kommt vom Menschen, nie erfunden — er ist die
Zeile, die jeder Empfänger sieht. Der Pre-Header ist kein Teil des Dokuments: ein HTML-Import kann
ihn nicht setzen, eine versteckte Vorschauzeile im HTML fällt beim Konvertieren weg. `splitTest`
ist unumkehrbar — in beide Richtungen — und braucht Premium; `conversions`/`revenue` zusätzlich den
Conversion-Pixel.

### `update-newsletter-draft`
**Wofür:** Name (≤ 250), Notiz (≤ 1000, nie an Empfänger), Betreff, Pre-Header, Zielgruppe,
UTM-Kampagnenname (≤ 120).
**Nicht:** Inhalt, Absender, Termin — und keinen Splittest (dessen Betreff:
`update-newsletter-split-test-variant`). **Stolperer:** Betreff oder Pre-Header schreiben macht jede
vorher gelesene `contentRevision` ungültig — der nächste Inhalts-Write wird als „geändert"
abgewiesen. Die Zielgruppe ersetzt die alte komplett: `mode` ist `all_contacts`, `saved_audience`
(mit `audienceId`) oder `tag_conditions` (mit `includeTagIds`/`excludeTagIds`, je `…Match` `any`
oder `all`; zusammen höchstens 50 Tags). Ein leerer `preheader` entfernt ihn, ein weggelassener
lässt ihn stehen — das gilt für jedes Feld: weggelassen heißt behalten.

`utmCampaignName` ist der Name, den KlickTipp als `utm_campaign` an die getrackten Links hängt. Er
gehört zur Kampagne, deshalb steht er hier und nicht beim Versand-Werkzeug. Leerer String heißt
„zurück zu den kontoweiten UTM-Einstellungen"; weggelassen heißt behalten. Über 120 Zeichen wird
abgelehnt, bevor irgendetwas geschrieben wird.

### `delete-newsletter-draft`
**Wofür:** einen Entwurf endgültig entfernen. **Nicht:** geplante, laufende, versendete Newsletter.
**Stolperer:** Kein Papierkorb. Eine Namensähnlichkeit aus der Suche ist keine Zustimmung.

### `configure-newsletter-delivery`
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
gerendert und mit `update-newsletter-draft` als `preheader` geschrieben.

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
`get-newsletter` mit `include: ["deliveryConfiguration"]` (`senderDomainMode`,
`senderDomain`). Lies sie, statt Adressen oder Domains zu raten.

### `send-newsletter-test`
**Wofür:** eine echte Mail an eine beliebige Adresse, über dieselbe Aktion wie der Testdialog der
Oberfläche. **Nicht:** ein Versand an die Zielgruppe, und kein Blick auf den Entwurf. **Stolperer:**
Der Empfänger wird als Kontakt mit dem Testempfänger-Tag angelegt oder markiert — eine
Schreiboperation am Konto, die Automationen starten kann, also vorher sagen. Die Mail trägt den
veröffentlichten Inhalt: ein nie veröffentlichter Body wird mit
`newsletter_send_content_publish_required` abgewiesen (erst `publish-newsletter-email-content`), alles andere,
was die Oberfläche vor einem Test verlangt — Betreff, Pflicht-Tags im Inhalt — mit
`newsletter_send_not_ready`; beide nennen die Gründe in `details.missingRequirements` und die
Editor-URL. Wurde nach dem Veröffentlichen geändert, wird gesendet, und die Antwort trägt
`warnings`: der Test zeigt den älteren Stand. Bei einem Splittest ist `messageId` Pflicht — die
`emailId` der Variante aus `get-newsletter-split-test`; gesendet wird genau diese Variante mit
ihrem Betreff, Zeitplan und Gewinnerauswahl bleiben unberührt. Ohne `messageId`, mit einer
Variante eines anderen Tests oder mit `messageId` bei einem normalen Newsletter wird abgewiesen,
bevor ein Testkontakt entsteht.

### `prepare-newsletter-dispatch`
**Wofür:** die Vorbereitung — Prüfung, Empfängerschätzung, Bestätigungs-URL. **Nicht:** senden. Nie.
**Stolperer:** Sag danach nicht „verschickt". Geänderter, nicht veröffentlichter Inhalt wird
abgewiesen — erst `publish-newsletter-email-content`. `mode` ist Pflicht (`immediate` / `scheduled`, kein
Default); `scheduledAt` ist bei `scheduled` Pflicht, bei `immediate` verboten, und trägt seinen
UTC-Offset. Ändert sich ein gebundener Wert oder läuft die URL ab, neu vorbereiten.

## Signaturen

Eine Signatur ist mehr als ein Text unter der Mail: sie trägt ein **Absenderprofil** (Absender,
Antwortadresse, CC, BCC, Empfänger, Versanddomain), **Tags**, über die KlickTipp sie selbst
auswählt, und eine **digitale Visitenkarte**. Angehängt wird sie erst beim Versand — eine Änderung
gilt also für jeden künftigen Versand, der sie trägt, nicht nur für den Newsletter, um den es gerade
geht. Welche Signatur ein Newsletter benutzt, setzt weiterhin `configure-newsletter-delivery` mit
`signatureId`; `0` heißt „KlickTipp wählt per Tagging" und ist kein Eintrag der Suche.

### `search-signatures`
**Wofür:** die Signaturen, die ein Newsletter tragen kann, mit ID, Name, gespeicherter und
wirksamer Absenderadresse, Bereitschaft dieser Absenderidentität und den Tags. **Nicht:** der Text —
das ist `get-signature`. **Stolperer:** Eine Signatur, die so, wie sie ist, nicht senden kann —
kein Inhalt, fehlende Pflichtplatzhalter, eine Absenderadresse ohne Freigabe —, **fehlt** in der
Liste. „Ich finde meine Signatur nicht" heißt deshalb meistens `includeUnusable: true`; dann kommt
sie mit den Gründen, und die gibst du weiter, statt sie zu verschweigen.

### `get-signature`
**Wofür:** eine Signatur ganz: Name, Notiz, Labels, Tag-IDs, Absenderprofil, Visitenkarte,
Inhaltsflags, Nutzbarkeit und was sie blockiert. **Stolperer:** Ohne `includeContent: true` kein
Text, nur die Flags — der Text ist der größte Teil der Antwort, hol ihn nur, wenn du ihn brauchst.
Eine leere gespeicherte `senderEmail` heißt „die Adresse des Kontos", nicht „kein Absender".

### `create-signature`
**Wofür:** eine neue Signatur, entweder mit vollständigem `content` oder als Kopie einer bestehenden
über `sourceSignatureId`; bei einer Kopie überschreibt, was du mitgibst, und der Rest bleibt vom
Original. **Nicht:** einen Newsletter ändern — keiner benutzt die neue Signatur, bis sie gewählt wird.
**Stolperer:** Mindestens ein Tag ist Pflicht, und jedes Tag darf noch keiner anderen Signatur
gehören. Das HTML braucht `%Link:Unsubscribe%` als `href` eines Links und die Adressplatzhalter
`%User:FirstName%`, `%User:LastName%`, `%User:Street%`, `%User:Zip%`, `%User:City%`,
`%User:Country%`; der Plain-Text dieselben, der Abmeldelink darf dort als Text stehen; das
transaktionale HTML die Adressplatzhalter, aber **kein** `%Link:Unsubscribe%` (`%Link:SubscriberInfo%`
ist empfohlen). Ein Konto, das Adressangaben weglassen darf, ist von den Adressplatzhaltern befreit,
nie vom Abmeldelink. Fehlt einer, wird abgelehnt — setz die Platzhalter, statt Adressdaten
auszuschreiben oder zu erfinden. Der Plain-Text wird nur gespeichert, wenn das Konto ihn frei
bearbeiten darf, sonst aus dem HTML erzeugt — erwarte ihn also nicht unverändert zurück. **Die
transaktionale Fassung ist kein Randfall:** sie geht an Erstkontakte, etwa mit einer
Bestätigungsmail, wo ein Abmeldelink von einer Anmeldung abmelden würde, die nie bestätigt wurde.
Biete sie beim Anlegen an, statt zu warten, bis jemand danach fragt. Die Absenderadresse braucht eine verifizierte Domain.
Die Antwort trägt nur Flags; den gespeicherten Text liest `get-signature`.

### `update-signature`
**Wofür:** Name, interne Notiz, Labels und Visitenkarte. **Nicht:** Text, Tags oder
Absenderprofil — dafür gibt es die beiden Werkzeuge darunter. **Stolperer:** Die
Standardsignatur lässt sich nicht umbenennen. Ein leerer String in der Visitenkarte leert das Feld;
ein weggelassenes Feld bleibt.

### `replace-signature-content`
**Wofür:** den Text einer Signatur ersetzen. **Nicht:** Name, Tags, Absender, Visitenkarte.
**Stolperer:** HTML und Plain werden **ganz** ersetzt, ohne Undo — lies den Text vorher mit
`get-signature` und `includeContent: true`, zeig der Person, was sich ändert, und frag. Weil die
Signatur erst beim Versand angehängt wird, ändert das jede künftige Mail, die sie trägt. Es gelten
dieselben Pflichtplatzhalter wie beim Anlegen. Der transaktionale Teil ändert sich nur, wenn du ihn
mitgibst; `useInTransactionalEmails: false` plus leeres `transactionalHtml` schaltet ihn ab und leert
ihn.

### `configure-signature-delivery`
**Wofür:** die Tags einer Signatur und ihr Absenderprofil — Absendername, Absenderadresse,
Antwortadresse, CC, BCC, Empfänger, Versanddomain. **Nicht:** Text, Name, Visitenkarte, und es legt
nichts an: jedes Tag, jede Adresse und jede Domain muss es im Konto schon geben. **Stolperer:**
Ändert sich die Absenderadresse, wird sie gegen ihre verifizierte Domain geprüft und die passende
Versanddomain abgeleitet und gespeichert, wie die App es tut. Eine gewöhnliche Signatur braucht
mindestens ein Tag, die Standardsignatur darf ohne auskommen; ein Tag, das schon einer anderen
Signatur gehört, wird abgelehnt.

## Absenderdomains

Eine Absenderadresse braucht eine **verifizierte** Domain, und verifiziert ist eine Domain erst,
wenn ihre DNS-Einträge stimmen. Die Einträge setzt die Person bei ihrem DNS-Anbieter — kein Werkzeug
hier schreibt DNS. Eine neue Domain erscheint in `availableSenderDomains` von
`configure-newsletter-delivery` erst, wenn sie senden darf.

### `list-sender-domains` · `get-sender-domain`
**Wofür:** die Domains des Kontos mit Prüfstand, Standard-Markierung und ob die Wartezeit für die
DNS-Verbreitung vorbei ist; einzeln mit Nutzbarkeit, letzter Prüfanfrage und den Absenderadressen
darunter, Subdomains eingeschlossen. **Nicht:** eine DNS-Abfrage — beide lesen den gespeicherten
Stand. **Stolperer:** Eine Adresse in der Liste von `get-sender-domain` ist nicht zwingend bestätigt
oder sendebereit. Die gemeinsame Rückfall-Infrastruktur von KlickTipp ist keine Domain des Kontos
und steht deshalb nicht darin.

### `get-sender-domain-dns-setup`
**Wofür:** jeden DNS-Eintrag, den die Domain braucht — Typ, Host, Wert, Priorität, TTL —, und den
zuletzt gemessenen Ist-Stand daneben. **Stolperer:** Mehrere erwartete Typen oder Werte sind
**Alternativen**: veröffentlicht wird genau ein Paar, normalerweise das erste. Gib die Einträge so
weiter, dass die Person sie abschreiben kann, statt sie zusammenzufassen. Es misst nicht live; ein
`checkedAt: null` heißt „noch kein Ergebnis", nicht „falsch".

### `create-sender-domain`
**Wofür:** eine Domain oder Subdomain registrieren, ohne Protokoll, Pfad, Platzhalter oder Punkt am
Ende. **Nicht:** verifizieren, zur Standarddomain machen, etwas senden. **Stolperer:** Es gelten
dieselben Regeln wie im Formular des Kontos — Syntax, reservierte Domains, **weltweite
Eindeutigkeit** und das Limit des Produkts. Frag, bevor du eine Domain anlegst, die niemand genannt
hat: sie ist danach im Konto, und nutzbar wird sie erst mit den DNS-Einträgen.

### `request-sender-domain-dns-check`
**Wofür:** eine frische DNS-Prüfung anstoßen, nachdem die Person die Einträge gesetzt hat.
**Nicht:** senden, und nicht die Wartezeit je Domain umgehen. **Stolperer:** Die Prüfung läuft
asynchron. In der Wartezeit kommt kein Fehler, sondern `cooldownActive: true` mit der gespeicherten
Anfrage und dem nächsten möglichen Zeitpunkt — sag der Person, wann es wieder geht, statt erneut
anzustoßen. Das Ergebnis liest `get-sender-domain-dns-setup`: fertig ist es, wenn jedes `checkedAt`
mindestens so spät ist wie `lastDnsCheckRequestedAt` aus dieser Antwort. Frag nicht in enger Schleife
nach — die DNS-Verbreitung braucht ihre Zeit, und die Wartezeit je Domain gilt trotzdem.

## Antwortformen

**Jedes Werkzeug veröffentlicht ein Output-Schema** (JSON Schema), das ein Client gegen
`structuredContent` prüfen kann.

Ein Schema **benennt Felder, es erklärt sie nicht**. Diese Seite bleibt deshalb die ausführlichere
Quelle: was ein Feld bedeutet, wann es fehlt und was eine Absage auslöst, steht hier und nicht im
Schema.
Jede Antwort kommt als `structuredContent` und als dieselbe kompakte JSON im Text. Ein `*`
markiert Felder, die immer da sind; alles andere ist nur da, wenn es angefordert wurde oder
zutrifft. Nicht angeforderte Projektionen **fehlen**, statt `null` zu sein.

### `get-newsletter`

Grundfelder: `accountId*`, `newsletterId*`, `emailId*` (null bei einem Splittest — jede Variante hat
seine eigene E-Mail), `createdAt*`, `newsletterStatus*` (`draft` · `scheduled` · `outgoing` ·
`sent`), `usageType*` (`newsletter` · `newsletter-split-test`), `emailEditor*` (`drag-and-drop` ·
`rich-text` · null beim Splittest), `isSplitTest*`, `splitTestVariants` (Varianten mit `emailId`,
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
Beschwerde abmeldet — **nicht addieren**), `canBeCancelled*` (sagt, ob `cancel-newsletter-dispatch`
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
  "newsletterId", "message" }` — die Operation kann keine Variante adressieren; `appUrl` sagt, wo die
  Varianten in KlickTipp bearbeitet werden. Nichts wurde verändert.
