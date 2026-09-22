# Dynamischer Inhalt: eine Zeile nur für einen Teil der Empfänger

Im Editor heißt es *Dynamischer Inhalt → Anzeigebedingung*, in den Werkzeugen **Entscheidung**
(`decision`). Eine Zeile, die daran gebunden ist, erscheint nur bei den Kontakten, die die Bedingung
erfüllt — bei allen anderen fällt sie beim Versand ersatzlos heraus.

**Das Wichtigste zuerst, weil es der Fehler ist, den niemand sieht:** Eine Bedingung, die auf
niemanden zutrifft, ist kein Fehler. Der Newsletter wird verschickt, nichts wird gemeldet, und die
Zeile fehlt bei *allen*. Genau so ist ein Test-Tag aus einer alten Sitzung auf der Hauptzeile eines
Entwurfs liegen geblieben und hätte die Kernbotschaft unsichtbar gemacht. Prüfe deshalb vor dem
Versand mit `email-decisions-get`, welche Zeilen gebunden sind — und ob die Bedingung überhaupt
jemanden trifft.

## Der Ablauf

1. **`email-condition-capabilities-get`** — ohne Argumente den Katalog der Bedingungsarten, mit
   `conditionTypes` zusätzlich für diese Arten: die erlaubten Vergleiche, die Entitäten *dieses
   Kontos* (Tags, Automationen, E-Mails …) und die Zeitfenster. Höchstens fünf Arten pro Aufruf; die
   Entitätsliste ist bei 200 gekappt, `entityCount` sagt, wie viele es wirklich sind.
2. **`email-decision-write`** — die benannte Bedingung anlegen. Du gibst nur die Wahl an; Operator,
   Sekunden und das SmartTag-Feld werden daraus abgeleitet. Antwort enthält die `decisionId`.
3. **`email-row-condition-write`** — die Zeile binden, adressiert über die `uuid` aus
   `contentOutline`. `decisionId: null` löst die Bindung wieder.
4. **`email-decisions-get`** — was die E-Mail trägt und welche Zeilen jede Bedingung steuert. Die
   Bindung steckt als Marker *in* der Zeile und taucht in keiner anderen Projektion auf; das hier
   ist der einzige Weg, sie zu sehen.

Eine Bedingung ohne gebundene Zeile steuert nichts und wird beim nächsten Speichern im Editor
verworfen. Eine Bedingung kann mehrere Zeilen steuern.

## Was eine Bedingung ausmacht

Du wählst vier Dinge, alles andere ergibt sich:

| Feld | was es ist | woher |
| --- | --- | --- |
| `conditionType` | **was** geprüft wird | Katalog unten, Klassenname |
| `condition` | **wie** verglichen wird | `has`, `has-not`, `has-any`, `has-not-any` |
| `entity` | **welche** Entität — nur bei `has` und `has-not` | Fähigkeiten dieses Kontos |
| `timeframe` | **wann** — Vorgabe `anytime` | feste Liste unten |
| `action` | welches Ereignis der Entität zählt | je Art, siehe Katalog |

`has` und `has-not` brauchen eine `entity`; `has-any` und `has-not-any` fragen „irgendeine Entität
dieser Art" und nehmen keine. Eine `entity`, die dem Konto nicht gehört, wird **abgelehnt** — nicht
gespeichert.

**Segmente und ihre Verknüpfung.** `segments` ist eine Liste; innerhalb eines Segments verknüpft
`conditionsOpAND` die Bedingungen, zwischen den Segmenten `segmentsOpAND` (beides Vorgabe `true`).
Ein Kontakt sieht die Zeile, wenn der Baum insgesamt zutrifft.

## Die Zeitfenster

Feste Liste, für jede Art dieselbe: `anytime` (immer), `24h`, `3d`, `30d`, `90d`, `1y`. Sie zählen
zurück vom Moment des Versands.

## Der Katalog der Bedingungsarten

Alle 22 Arten, mit ihren Aktionen. Die Vergleiche sind überall `has`, `has-not`, `has-any`,
`has-not-any` — mit **einer** Ausnahme, die unten markiert ist. `conditionType` ist der vollständige
Klassenname, also `App\Klicktipp\Tag` und nicht `Tag`.

| `conditionType` (ohne `App\Klicktipp\`) | im Editor | `action` |
| --- | --- | --- |
| `Tag` | Manuelles Tag | `received` |
| `TagCategorySmartLink` | SmartLink | `clicked` |
| `CampaignsProcessFlow` | Automation | `started`, `finished` |
| `EmailsAutomationEmail` | E-Mails (Automation) | `sent`, `opened`, `clicked`, `viewed` |
| `EmailsAutomationSMS` | SMS (Automation) | `sent`, `clicked` |
| `CampaignsNewsletter` | Newsletter/Autoresponder | `sent`, `opened`, `clicked`, `viewed`, `converted` |
| `Requests` | Eintragung per E-Mail | `subscribed` |
| `SMSListbuildings` | Eintragung per SMS | `subscribed` |
| `APIKey` | API-Key | `subscribed` |
| `BusinessCardReader` | Visitenkartenscanner | `subscribed` |
| `Event` | Visitenkartenscanner-Event | `subscribed` |
| `SubscriptionFormsCustom` | Anmeldeformular | `subscribed` |
| `LandingPage\LandingPage` | Landingpage | `subscribed` |
| `PaymentIPNs` | Produkt | `bought` |
| `PaymentRefund` | Rückerstattung | `refunded` |
| `PaymentChargeback` | Rückbuchung | `chargedback` |
| `PaymentSubsequent` | Folgezahlung | `bought subsequently` |
| `PaymentDeferred` | Aufgeschobene Zahlung | `bought deferred` |
| `PaymentRebill` | Abo | `canceled`, `resumed` |
| `PaymentRebillStatus` | Abo-Status | `completed`, `expired` — **nur `has` und `has-any`** |
| `PaymentAffiliation` | Digistore-Affiliate | `affiliated` |
| `ToolOutbound` | Outbound | `triggered` |

Die Aktion entscheidet, *welches* Ereignis zählt: bei einem Newsletter ist `sent` etwas anderes als
`clicked`, und beide sind erlaubte Bedingungen für dieselbe E-Mail. Lässt du `action` weg, wird die
erste der Liste genommen.

Verlasse dich nicht auf diese Tabelle allein, wenn es darauf ankommt: welche Arten ein Konto
tatsächlich anbieten kann und welche Entitäten es dafür hat, beantwortet
`email-condition-capabilities-get` — die Tabelle hier sagt, wonach du fragen kannst.

## Ein vollständiges Beispiel

„Diese Zeile nur an Kontakte, die das Tag *Kunde* tragen":

```json
// 1. email-condition-capabilities-get  { "conditionTypes": ["App\\Klicktipp\\Tag"] }
//    -> entities: [{ "entity": 499, "label": "Kunde", "actionFields": { "received": 499 } }, ...]

// 2. email-decision-write
{
  "editorUrl": "…",
  "contentRevision": "…",
  "name": "Nur Kunden",
  "segments": [
    {
      "conditionsOpAND": true,
      "conditions": [
        { "conditionType": "App\\Klicktipp\\Tag", "condition": "has", "entity": 499 }
      ]
    }
  ]
}
//    -> decisionId "1"

// 3. email-row-condition-write
{ "editorUrl": "…", "contentRevision": "…", "rowUuid": "a4fac5c0-…", "decisionId": "1" }
```

Beide Schreibaufrufe sind an die `contentRevision` gebunden und speichern den Entwurf; veröffentlicht
wird weiterhin mit `email-content-publish`.

## Wenn eine Zeile nicht erscheint

Der übliche Fall ist nicht kaputt, sondern leer: die Bedingung trifft niemanden.

1. `email-decisions-get` — welche Bedingung steuert diese Zeile, und wie sieht ihr Baum aus?
2. Die `entity` in der Bedingung gegen das Konto prüfen: trägt das Tag überhaupt jemand? Ein Tag aus
   einem Test trägt typischerweise **null** Kontakte.
3. Entweder mit `email-decision-write` und derselben `decisionId` auf eine sinnvolle Entität
   umschreiben — die Bindung bleibt bestehen —, oder mit `email-row-condition-write` und
   `decisionId: null` die Zeile wieder für alle sichtbar machen.

Ein HTML-Import löscht Entscheidungen; das meldet der Werkzeug-Hinweis als „KlickTipp decisions are
deleted". Kopieren (`email-content-copy`) und Dokument-Import erhalten sie.
