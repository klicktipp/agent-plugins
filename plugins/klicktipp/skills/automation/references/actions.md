# Aktionstypen: Werkzeug, Typ, Pflicht-Settings

Diese Tabelle ersetzt die Werkzeugbeschreibungen. Die kommen aus einer Vorlage und unterscheiden die
Typen kaum — `tagging` sagt fast denselben Satz wie `untagging`. Was einen Typ ausmacht, steht hier.

Jedes `add-automation-…-action` hängt an mit: `automationId`, `revision`, `afterActionId`,
`branch`, `settings`, optional `dryRun`. Jedes `update-automation-…-action` ändert nur die
Settings, die es bekommt; weggelassene bleiben, und übergebene Listen **ersetzen** die bisherige.

| Werkzeug (`add-automation-<art>-action` / `update-automation-<art>-action`) | Typ im Graphen | Pflicht in `settings` |
|---|---|---|
| `update-automation-start-action` *(kein add)* | `start` | — |
| `email` | `email` | `emailID` |
| `sms` | `sms` | `emailID` ← **ein SMS-Entwurf** |
| `notification-email` | `notify by email` | `emailID`, `notifyReceiverEmail` |
| `notification-sms` | `notify by sms` | `emailID`, `notifyReceiverEmail` ← eine Mobilnummer wie `+491701234567` |
| `wait` | `wait` | `delayType` |
| `decision` | `decision` | `segmentsOpAND`, `segments` |
| `goal` | `goal` | `segmentsOpAND`, `segments` — wirkt in der **ganzen** Automation, siehe SKILL.md |
| `tag` | `tagging` | `tagID` |
| `untag` | `untagging` | `tagID` |
| `set-field` | `setfield` | `customFieldID`, `customFieldOp` |
| `go-to` | `goto` | `targetActionId` |
| `exit` | `exit` | — |
| `restart` | `restart` | — |
| `start-automation` | `start automation` | `campaignID` |
| `stop-automation` | `stop automation` | `campaignID` |
| `split-test` | `splittest` | — |
| `outbound` | `outbound` | `outboundID` |
| `name-detection` | `detect name` | `customFieldID` |
| `gender-detection` | `detect gender` | `customFieldID` |
| `unsubscribe` | `unsubscribe-contact` | — |

Die Typen `facebook audience add`, `facebook audience remove`, `fullcontact` und
`website_enrichment` haben über diese Verbindung **kein** Werkzeug. Eine im Editor gebaute
Automation kann sie enthalten, und ein Lesen meldet sie; anlegen oder ändern lassen sie sich hier
nicht.

## `delayType` — die Werte einer Wartezeit

`immediately`, `seconds`, `minutes`, `hours`, `days`, `weeks`, `months`, `years`,
`from field`, `customfield minutes`, `customfield hours`, `customfield days`, `customfield weeks`,
`customfield months`, `customfield years`, `birthday`, `calendar`, `limiter`.

Die Menge gehört in `delayTime` (−999 bis 999). „Warten – 3 Tage" ist also
`{"delayType": "days", "delayTime": 3}`.

Die `customfield …`-Werte und `from field` zählen **nicht ab dem Einstieg des Kontakts, sondern ab
einem Datum in dessen Feld**; `delayField` nennt das Feld. Nur so trifft eine Kampagne für alle
einen festen Termin, egal wann sie eingestiegen sind — deshalb darf `delayTime` hier negativ sein:
`-24` mit `customfield hours` heißt 24 Stunden *vor* dem Termin. Wann das der richtige Weg ist und
was sonst passiert, steht in SKILL.md unter BP‑2.

Zwei Verhalten, die man erst sieht, wenn sie zuschlagen: ein so berechneter Zeitpunkt, der **schon
vorbei** ist, wartet nicht, er ist fällig — mehrere Erinnerungen laufen dann in einem Zug durch. Und
ein Feld **ohne gültiges Datum** wartet auch nicht, sondern geht sofort weiter, für jede betroffene
Wartezeit.

## Bedingungen (`decision`, `goal`)

`segments` ist die Liste der Bedingungen, `segmentsOpAND` sagt, ob sie mit UND oder ODER verbunden
sind. Eine Bedingung besteht aus Operator, `field` und `value`:

- Den **Operator** aus `get-automation-editor-capabilities` → `conditionOperators` nehmen. Nicht raten.
- Bei Tag- und Nachrichtenbedingungen ist `field` die **Smart-Tag-ID**, nicht die Objekt-ID. Für
  „E-Mail geöffnet" oder „Link geklickt" liefert `get-automation-email` die Smart-Tags der Nachricht.
- Wo ein Operator kein Feld braucht, ist `field` `0`.
- Bei Tag-Bedingungen ist `value` der Zeitraum; `0` heißt „irgendwann".
- Gespeicherte Segmente gehören mit ihrem Selektor in `value2`.
- Für die Datumsoperatoren `is before` / `is after` ist `value` **relativ zu jetzt** und wird wie
  `strtotime` gelesen: `+24 hours`, `+1 day`, `-2 weeks`. So fragst du „liegt das Datum in diesem
  Feld noch mehr als 24 Stunden vor uns" — die Bedingung, mit der eine Terminkampagne Späteinsteiger
  an vergangenen Erinnerungen vorbeiführt.

## Der Rest der Familie

**Graph:** `get-automation` (Graph, IDs, Revision), `search-automations`, `validate-automation`,
`create-automation-draft`, `update-automation-draft`, `delete-automation-action`,
`move-automation-action`, `copy-automation-action`.

**Nachrichten:** für Automations-E-Mails `get-automation-email`, `create-automation-email-draft`,
`update-automation-email-draft`, `delete-automation-email-draft`, `copy-automation-email`,
`send-automation-email-test`; dieselben ohne Kopie für Benachrichtigungs-E-Mails
(`…-notification-email…`, Test mit `send-notification-email-test`); für beide
`send-email-for-gmail-placement-preview` und `get-email-gmail-placement-preview-result`.
SMS: `get-automation-sms`, `create-automation-sms-draft`, `update-automation-sms-draft`,
`delete-automation-sms-draft`, `replace-automation-sms-content`, `copy-automation-sms`,
`send-automation-sms-test`; dieselben ohne Kopie für Benachrichtigungs-SMS.

**Betrieb:** `estimate-automation-audience`, `prepare-automation-activation`, `stop-automation`,
`move-automation-contacts`; die Zahlen (`get-automation-statistics`,
`get-automation-waiting-contact-counts`, `get-automation-email-statistics`,
`get-automation-sms-statistics`) beim Skill `dashboard`.

**Nachschlagen:** `get-automation-editor-capabilities`, `search-automation-editor-references`.
