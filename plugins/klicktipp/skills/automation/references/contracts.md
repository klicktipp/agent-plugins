# Die veröffentlichten Verträge — Automationen

Wort für Wort das, was der Server in `tools/list` für die 83 Werkzeuge dieses Skills
ausliefert: Beschreibung, Annotationen, jeder Parameter mit Typ, Grenzen und Beschreibung. Ein `*`
markiert Pflichtparameter. `R` liest nur · `D` löscht oder ersetzt ohne Undo · `O` erreicht etwas
außerhalb des Kontos · `I` ein zweiter gleicher Aufruf ändert nichts mehr.

Diese Datei spiegelt den Server, sie interpretiert ihn nicht: ändert sich eine
Werkzeugbeschreibung, wird sie hier wörtlich nachgezogen. Welcher Aktionstyp was tut und was in
`settings` gehört, steht in [actions.md](actions.md); die Statistik der Automationen beim Skill
`dashboard`. Ein Objekt-Parameter wie `settings` ist hier nur als `object` genannt — sein Schema
liefert `get-automation-editor-capabilities`.

## Inhalt

`get-automation` · `validate-automation` · `create-automation-draft` · `update-automation-draft` · `move-automation-action` · `copy-automation-action` · `delete-automation-action` · `get-automation-editor-capabilities` · `search-automation-editor-references` · `update-automation-start-action` · `add-automation-email-action` · `update-automation-email-action` · `add-automation-sms-action` · `update-automation-sms-action` · `add-automation-notification-email-action` · `update-automation-notification-email-action` · `add-automation-notification-sms-action` · `update-automation-notification-sms-action` · `add-automation-wait-action` · `update-automation-wait-action` · `add-automation-decision-action` · `update-automation-decision-action` · `add-automation-goal-action` · `update-automation-goal-action` · `add-automation-tag-action` · `update-automation-tag-action` · `add-automation-untag-action` · `update-automation-untag-action` · `add-automation-set-field-action` · `update-automation-set-field-action` · `add-automation-go-to-action` · `update-automation-go-to-action` · `add-automation-exit-action` · `update-automation-exit-action` · `add-automation-restart-action` · `update-automation-restart-action` · `add-automation-start-automation-action` · `update-automation-start-automation-action` · `add-automation-stop-automation-action` · `update-automation-stop-automation-action` · `add-automation-split-test-action` · `update-automation-split-test-action` · `add-automation-outbound-action` · `update-automation-outbound-action` · `add-automation-name-detection-action` · `update-automation-name-detection-action` · `add-automation-gender-detection-action` · `update-automation-gender-detection-action` · `add-automation-unsubscribe-action` · `update-automation-unsubscribe-action` · `estimate-automation-audience` · `prepare-automation-activation` · `stop-automation` · `move-automation-contacts` · `search-automation-templates` · `get-automation-template` · `import-automation-template` · `get-automation-email` · `create-automation-email-draft` · `update-automation-email-draft` · `delete-automation-email-draft` · `copy-automation-email` · `send-automation-email-test` · `get-notification-email` · `create-notification-email-draft` · `update-notification-email-draft` · `delete-notification-email-draft` · `send-notification-email-test` · `send-email-for-gmail-placement-preview` · `get-email-gmail-placement-preview-result` · `get-automation-sms` · `create-automation-sms-draft` · `update-automation-sms-draft` · `delete-automation-sms-draft` · `replace-automation-sms-content` · `copy-automation-sms` · `send-automation-sms-test` · `get-notification-sms` · `create-notification-sms-draft` · `update-notification-sms-draft` · `delete-notification-sms-draft` · `replace-notification-sms-content` · `send-notification-sms-test`

## `get-automation` · RI

**Read automation**

Reads an automation graph with stable action IDs, revision, status, validation findings and editor URL. Sends and activates nothing.

Parameter:

- `automationId`* — integer (minimum 1)
- `accountId` — null | integer (minimum 1)

## `validate-automation` · RI

**Validate automation**

Validates a saved automation and returns action-specific findings and the checked revision. Sends and activates nothing.

Parameter:

- `automationId`* — integer (minimum 1)
- `accountId` — null | integer (minimum 1)

## `create-automation-draft`

**Create automation draft**

Creates an inactive automation draft with a start action. copyFromId also copies a graph and its split-test settings but reuses referenced emails. Entry conditions are configured with update-automation-start-action, further actions with the automation action tools. Does not schedule or send.

Parameter:

- `name`* — string (minLength 1; maxLength 250)
- `copyFromId` — null | integer (minimum 1)
- `accountId` — null | integer (minimum 1)

## `update-automation-draft`

**Update automation draft settings**

Updates supplied settings of an inactive automation at its current revision. Omitted values stay; empty strings or an empty metaLabels list clear values. multipleSend can only disable the legacy repeat flag; repeated entry uses start conditions or restart actions.

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `settings`* — object
- `accountId` — null | integer (minimum 1)

## `move-automation-action`

**Move automation action**

Moves an automation action by stable ID in an inactive graph. subtree moves its following graph to an open branch; a populated decision requires subtree. Moving one regular action reconnects its old neighbours; goto references retain their IDs. Requires the current revision; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `subtree` — boolean
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `copy-automation-action`

**Copy automation action**

Copies an automation action or subtree into an inactive graph, assigning new IDs but sharing referenced emails. A single copied decision has empty branches except its insertion-point successor. Split tests are copied independently; subtrees require an open destination. Requires the current revision; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `subtree` — boolean
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `delete-automation-action` · D

**Delete automation action**

Deletes an action from an inactive automation, discarding the selected branch or preserving a chosen successor. Decision choices are keep_yes, keep_no or subtree; other actions use keep_next or subtree. The start action cannot be deleted; incoming goto references must be changed first. Emails stay. dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `mode`* — string (einer von `keep_next`, `keep_yes`, `keep_no`, `subtree`)
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `get-automation-editor-capabilities` · RI

**Read automation capabilities**

Reads automation editor capabilities: email and SMS actions with closed settings schemas and required add fields, engine condition and field operators, account-authorized plugin conditions. actionType optionally limits it to a graph type from get-automation. Integration availability also depends on the selected reference; resolve IDs with search-automation-editor-references first.

Parameter:

- `actionType` — string | null (einer von `start`, `email`, `sms`, `notify by sms`, `notify by email`, `wait`, `decision`, `goal`, `tagging`, `untagging`, `setfield`, `goto`, `exit`, `restart`, `start automation`, `stop automation`, `splittest`, `outbound`, `facebook audience add`, `facebook audience remove`, `detect name`, `detect gender`, `fullcontact`, `website_enrichment`, `unsubscribe`, `null`)
- `accountId` — null | integer (minimum 1)

## `search-automation-editor-references` · RI

**Find automation references**

Searches existing emails, SMS, tags, fields, signatures, calendars, outbounds, Facebook audiences, automations or saved segment selectors by name to resolve automation editor IDs, without connection secrets. Email IDs are message references; event conditions use their smart tags from get-automation-email or get-notification-email. Create missing tags or fields with the tag/field tools.

Parameter:

- `kind`* — string (einer von `automation-email`, `notification-email`, `automation-sms`, `notification-sms`, `tag`, `field`, `signature`, `calendar`, `outbound`, `facebook-audience`, `automation`, `segment`)
- `query` — string (maxLength 250)
- `offset` — integer (minimum 0)
- `limit` — integer (minimum 1; maximum 100)
- `accountId` — null | integer (minimum 1)

## `update-automation-start-action`

**Update start action**

Updates an automation's existing start action to control who enters and when. An empty condition means only another automation can start it. Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `add-automation-email-action`

**Add email action**

Adds an automation email action that sends a referenced email (emailID, created with create-automation-email-draft) when the contact reaches it. Editing the shared email affects every action that references it. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `update-automation-email-action`

**Update email action**

Updates an automation email action's settings or referenced email, not its content (update-automation-email-draft). Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `add-automation-sms-action`

**Add SMS action**

Adds an automation SMS action that sends a referenced SMS to the contact when reached. emailID takes an automation SMS draft ID (create-automation-sms-draft), not an email ID. Requires SMS marketing, an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `update-automation-sms-action`

**Update SMS action**

Updates an automation SMS action's settings or referenced SMS draft (emailID), not the message text (update-automation-sms-draft). Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `add-automation-notification-email-action`

**Add notification-email action**

Adds an automation email notification action for an internal address, not the contact. emailID references a notification email draft (create-notification-email-draft); notifyReceiverEmail takes an address or dispatchProfile. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `update-automation-notification-email-action`

**Update notification-email action**

Updates an automation email notification's receiver or message reference, not its body (update-notification-email-draft). Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `add-automation-notification-sms-action`

**Add notification-sms action**

Adds an automation SMS notification action for an internal number, not the contact. emailID references a notification SMS draft (create-notification-sms-draft); notifyReceiverEmail takes the phone number to notify. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `update-automation-notification-sms-action`

**Update notification-sms action**

Updates an automation SMS notification's receiver or message reference, not its text (update-notification-sms-draft). Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `add-automation-wait-action`

**Add wait action**

Adds a wait action before the next automation step: a delay, date field, birthday or calendar rule. delayType immediately means no wait. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `update-automation-wait-action`

**Update wait action**

Updates an automation wait action's delay for contacts reaching it from now on; contacts already waiting keep their scheduled time (move-contact-past-automation-wait releases one early). Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `add-automation-decision-action`

**Add decision action**

Adds a decision action that routes matching contacts to yes and others to no; an empty branch ends the flow. Build the condition from the operators get-automation-editor-capabilities reports; for open/click conditions, the field setting takes a message smart-tag ID, not a message ID. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `update-automation-decision-action`

**Update decision action**

Updates an automation decision's condition, changing future routing while keeping both branches and their actions. Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `add-automation-goal-action`

**Add goal action**

Adds an automation goal with a matching condition and one following action, without splitting the flow. Build the condition from the operators get-automation-editor-capabilities reports. A missing condition or successor is flagged by validate-automation. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `update-automation-goal-action`

**Update goal action**

Updates an automation goal's condition, revenue or savings without moving its successor. Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `add-automation-tag-action`

**Add tag action**

Adds an automation action that assigns a manual tag (tagID from search-automation-editor-references) to a contact when reached (smart tags are refused). This may start or alter other campaigns and automations. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `update-automation-tag-action`

**Update tag action**

Updates an automation tag action's manual tag assigned to future contacts, potentially starting other automations. Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `add-automation-untag-action`

**Add untag action**

Adds an automation action that removes a manual tag or SmartLink (tagID from search-automation-editor-references) from the contact when reached; smart tags are refused. This may alter other campaigns or automations. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `update-automation-untag-action`

**Update untag action**

Updates an automation untag action's manual tag or SmartLink removed from future contacts, potentially altering other automations. Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `add-automation-set-field-action`

**Add set-field action**

Adds an automation action that sets, clears or calculates a contact field according to customFieldOp (operators from get-automation-editor-capabilities). Running it replaces the prior value. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `update-automation-set-field-action`

**Update set-field action**

Updates an automation set-field action's contact field or write operation for future runs; existing contact values stay. Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `add-automation-go-to-action`

**Add goto action**

Adds a go-to action that moves the contact to targetActionId in the same automation, allowing loops or shared tails. The target must be an action ID from get-automation; the start action and other go-to actions are not valid targets. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `update-automation-go-to-action`

**Update goto action**

Updates an automation go-to action's targetActionId, changing future contact routing; the start action and other go-to actions are not valid targets. Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `add-automation-exit-action`

**Add exit action**

Adds an exit action that ends this automation for a contact, without removing them from the account or other automations. Nothing follows this action. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `update-automation-exit-action`

**Update exit action**

Updates an automation exit action's name or colour, not its effect. Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `add-automation-restart-action`

**Add restart action**

Adds an automation restart action: after at least five minutes, a contact change restarts the contact if the start condition still holds (time-based conditions may restart on their own). Optional tagID adds a manual tag on restart; smart tags are refused. Nothing follows it. This is the only way a contact re-enters the same automation without a new entry event. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `update-automation-restart-action`

**Update restart action**

Updates an automation restart action's name, colour or tagID, the manual tag added on restart (smart tags are refused). Timing is not configurable: after at least 5 minutes, the next contact change at which the start condition still holds restarts the contact. Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `add-automation-start-automation-action`

**Add start-automation action**

Adds an automation action that starts another automation (campaignID from search-automations) for the contact alongside this one; this flow neither waits nor ends. The contact enters only if it meets that automation’s start condition at that moment, otherwise nothing happens; a contact that finished it or was stopped out of it does not enter again. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `update-automation-start-automation-action`

**Update start-automation action**

Updates an automation start-automation action's target automation for future contacts; they still enter only if they meet its start condition. Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `add-automation-stop-automation-action`

**Add stop-automation action**

Adds an automation action that removes the contact from another automation (campaignID from search-automations), cancelling its pending steps for that contact. The contact counts as finished there and cannot re-enter it, neither through a restart nor a start-automation action. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `update-automation-stop-automation-action`

**Update stop-automation action**

Updates an automation stop-automation action's target automation for future contacts; they cannot re-enter it. Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `add-automation-split-test-action`

**Add split-test action**

Adds an automation split-test action that distributes arriving contacts across branches. Arms are configured in settings.splitTest; get-automation reports per arm the contacts it got and the conversions (contacts given its goal tag), get-automation-email-statistics the sends, opens and clicks of email arms. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `update-automation-split-test-action`

**Update split-test action**

Updates an automation split test's arms and allocation; only until the first contact reaches it, as in the app, afterwards the test is locked. Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `add-automation-outbound-action`

**Add outbound action**

Adds an automation outbound action that sends the contact's data to a configured webhook or connected service when reached. outboundID comes from search-automation-editor-references. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `update-automation-outbound-action`

**Update outbound action**

Updates an automation outbound action's configured outbound that receives contact data on future runs. Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `add-automation-name-detection-action`

**Add detect-name action**

Adds an automation name-detection action that guesses a first and last name from the contact's email address. The first name goes to customFieldID only while that field is empty or holds the same name; the last name to the optional customField2ID only while it is empty. Both must be different single-line text fields; guesses can be wrong. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `update-automation-name-detection-action`

**Update detect-name action**

Updates an automation name-detection action's first-name field customFieldID, last-name field customField2ID (empty for none), name or colour; both fields must be different single-line text fields. Existing contact values stay. Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `add-automation-gender-detection-action`

**Add detect-gender action**

Adds an automation gender-detection action that guesses from the source first-name field (customFieldID). It writes only an empty single-line text target field (customField2ID, not the source), and/or assigns manual tags; it needs a target with values or at least one tag. Guesses can be wrong. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `update-automation-gender-detection-action`

**Update detect-gender action**

Updates an automation gender-detection action's source first-name field, target field with its per-gender values, or per-gender manual tags; both fields are single-line text fields and must differ, smart tags are refused. Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `add-automation-unsubscribe-action`

**Add unsubscribe action**

Adds an automation action that unsubscribes the contact from the account when reached, stopping all mailings; a new opt-in is needed to resubscribe. Add only when requested. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `update-automation-unsubscribe-action`

**Update unsubscribe action**

Updates an automation unsubscribe action's name or colour, not its effect on future contacts. Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `settings`* — object
- `dryRun` — boolean
- `accountId` — null | integer (minimum 1)

## `estimate-automation-audience` · RI

**Estimate initial automation audience**

Estimates an automation's initial audience in batches. When continue=true, pass the returned offset, min and max to the next call. Future entrants are not a fixed recipient list.

Parameter:

- `automationId`* — integer (minimum 1)
- `offset` — integer (minimum 0)
- `min` — integer (minimum 0)
- `max` — integer (minimum 0)
- `accountId` — null | integer (minimum 1)

## `prepare-automation-activation` · RI

**Prepare automation activation**

Validates the current automation and returns its activation dialog link; it does not start, schedule or publish. The user reviews the current state and confirms activation there; the link is not bound to a saved snapshot.

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `accountId` — null | integer (minimum 1)

## `stop-automation` · DO

**Stop automation**

Requests an automation stop; pass confirm=true only after the user explicitly asked to stop it. Requires the current revision. Already dispatched email and external side effects cannot be recalled.

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `confirm` — boolean
- `accountId` — null | integer (minimum 1)

## `move-automation-contacts` · DO

**Move automation contacts**

Previews moving eligible contacts from source actions to a target action; confirm=true queues the move; pass it only after the user has seen the sources, target and effects and explicitly requested it. A queued response is not completion and has no completion tracker; counts may change before processing.

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `sourceActionIds`* — array<integer> (minItems 1; maxItems 100; uniqueItems)
- `targetActionId`* — integer (minimum 1)
- `confirm` — boolean
- `accountId` — null | integer (minimum 1)

## `search-automation-templates` · RI

**Search Marketing Campaign Templates**

Searches Business Automation Masterclass templates by purpose, best match first. Returns each template's start tag, email subjects, fields, tags, included automations and import URI. Reads only.

Parameter:

- `query` — null | string (maxLength 200): What the automation should do, in the user's words, e.g. Termin nachfassen or Bewertungen sammeln; omit to list all
- `module` — null | integer (minimum 1; maximum 99): Only templates of this Masterclass module
- `limit` — null | integer (minimum 1; maximum 50): Maximum number of templates to return, 1 to 50; default 10
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account of the access token

## `get-automation-template` · RI

**Get Marketing Campaign Template**

Reads an automation template's proposed import from a shared link or catalogue URI: included automations and objects, default account mappings, smart-import availability, blockers and untransferable references. Imports nothing.

Parameter:

- `templateLink`* — string (minLength 1; maxLength 2000): Template link as shared, e.g. https://app.klicktipp.com/template/1c5fz1uftzfzbe4b, or the uri of a catalogue template from search-automation-templates, e.g. klicktipp://automation-templates/teve
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account of the access token

## `import-automation-template`

**Import Marketing Campaign Template**

Imports an automation template from a shared link or catalogue URI, creating paused automations and creating or mapping their tags, fields, emails and outbounds. Sends nothing until activation. Created objects remain without undo; outbound limits, duplicate names or invalid mappings refuse before writing. Read it with get-automation-template first and settle name and mappings with the user.

Parameter:

- `templateLink`* — string (minLength 1; maxLength 2000): Template link as shared, or the uri of a catalogue template from search-automation-templates
- `automationName` — null | string (minLength 1; maxLength 250): Name of the new automation; omitted takes the template name. Smart import only
- `objectPrefix` — null | string (maxLength 100): Prefix put before the name of every created object; omitted means none. Smart import only
- `metaLabels` — array<string> (maxItems 100)
- `mappings` — array<object> (maxItems 500)
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account of the access token

## `get-automation-email` · RI

**Get automation-email settings**

Reads an automation email draft's settings, revision and campaign uses, and effectiveSender: the From name, address, reply address and sending domain the dispatch uses, with their source, resolved without sending. Its email ID is distinct from an automation action ID.

Parameter:

- `emailId`* — integer (minimum 1)
- `accountId` — null | integer (minimum 1)

## `create-automation-email-draft`

**Create automation-email draft**

Creates an independent drag-and-drop automation email draft with optional settings. Does not attach it to an action, publish or send it.

Parameter:

- `name`* — string (minLength 1; maxLength 250)
- `settings` — object
- `accountId` — null | integer (minimum 1)

## `update-automation-email-draft`

**Update automation-email draft**

Updates supplied automation email settings at the current revision. Refuses emails used by active or scheduled automations. Content and action assignment use separate tools; sends nothing.

Parameter:

- `emailId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `settings`* — object
- `accountId` — null | integer (minimum 1)

## `delete-automation-email-draft` · D

**Delete automation-email draft**

Deletes an unreferenced automation email draft at the current revision without undo. Automation actions remain; confirm only for the email the user asked to delete.

Parameter:

- `emailId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `confirm`* — boolean
- `accountId` — null | integer (minimum 1)

## `copy-automation-email`

**Copy Marketing Campaign Email**

Copies a campaign (automation) email into an independent draft using its revision from get-automation-email. Active sources can be copied; the original is unchanged. Does not attach the copy to a campaign or send.

Parameter:

- `emailId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `name`* — string (minLength 1; maxLength 250)
- `accountId` — null | integer (minimum 1)

## `send-automation-email-test` · DO

**Send Test Marketing Campaign Email**

Sends a published campaign (automation) email as a test to one specified address. An address not yet in the account becomes a tagged test contact and may start automations; name the address and disclose that effect before calling. Pass confirm=true only after the user requested this test. Emails without published content are refused; unpublished edits are not sent. Notification emails use send-notification-email-test.

Parameter:

- `emailId`* — integer (minimum 1)
- `recipientEmail`* — string (minLength 3; maxLength 250)
- `confirm` — boolean
- `accountId` — null | integer (minimum 1)

## `get-notification-email` · RI

**Get notification-email settings**

Reads a notification email draft's settings, revision and campaign uses, and effectiveSender: the From name, address, reply address and sending domain the dispatch uses, with their source, resolved without sending. Its email ID is distinct from an automation action ID.

Parameter:

- `emailId`* — integer (minimum 1)
- `accountId` — null | integer (minimum 1)

## `create-notification-email-draft`

**Create notification-email draft**

Creates an independent drag-and-drop notification email draft with optional settings. Does not attach it to an action, publish or send it.

Parameter:

- `name`* — string (minLength 1; maxLength 250)
- `settings` — object
- `accountId` — null | integer (minimum 1)

## `update-notification-email-draft`

**Update notification-email draft**

Updates supplied notification email settings at the current revision. Refuses emails used by active or scheduled automations. Content and action assignment use separate tools; sends nothing.

Parameter:

- `emailId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `settings`* — object
- `accountId` — null | integer (minimum 1)

## `delete-notification-email-draft` · D

**Delete notification-email draft**

Deletes an unreferenced notification email draft at the current revision without undo. Automation actions remain; confirm only for the email the user asked to delete.

Parameter:

- `emailId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `confirm`* — boolean
- `accountId` — null | integer (minimum 1)

## `send-notification-email-test` · DO

**Send Test Notification Email**

Sends a published notification email as a test to one specified address. An address not yet in the account becomes a tagged test contact and may start automations; name the address and disclose that effect before calling. Pass confirm=true only after the user requested this test. Emails without published content are refused; unpublished edits are not sent. Campaign emails use send-automation-email-test.

Parameter:

- `emailId`* — integer (minimum 1)
- `recipientEmail`* — string (minLength 3; maxLength 250)
- `confirm` — boolean
- `accountId` — null | integer (minimum 1)

## `send-email-for-gmail-placement-preview` · DO

**Request Gmail placement preview**

Sends a published campaign or notification email to the configured Gmail preview address and starts the inbox placement check; pass confirm=true only after the user explicitly requested it. Returns pending or reported state; get-email-gmail-placement-preview-result reads later results. Does not change campaign scheduling.

Parameter:

- `emailId`* — integer (minimum 1)
- `confirm` — boolean
- `accountId` — null | integer (minimum 1)

## `get-email-gmail-placement-preview-result` · RI

**Read Gmail preview result**

Reads the Gmail placement result requested by send-email-for-gmail-placement-preview. A reported result may contain an error or timeout; it is no delivery guarantee.

Parameter:

- `emailId`* — integer (minimum 1)
- `accountId` — null | integer (minimum 1)

## `get-automation-sms` · RI

**Get automation-sms settings**

Reads an automation SMS draft's settings, revision and campaign uses. Its SMS ID is distinct from an automation action ID.

Parameter:

- `smsId`* — integer (minimum 1)
- `accountId` — null | integer (minimum 1)

## `create-automation-sms-draft`

**Create automation-sms draft**

Creates an independent automation SMS draft with optional settings. Settings, even notes alone, save only with a provider and sender, as in the app; a provider must be connected in the account SMS settings. Does not attach it to an action or send it.

Parameter:

- `name`* — string (minLength 1; maxLength 250)
- `settings` — object
- `accountId` — null | integer (minimum 1)

## `update-automation-sms-draft`

**Update automation-sms draft**

Updates supplied automation SMS settings at the current revision. Settings save only while the SMS has a provider and sender, as in the app. Refuses SMS used by active or scheduled automations. Content and action assignment use separate tools; sends nothing.

Parameter:

- `smsId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `settings`* — object
- `accountId` — null | integer (minimum 1)

## `delete-automation-sms-draft` · D

**Delete automation-sms draft**

Deletes an unreferenced automation SMS draft at the current revision without undo. Automation actions remain; confirm only for the SMS the user asked to delete.

Parameter:

- `smsId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `confirm`* — boolean
- `accountId` — null | integer (minimum 1)

## `replace-automation-sms-content`

**Replace Marketing Campaign SMS Content**

Replaces automation SMS plaintext at its current draft revision. Empty text is allowed; active or scheduled uses are refused. Does not send. Notification SMS use replace-notification-sms-content.

Parameter:

- `smsId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `plain`* — string (maxLength 5000)
- `accountId` — null | integer (minimum 1)

## `copy-automation-sms`

**Copy Marketing Campaign SMS**

Copies an automation SMS into an independent draft with its own new smart tags. Active sources are allowed; the original stays. Does not attach or send the copy. Creation is not automatically retryable.

Parameter:

- `smsId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `name`* — string (minLength 1; maxLength 250)
- `accountId` — null | integer (minimum 1)

## `send-automation-sms-test` · DO

**Send Test Marketing Campaign SMS**

Sends a saved automation SMS test to the specified phone number via its provider, charging SMS credits without recall. Personalization uses a matching or random account contact. Pass confirm=true only when the user asked for a test to exactly this number; do not automatically retry.

Parameter:

- `smsId`* — integer (minimum 1)
- `recipientPhone`* — string (pattern `^\+[1-9][0-9]{5,14}$`)
- `confirm`* — boolean
- `accountId` — null | integer (minimum 1)

## `get-notification-sms` · RI

**Get notification-sms settings**

Reads a notification SMS draft's settings, revision and campaign uses. Its SMS ID is distinct from an automation action ID.

Parameter:

- `smsId`* — integer (minimum 1)
- `accountId` — null | integer (minimum 1)

## `create-notification-sms-draft`

**Create notification-sms draft**

Creates an independent notification SMS draft with optional settings. Settings, even notes alone, save only with a provider and sender, as in the app; a provider must be connected in the account SMS settings. Does not attach it to an action or send it.

Parameter:

- `name`* — string (minLength 1; maxLength 250)
- `settings` — object
- `accountId` — null | integer (minimum 1)

## `update-notification-sms-draft`

**Update notification-sms draft**

Updates supplied notification SMS settings at the current revision. Settings save only while the SMS has a provider and sender, as in the app. Refuses SMS used by active or scheduled automations. Content and action assignment use separate tools; sends nothing.

Parameter:

- `smsId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `settings`* — object
- `accountId` — null | integer (minimum 1)

## `delete-notification-sms-draft` · D

**Delete notification-sms draft**

Deletes an unreferenced notification SMS draft at the current revision without undo. Automation actions remain; confirm only for the SMS the user asked to delete.

Parameter:

- `smsId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `confirm`* — boolean
- `accountId` — null | integer (minimum 1)

## `replace-notification-sms-content`

**Replace Notification SMS Content**

Replaces notification SMS plaintext at its current draft revision. Empty text is allowed; active or scheduled uses are refused. Does not send. Automation SMS use replace-automation-sms-content.

Parameter:

- `smsId`* — integer (minimum 1)
- `revision`* — string (pattern `^[a-f0-9]{64}$`)
- `plain`* — string (maxLength 5000)
- `accountId` — null | integer (minimum 1)

## `send-notification-sms-test` · DO

**Send Test Notification SMS**

Sends a saved notification SMS test to the specified phone number via its provider, charging SMS credits without recall. Personalization uses a matching or random account contact. Pass confirm=true only when the user asked for a test to exactly this number; do not automatically retry.

Parameter:

- `smsId`* — integer (minimum 1)
- `recipientPhone`* — string (pattern `^\+[1-9][0-9]{5,14}$`)
- `confirm`* — boolean
- `accountId` — null | integer (minimum 1)
