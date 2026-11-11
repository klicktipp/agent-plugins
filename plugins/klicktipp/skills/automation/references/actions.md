# Action types: tool, type, required settings

This table replaces the tool descriptions. Those are generated from a template and barely
distinguish the types — `tagging` says almost the same sentence as `untagging`. What makes a type is
here.

Every `add-automation-…-action` attaches with: `automationId`, `revision`, `afterActionId`,
`branch`, `settings`, optionally `dryRun`. Every `update-automation-…-action` changes only the
settings it is given; omitted ones stay, and lists that are passed **replace** the previous list.

| Tool (`add-automation-<kind>-action` / `update-automation-<kind>-action`) | Type in the graph | Required in `settings` |
|---|---|---|
| `update-automation-start-action` *(no add)* | `start` | — |
| `email` | `email` | `emailID` |
| `sms` | `sms` | `emailID` ← **an SMS draft** |
| `notification-email` | `notify by email` | `emailID`, `notifyReceiverEmail` |
| `notification-sms` | `notify by sms` | `emailID`, `notifyReceiverEmail` |
| `wait` | `wait` | `delayType` |
| `decision` | `decision` | `segmentsOpAND`, `segments` |
| `goal` | `goal` | `segmentsOpAND`, `segments` — acts across the **whole** automation, see SKILL.md |
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
| `facebook-audience` | `facebook audience add` | `audienceID` |
| `facebook-audience-removal` | `facebook audience remove` | `audienceID` |
| `name-detection` | `detect name` | `customFieldID` |
| `gender-detection` | `detect gender` | `customFieldID` |
| `fullcontact` | `fullcontact` | — |
| `unsubscribe` | `unsubscribe-contact` | — |

Website enrichment (`website_enrichment`) has **no** tool. An automation built in the editor can
carry it and a read reports it; it cannot be created or changed, and
`get-automation-editor-capabilities` therefore does not offer it in the first place.

## `delayType` — the values of a wait

`immediately`, `seconds`, `minutes`, `hours`, `days`, `weeks`, `months`, `years`,
`from field`, `customfield minutes`, `customfield hours`, `customfield days`, `customfield weeks`,
`customfield months`, `customfield years`, `birthday`, `calendar`, `limiter`.

The amount goes into `delayTime` (−999 to 999). "Wait – 3 days" is therefore
`{"delayType": "days", "delayTime": 3}`.

The `customfield …` values and `from field` count **not from the contact's entry but from a date in
that contact's field**; `delayField` names the field. Only that way does a campaign hit a fixed date
for everyone, whenever they entered — which is why `delayTime` may be negative here: `-24` with
`customfield hours` means 24 hours *before* the date. When this is the right way, and what else
happens, is in SKILL.md under "Dated campaigns".

Two behaviours you do not see until they bite: a moment computed this way that has **already
passed** does not wait, it is due — several reminders then run through in one go. And a field
**without a valid date** does not wait either but continues immediately, for every wait affected.

## Conditions (`decision`, `goal`)

`segments` is the list of conditions, `segmentsOpAND` says whether they are joined with AND or OR. A
condition consists of an operator, `field` and `value`:

- Take the **operator** from `get-automation-editor-capabilities` → `conditionOperators`. Do not guess.
- For tag and message conditions, `field` is the **smart tag ID**, not the object ID. For "email
  opened" or "link clicked", `get-automation-email` delivers the message's smart tags.
- Where an operator needs no field, `field` is `0`.
- For tag conditions, `value` is the time range; `0` means "at some point".
- Saved segments go into `value2` with their selector.
- For the date operators `is before` / `is after`, `value` is **relative to now** and read like
  `strtotime`: `+24 hours`, `+1 day`, `-2 weeks`. That is how you ask "is the date in this field
  still more than 24 hours ahead of us" — the condition with which a dated campaign routes late
  entrants past reminders that have passed.

## The rest of the family

**Graph:** `get-automation` (graph, IDs, revision), `search-automations`, `validate-automation`,
`create-automation-draft`, `update-automation-draft`, `delete-automation-draft`,
`delete-automation-action`, `move-automation-action`, `copy-automation-action`.

**Messages:** `get-automation-email`, `create-automation-email-draft`,
`update-automation-email-draft`, `delete-automation-email-draft`, the same four for
`automation-sms`, `notification-email` and `notification-sms`,
one tool per kind for copying, SMS text and test sends — `copy-automation-email` /
`copy-notification-email`, `copy-automation-sms` / `copy-notification-sms`,
`replace-automation-sms-content` / `replace-notification-sms-content`,
`send-automation-email-test` / `send-notification-email-test`, `send-automation-sms-test` /
`send-notification-sms-test` — plus `check-sms-readiness`, `preview-personalized-email`,
`send-email-for-gmail-placement-preview`.

**Operation:** `estimate-automation-audience`, `prepare-automation-activation`, `stop-automation`,
`get-automation-waiting-contact-counts`, `get-automation-statistics`, `get-automation-email-statistics`,
`move-automation-contacts`.

**Lookup:** `get-automation-editor-capabilities`, `search-automation-editor-references`.
