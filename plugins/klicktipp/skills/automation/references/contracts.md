# Die veröffentlichten Verträge — Automationen

Wort für Wort das, was der Server in `tools/list` für die 92 Werkzeuge dieses Skills
ausliefert: Beschreibung, Annotationen, jeder Parameter mit Typ, Grenzen und Beschreibung. Ein `*`
markiert Pflichtparameter. `R` liest nur · `D` löscht oder ersetzt ohne Undo · `O` erreicht etwas
außerhalb des Kontos · `I` ein zweiter gleicher Aufruf ändert nichts mehr.

Diese Datei spiegelt den Server, sie interpretiert ihn nicht: ändert sich eine
Werkzeugbeschreibung, wird sie hier wörtlich nachgezogen. Welcher Aktionstyp was tut und was in
`settings` gehört, steht in [actions.md](actions.md); die Statistik der Automationen beim Skill
`dashboard`. Der Objekt-Parameter `settings` der Aktionswerkzeuge ist hier nur als `object` genannt — sein
Schema liefert `get-automation-editor-capabilities`.

## Inhalt

`get-automation` · `validate-automation` · `create-automation-draft` · `update-automation-draft` ·
`delete-automation-draft` · `delete-automation` · `get-campaign-dependencies` ·
`move-automation-action` · `copy-automation-action` · `delete-automation-action` ·
`get-automation-editor-capabilities` · `search-automation-editor-references` ·
`update-automation-start-action` · `add-automation-email-action` · `update-automation-email-action`
· `add-automation-sms-action` · `update-automation-sms-action` ·
`add-automation-notification-email-action` · `update-automation-notification-email-action` ·
`add-automation-notification-sms-action` · `update-automation-notification-sms-action` ·
`add-automation-wait-action` · `update-automation-wait-action` · `add-automation-decision-action` ·
`update-automation-decision-action` · `add-automation-goal-action` · `update-automation-goal-action`
· `add-automation-tag-action` · `update-automation-tag-action` · `add-automation-untag-action` ·
`update-automation-untag-action` · `add-automation-set-field-action` ·
`update-automation-set-field-action` · `add-automation-go-to-action` ·
`update-automation-go-to-action` · `add-automation-exit-action` · `update-automation-exit-action` ·
`add-automation-restart-action` · `update-automation-restart-action` ·
`add-automation-start-automation-action` · `update-automation-start-automation-action` ·
`add-automation-stop-automation-action` · `update-automation-stop-automation-action` ·
`add-automation-split-test-action` · `update-automation-split-test-action` ·
`add-automation-outbound-action` · `update-automation-outbound-action` ·
`add-automation-name-detection-action` · `update-automation-name-detection-action` ·
`add-automation-gender-detection-action` · `update-automation-gender-detection-action` ·
`add-automation-unsubscribe-action` · `update-automation-unsubscribe-action` ·
`estimate-automation-audience` · `prepare-automation-activation` · `stop-automation` ·
`move-automation-contacts` · `get-contact-automation-status` · `move-contact-past-automation-wait` ·
`search-automation-templates` · `get-automation-template` · `import-automation-template` ·
`get-automation-email` · `create-automation-email-draft` · `update-automation-email-draft` ·
`delete-automation-email-draft` · `copy-automation-email` · `send-automation-email-test` ·
`preview-personalized-email` · `get-notification-email` · `create-notification-email-draft` ·
`update-notification-email-draft` · `delete-notification-email-draft` · `copy-notification-email` ·
`send-notification-email-test` · `send-email-for-gmail-placement-preview` ·
`get-email-gmail-placement-preview-result` · `get-automation-sms` · `create-automation-sms-draft` ·
`update-automation-sms-draft` · `delete-automation-sms-draft` · `replace-automation-sms-content` ·
`copy-automation-sms` · `send-automation-sms-test` · `check-sms-readiness` · `get-notification-sms`
· `create-notification-sms-draft` · `update-notification-sms-draft` ·
`delete-notification-sms-draft` · `copy-notification-sms` · `replace-notification-sms-content` ·
`send-notification-sms-test`

## `get-automation` · RI

**Read automation**

Reads an automation graph with stable action IDs, revision, status, validation findings and editor URL. The findings are those of validate-automation. Sends and activates nothing.

Parameter:

- `automationId`* — integer (minimum 1)
- `accountId` — null | integer (minimum 1)

## `validate-automation` · RI

**Validate automation**

Validates a saved automation and returns action-specific findings and the checked revision. Checks the graph and settings of each action, the subject, content and publication of each email, whether each email can be sent from its sender address and domain (code "email sender cannot send"), and whether the tag of each condition has the type its operator takes (code "condition tag has wrong type"; the editor shows such a condition empty, rewrite it with the operator the message names). Both are warnings: activation does not check them. Does not check spam score or links. Sends and activates nothing.

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
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `settings`* — object
  - `name` — string (minLength 1; maxLength 250)
  - `notes` — string (maxLength 10000)
  - `utmCampaignName` — string (maxLength 250)
  - `metaLabels` — array<string> (maxItems 100)
  - `multipleSend` — integer (einer von `0`)
- `accountId` — null | integer (minimum 1)

## `delete-automation-draft` · D

**Delete automation draft**

Deletes an inactive automation draft only when it has no contact history or dependencies. Referenced emails remain. Requires the current revision and explicit confirmation; there is no undo.

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `confirm` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `delete-automation` · D

**Delete Automation**

Deletes an automation that is neither active nor scheduled, including waiting contacts, statistics, system tags and goal history, without undo. With contact history the first call is refused with counts; repeat with deleteContactHistory=true. Other dependencies block deletion. Referenced emails remain. Stop an active automation first with stop-automation.

Parameter:

- `automationId`* — integer (minimum 1): ID of the automation to delete
- `revision`* — string (Muster `^[a-f0-9]{64}$`): Current revision from get-automation
- `confirm` — boolean (Default `false`): true only when the user asked to delete this automation
- `deleteContactHistory` — boolean (Default `false`): true only after the user agreed to lose its contact history; the first refusal names it
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account of the access token

## `get-campaign-dependencies` · RI

**Get Campaign Dependencies**

Lists dependencies of an email or SMS newsletter, follow-up or automation, with links to the automations and campaigns that still use it. These references block deletion until removed. Reads only.

Parameter:

- `campaignId`* — integer (minimum 1): ID of a newsletter, SMS newsletter, follow-up or automation
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account of the access token

## `move-automation-action`

**Move automation action**

Moves an automation action by stable ID in an inactive graph. subtree moves its following graph to an open branch; a populated decision requires subtree. Moving one regular action reconnects its old neighbours; goto references retain their IDs. Requires the current revision; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `subtree` — boolean (Default `false`)
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `copy-automation-action`

**Copy automation action**

Copies an automation action or subtree into an inactive graph, assigning new IDs but sharing referenced emails. A single copied decision has empty branches except its insertion-point successor. Split tests are copied independently; subtrees require an open destination. Requires the current revision; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `subtree` — boolean (Default `false`)
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `delete-automation-action` · D

**Delete automation action**

Deletes an action from an inactive automation, discarding the selected branch or preserving a chosen successor. Decision choices are keep_yes, keep_no or subtree; other actions use keep_next or subtree. The start action cannot be deleted; incoming goto references must be changed first. Emails stay. dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `mode`* — string (einer von `keep_next`, `keep_yes`, `keep_no`, `subtree`)
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `get-automation-editor-capabilities` · RI

**Read automation capabilities**

Reads automation editor capabilities: email and SMS actions with closed settings schemas and required add fields, engine condition and field operators, the tag type each tag condition takes (conditionTagTypes: "tagged with" a manual tag, "subscribed by apikey" an API-key smart tag), account-authorized plugin conditions. actionType optionally limits it to a graph type from get-automation. Integration availability also depends on the selected reference; resolve IDs with search-automation-editor-references first.

Parameter:

- `actionType` — null | string (einer von `start`, `email`, `sms`, `notify by sms`, `notify by email`, `wait`, `decision`, `goal`, `tagging`, `untagging`, `setfield`, `goto`, `exit`, `restart`, `start automation`, `stop automation`, `splittest`, `outbound`, `facebook audience add`, `facebook audience remove`, `detect name`, `detect gender`, `fullcontact`, `website_enrichment`, `unsubscribe`, `null`)
- `accountId` — null | integer (minimum 1)

## `search-automation-editor-references` · RI

**Find automation references**

Searches existing emails, SMS, tags, fields, signatures, calendars, outbounds, Facebook audiences, automations or saved segment selectors by name to resolve automation editor IDs; returns only IDs and names. Email IDs are message references; event conditions use their smart tags from get-automation-email or get-notification-email. Create missing tags or fields with the tag/field tools.

Parameter:

- `kind`* — string (einer von `automation-email`, `notification-email`, `automation-sms`, `notification-sms`, `tag`, `field`, `signature`, `calendar`, `outbound`, `facebook-audience`, `automation`, `segment`)
- `query` — string (maxLength 250; Default ``)
- `offset` — integer (minimum 0; Default `0`)
- `limit` — integer (minimum 1; maximum 100; Default `25`)
- `accountId` — null | integer (minimum 1)

## `update-automation-start-action`

**Update start action**

Updates an automation's existing start action to control who enters and when. An empty condition means only another automation can start it. A tag condition takes only a tag of the type get-automation-editor-capabilities names for its operator (conditionTagTypes). Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `settings`* — object
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
  - `segmentsOpAND` — boolean
  - `segments` — array<object> (maxItems 100)
    - `conditionsOpAND`* — boolean
    - `conditions`* — array<object> (maxItems 100)
      - `op`* — string (minLength 1; maxLength 150)
      - `field`* — string | integer
      - `value` — string | number | boolean | array
      - `value2` — string | number | boolean | array
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `add-automation-email-action`

**Add email action**

Adds an automation email action that sends a referenced email (emailID, created with create-automation-email-draft) when the contact reaches it. emailID may be left out or 0, as in the app, to build the steps first and write the emails later; do not create empty emails for that. validate-automation reports a step without an email, and the automation cannot be activated until each has one. Editing the shared email affects every action that references it. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
  - `success_tag_id` — integer (minimum 0): Only for an email with AI-generated content: manual tag set when generating the content succeeded; 0 for none. Not used for other emails.
  - `error_tag_id` — integer (minimum 0): Only for an email with AI-generated content: manual tag set when generating the content failed or timed out; 0 for none. Not used for other emails.
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
  - `emailID` — integer (minimum 0): Email sent by this step; 0 for none yet, which the automation reports and which keeps it from being activated.
  - `ignoreSubscriberStatus` — integer (einer von `0`, `1`)
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `update-automation-email-action`

**Update email action**

Updates an automation email action's settings or referenced email, not its content (update-automation-email-draft). emailID 0 detaches the email, as clearing the field in the app does; the email itself stays and can then be deleted if nothing else uses it. Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `settings`* — object
  - `success_tag_id` — integer (minimum 0): Only for an email with AI-generated content: manual tag set when generating the content succeeded; 0 for none. Not used for other emails.
  - `error_tag_id` — integer (minimum 0): Only for an email with AI-generated content: manual tag set when generating the content failed or timed out; 0 for none. Not used for other emails.
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
  - `emailID` — integer (minimum 0): Email sent by this step; 0 for none yet, which the automation reports and which keeps it from being activated.
  - `ignoreSubscriberStatus` — integer (einer von `0`, `1`)
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `add-automation-sms-action`

**Add SMS action**

Adds an automation SMS action that sends a referenced SMS to the contact when reached. emailID takes an automation SMS draft ID (create-automation-sms-draft), not an email ID. Requires SMS marketing, an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
  - `emailID`* — integer (minimum 1)
  - `ignoreSubscriberStatus` — integer (einer von `0`, `1`)
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `update-automation-sms-action`

**Update SMS action**

Updates an automation SMS action's settings or referenced SMS draft (emailID), not the message text (update-automation-sms-draft). Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `settings`* — object
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
  - `emailID` — integer (minimum 1)
  - `ignoreSubscriberStatus` — integer (einer von `0`, `1`)
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `add-automation-notification-email-action`

**Add notification-email action**

Adds an automation email notification action for an internal address, not the contact. emailID references a notification email draft (create-notification-email-draft); notifyReceiverEmail takes an address or dispatchProfile. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
  - `emailID`* — integer (minimum 1)
  - `notifyReceiverEmail`* — string (minLength 1; maxLength 1000): Address the notification goes to, or dispatchProfile to pick it by the contact's tags: the receiver address of the signature those tags select, as "Automatically by tags (dispatch profile)" in the app.
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `update-automation-notification-email-action`

**Update notification-email action**

Updates an automation email notification's receiver or message reference, not its body (update-notification-email-draft). Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `settings`* — object
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
  - `emailID` — integer (minimum 1)
  - `notifyReceiverEmail` — string (minLength 1; maxLength 1000): Address the notification goes to, or dispatchProfile to pick it by the contact's tags: the receiver address of the signature those tags select, as "Automatically by tags (dispatch profile)" in the app.
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `add-automation-notification-sms-action`

**Add notification-sms action**

Adds an automation SMS notification action for an internal number, not the contact. emailID references a notification SMS draft (create-notification-sms-draft); notifyReceiverEmail takes the phone number to notify. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
  - `emailID`* — integer (minimum 1)
  - `notifyReceiverEmail`* — string (minLength 1; maxLength 1000): Mobile number the notification SMS goes to, e.g. +491701234567; not an email address. dispatchProfile is not available for an SMS.
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `update-automation-notification-sms-action`

**Update notification-sms action**

Updates an automation SMS notification's receiver or message reference, not its text (update-notification-sms-draft). Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `settings`* — object
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
  - `emailID` — integer (minimum 1)
  - `notifyReceiverEmail` — string (minLength 1; maxLength 1000): Mobile number the notification SMS goes to, e.g. +491701234567; not an email address. dispatchProfile is not available for an SMS.
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `add-automation-wait-action`

**Add wait action**

Adds a wait action before the next automation step: a delay, date field, birthday or calendar rule. delayType immediately means no wait. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
  - `delayType`* — string (einer von `immediately`, `seconds`, `minutes`, `hours`, `days`, `weeks`, `months`, `years`, `from field`, `customfield minutes`, `customfield hours`, `customfield days`, `customfield weeks`, `customfield months`, `customfield years`, `birthday`, `calendar`, `limiter`)
  - `delayTime` — integer (minimum -999; maximum 999)
  - `delayField` — string (minLength 1; maxLength 100)
  - `delayMonth` — array<integer> (maxItems 100)
  - `delayWeeks` — array<integer> (maxItems 100)
  - `delayDayOfMonth` — array<integer> (maxItems 100)
  - `delayDayOfWeek` — array<integer> (maxItems 100)
  - `delayHours` — array<integer> (maxItems 100)
  - `calendarIDs` — array<integer> (maxItems 100)
  - `delaySecondsOfDay` — integer (minimum -1; maximum 86399)
  - `limiterPeriod` — string (einer von `hours`, `days`, `weeks`, `months`, `years`)
  - `limiterValue` — integer (minimum 1)
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `update-automation-wait-action`

**Update wait action**

Updates an automation wait action's delay for contacts reaching it from now on; contacts already waiting keep their scheduled time (move-contact-past-automation-wait releases one early). Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `settings`* — object
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
  - `delayType` — string (einer von `immediately`, `seconds`, `minutes`, `hours`, `days`, `weeks`, `months`, `years`, `from field`, `customfield minutes`, `customfield hours`, `customfield days`, `customfield weeks`, `customfield months`, `customfield years`, `birthday`, `calendar`, `limiter`)
  - `delayTime` — integer (minimum -999; maximum 999)
  - `delayField` — string (minLength 1; maxLength 100)
  - `delayMonth` — array<integer> (maxItems 100)
  - `delayWeeks` — array<integer> (maxItems 100)
  - `delayDayOfMonth` — array<integer> (maxItems 100)
  - `delayDayOfWeek` — array<integer> (maxItems 100)
  - `delayHours` — array<integer> (maxItems 100)
  - `calendarIDs` — array<integer> (maxItems 100)
  - `delaySecondsOfDay` — integer (minimum -1; maximum 86399)
  - `limiterPeriod` — string (einer von `hours`, `days`, `weeks`, `months`, `years`)
  - `limiterValue` — integer (minimum 1)
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `add-automation-decision-action`

**Add decision action**

Adds a decision action that routes matching contacts to yes and others to no; an empty branch ends the flow. Build the condition from the operators get-automation-editor-capabilities reports; for open/click conditions, the field setting takes a message smart-tag ID, not a message ID. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
  - `segmentsOpAND`* — boolean
  - `segments`* — array<object> (maxItems 100)
    - `conditionsOpAND`* — boolean
    - `conditions`* — array<object> (maxItems 100)
      - `op`* — string (minLength 1; maxLength 150)
      - `field`* — string | integer
      - `value` — string | number | boolean | array
      - `value2` — string | number | boolean | array
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `update-automation-decision-action`

**Update decision action**

Updates an automation decision's condition, changing future routing while keeping both branches and their actions. Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `settings`* — object
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
  - `segmentsOpAND` — boolean
  - `segments` — array<object> (maxItems 100)
    - `conditionsOpAND`* — boolean
    - `conditions`* — array<object> (maxItems 100)
      - `op`* — string (minLength 1; maxLength 150)
      - `field`* — string | integer
      - `value` — string | number | boolean | array
      - `value2` — string | number | boolean | array
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `add-automation-goal-action`

**Add goal action**

Adds an automation goal with a matching condition and one following action, without splitting the flow. Build the condition from the operators get-automation-editor-capabilities reports. A missing condition or successor is flagged by validate-automation. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
  - `segmentsOpAND`* — boolean
  - `segments`* — array<object> (maxItems 100)
    - `conditionsOpAND`* — boolean
    - `conditions`* — array<object> (maxItems 100)
      - `op`* — string (minLength 1; maxLength 150)
      - `field`* — string | integer
      - `value` — string | number | boolean | array
      - `value2` — string | number | boolean | array
  - `revenue` — number: Revenue of reaching the goal, in cents: 1000 is 10.00 EUR.
  - `savings` — number: Cost saving of reaching the goal, in cents: 1000 is 10.00 EUR.
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `update-automation-goal-action`

**Update goal action**

Updates an automation goal's condition, revenue or savings without moving its successor. Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `settings`* — object
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
  - `segmentsOpAND` — boolean
  - `segments` — array<object> (maxItems 100)
    - `conditionsOpAND`* — boolean
    - `conditions`* — array<object> (maxItems 100)
      - `op`* — string (minLength 1; maxLength 150)
      - `field`* — string | integer
      - `value` — string | number | boolean | array
      - `value2` — string | number | boolean | array
  - `revenue` — number: Revenue of reaching the goal, in cents: 1000 is 10.00 EUR.
  - `savings` — number: Cost saving of reaching the goal, in cents: 1000 is 10.00 EUR.
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `add-automation-tag-action`

**Add tag action**

Adds an automation action that assigns a manual tag (tagID from search-automation-editor-references) to a contact when reached (smart tags are refused). This may start or alter other campaigns and automations. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
  - `tagID`* — integer (minimum 1)
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `update-automation-tag-action`

**Update tag action**

Updates an automation tag action's manual tag assigned to future contacts, potentially starting other automations. Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `settings`* — object
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
  - `tagID` — integer (minimum 1)
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `add-automation-untag-action`

**Add untag action**

Adds an automation action that removes a manual tag or SmartLink (tagID from search-automation-editor-references) from the contact when reached; smart tags are refused. This may alter other campaigns or automations. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
  - `tagID`* — integer (minimum 1)
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `update-automation-untag-action`

**Update untag action**

Updates an automation untag action's manual tag or SmartLink removed from future contacts, potentially altering other automations. Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `settings`* — object
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
  - `tagID` — integer (minimum 1)
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `add-automation-set-field-action`

**Add set-field action**

Adds an automation action that sets, clears or calculates a contact field according to customFieldOp (operators from get-automation-editor-capabilities). Running it replaces the prior value. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
  - `customFieldID`* — string (minLength 1; maxLength 100)
  - `customFieldOp`* — string (einer von `set field value`, `copy from field`, `copy from subscriber`, `empty field`, `prepend string`, `append string`, `replace string`, `generate CRC32 hash`, `generate MD5 hash`, `generate SHA1 hash`, `generate SHA256 hash`, `generate SHA384 hash`, `generate SHA512 hash`, `add number`, `subtract number`, `random number`, `truncate url query`, `truncate url path`, `datetime now`, `datetime increase`, `datetime decrease`, `now next month`, `now next year`, `field next month`, `field next year`, `ultimo`, `easter date`, `time now`, `floor full hour`, `ceil full hour`, `round full hour`)
  - `customFieldValue` — string (maxLength 1000): For "set field value": a date as YYYY-MM-DD, a time as HH:MM, a date and time as YYYY-MM-DD HH:MM (no seconds, no time zone). For "datetime now/increase/decrease": the amount and unit, e.g. "+3 days" (units minutes, hours, days, weeks, month, years), on a date-and-time field followed by HH:MM when customFieldValue2 is "set field value". A changed operation starts from empty values.
  - `customFieldValue2` — string (maxLength 1000): For "datetime now/increase/decrease" on a date-and-time field, the time: "datetime now" (keep the current time), "set field value" (the time in customFieldValue), "round full hour", "floor full hour" or "ceil full hour".
  - `delayDayOfWeek` — array<integer> (minItems 1; maxItems 7): For "datetime now/increase/decrease": the weekdays (1 Monday to 7 Sunday) the calculated date may fall on; it moves on a day until it does. Omit for all seven.
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `update-automation-set-field-action`

**Update set-field action**

Updates an automation set-field action's contact field or write operation for future runs; existing contact values stay. Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `settings`* — object
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
  - `customFieldID` — string (minLength 1; maxLength 100)
  - `customFieldOp` — string (einer von `set field value`, `copy from field`, `copy from subscriber`, `empty field`, `prepend string`, `append string`, `replace string`, `generate CRC32 hash`, `generate MD5 hash`, `generate SHA1 hash`, `generate SHA256 hash`, `generate SHA384 hash`, `generate SHA512 hash`, `add number`, `subtract number`, `random number`, `truncate url query`, `truncate url path`, `datetime now`, `datetime increase`, `datetime decrease`, `now next month`, `now next year`, `field next month`, `field next year`, `ultimo`, `easter date`, `time now`, `floor full hour`, `ceil full hour`, `round full hour`)
  - `customFieldValue` — string (maxLength 1000): For "set field value": a date as YYYY-MM-DD, a time as HH:MM, a date and time as YYYY-MM-DD HH:MM (no seconds, no time zone). For "datetime now/increase/decrease": the amount and unit, e.g. "+3 days" (units minutes, hours, days, weeks, month, years), on a date-and-time field followed by HH:MM when customFieldValue2 is "set field value". A changed operation starts from empty values.
  - `customFieldValue2` — string (maxLength 1000): For "datetime now/increase/decrease" on a date-and-time field, the time: "datetime now" (keep the current time), "set field value" (the time in customFieldValue), "round full hour", "floor full hour" or "ceil full hour".
  - `delayDayOfWeek` — array<integer> (minItems 1; maxItems 7): For "datetime now/increase/decrease": the weekdays (1 Monday to 7 Sunday) the calculated date may fall on; it moves on a day until it does. Omit for all seven.
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `add-automation-go-to-action`

**Add goto action**

Adds a go-to action that moves the contact to targetActionId in the same automation, allowing loops or shared tails. The target must be an action ID from get-automation; the start action and other go-to actions are not valid targets. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
  - `targetActionId`* — integer (minimum 0)
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `update-automation-go-to-action`

**Update goto action**

Updates an automation go-to action's targetActionId, changing future contact routing; the start action and other go-to actions are not valid targets. Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `settings`* — object
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
  - `targetActionId` — integer (minimum 0)
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `add-automation-exit-action`

**Add exit action**

Adds an exit action that ends this automation for a contact, without removing them from the account or other automations. Nothing follows this action. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `update-automation-exit-action`

**Update exit action**

Updates an automation exit action's name or colour, not its effect. Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `settings`* — object
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `add-automation-restart-action`

**Add restart action**

Adds an automation restart action: after at least five minutes, a contact change restarts the contact if the start condition still holds (time-based conditions may restart on their own). Optional tagID adds a manual tag on restart; smart tags are refused. Nothing follows it. This is the only way a contact re-enters the same automation without a new entry event. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
  - `tagID` — integer (minimum 0): Manual tag put on the contact when it is restarted; 0 for none.
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `update-automation-restart-action`

**Update restart action**

Updates an automation restart action's name, colour or tagID, the manual tag added on restart (smart tags are refused). Timing is not configurable: after at least 5 minutes, the next contact change at which the start condition still holds restarts the contact. Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `settings`* — object
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
  - `tagID` — integer (minimum 0): Manual tag put on the contact when it is restarted; 0 for none.
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `add-automation-start-automation-action`

**Add start-automation action**

Adds an automation action that starts another automation (campaignID from search-automations) for the contact alongside this one; this flow neither waits nor ends. The contact enters only if it meets that automation’s start condition at that moment, otherwise nothing happens; a contact that finished it or was stopped out of it does not enter again. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
  - `campaignID`* — integer (minimum 1)
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `update-automation-start-automation-action`

**Update start-automation action**

Updates an automation start-automation action's target automation for future contacts; they still enter only if they meet its start condition. Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `settings`* — object
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
  - `campaignID` — integer (minimum 1)
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `add-automation-stop-automation-action`

**Add stop-automation action**

Adds an automation action that removes the contact from another automation (campaignID from search-automations), cancelling its pending steps for that contact. The contact counts as finished there and cannot re-enter it, neither through a restart nor a start-automation action. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
  - `campaignID`* — integer (minimum 1)
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `update-automation-stop-automation-action`

**Update stop-automation action**

Updates an automation stop-automation action's target automation for future contacts; they cannot re-enter it. Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `settings`* — object
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
  - `campaignID` — integer (minimum 1)
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `add-automation-split-test-action`

**Add split-test action**

Adds an automation split-test action that distributes arriving contacts across branches. Arms are configured in settings.splitTest; get-automation reports per arm the contacts it got and the conversions (contacts given its goal tag), get-automation-email-statistics the sends, opens and clicks of email arms. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
  - `splitTest` — object
    - `revision` — string (Muster `^[a-f0-9]{64}$`)
    - `durationSeconds` — integer (minimum 1; maximum 99999999)
    - `variants` — array<object> (minItems 2; maxItems 20)
      - `kind`* — string (einer von `email`, `sms`, `automation`, `outbound`, `tag`)
      - `entityId`* — integer (minimum 1)
      - `weight`* — integer (minimum 1; maximum 99)
      - `goalTagId`* — integer (minimum 1)
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `update-automation-split-test-action`

**Update split-test action**

Updates an automation split test's arms and allocation; only until the first contact reaches it, as in the app, afterwards the test is locked. Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `settings`* — object
  - `splitTest` — object
    - `revision` — string (Muster `^[a-f0-9]{64}$`)
    - `durationSeconds` — integer (minimum 1; maximum 99999999)
    - `variants` — array<object> (minItems 2; maxItems 20)
      - `kind`* — string (einer von `email`, `sms`, `automation`, `outbound`, `tag`)
      - `entityId`* — integer (minimum 1)
      - `weight`* — integer (minimum 1; maximum 99)
      - `goalTagId`* — integer (minimum 1)
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `add-automation-outbound-action`

**Add outbound action**

Adds an automation outbound action that hands the contact's data to the selected outbound when reached. outboundID comes from search-automation-editor-references. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
  - `outboundID`* — integer (minimum 1)
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `update-automation-outbound-action`

**Update outbound action**

Updates an automation outbound action's configured outbound that receives contact data on future runs. Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `settings`* — object
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
  - `outboundID` — integer (minimum 1)
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `add-automation-name-detection-action`

**Add detect-name action**

Adds an automation name-detection action that guesses a first and last name from the contact's email address. The first name goes to customFieldID only while that field is empty or holds the same name; the last name to the optional customField2ID only while it is empty. Both must be different single-line text fields; guesses can be wrong. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
  - `customField2ID` — string (maxLength 100): Single-line text field the last name is written into, another one than customFieldID; empty for none. Written only while it is empty.
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
  - `customFieldID`* — string (minLength 1; maxLength 100): Single-line text field the first name is written into. If it already holds a different first name, nothing is written.
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `update-automation-name-detection-action`

**Update detect-name action**

Updates an automation name-detection action's first-name field customFieldID, last-name field customField2ID (empty for none), name or colour; both fields must be different single-line text fields. Existing contact values stay. Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `settings`* — object
  - `customField2ID` — string (maxLength 100): Single-line text field the last name is written into, another one than customFieldID; empty for none. Written only while it is empty.
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
  - `customFieldID` — string (minLength 1; maxLength 100): Single-line text field the first name is written into. If it already holds a different first name, nothing is written.
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `add-automation-gender-detection-action`

**Add detect-gender action**

Adds an automation gender-detection action that guesses from the source first-name field (customFieldID). It writes only an empty single-line text target field (customField2ID, not the source), and/or assigns manual tags; it needs a target with values or at least one tag. Guesses can be wrong. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
  - `customField2ID` — string (maxLength 100): Single-line text field the result is written into, not customFieldID; empty for none. Needs at least one of the three values. Written only while it is empty, a value already there is kept.
  - `customFieldValue` — string (maxLength 1000): Value written into customField2ID for a male first name.
  - `customFieldValue2` — string (maxLength 1000): Value written into customField2ID for a female first name.
  - `customFieldValue3` — string (maxLength 1000): Value written into customField2ID for a unisex or unknown first name.
  - `tagID` — integer (minimum 0): Manual tag set for a male first name; 0 for none.
  - `tag2ID` — integer (minimum 0): Manual tag set for a female first name; 0 for none.
  - `tag3ID` — integer (minimum 0): Manual tag set for a unisex or unknown first name; 0 for none.
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
  - `customFieldID`* — string (minLength 1; maxLength 100): Single-line text field holding the first name (the app's first-name field); it is only read.
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `update-automation-gender-detection-action`

**Update detect-gender action**

Updates an automation gender-detection action's source first-name field, target field with its per-gender values, or per-gender manual tags; both fields are single-line text fields and must differ, smart tags are refused. Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `settings`* — object
  - `customField2ID` — string (maxLength 100): Single-line text field the result is written into, not customFieldID; empty for none. Needs at least one of the three values. Written only while it is empty, a value already there is kept.
  - `customFieldValue` — string (maxLength 1000): Value written into customField2ID for a male first name.
  - `customFieldValue2` — string (maxLength 1000): Value written into customField2ID for a female first name.
  - `customFieldValue3` — string (maxLength 1000): Value written into customField2ID for a unisex or unknown first name.
  - `tagID` — integer (minimum 0): Manual tag set for a male first name; 0 for none.
  - `tag2ID` — integer (minimum 0): Manual tag set for a female first name; 0 for none.
  - `tag3ID` — integer (minimum 0): Manual tag set for a unisex or unknown first name; 0 for none.
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
  - `customFieldID` — string (minLength 1; maxLength 100): Single-line text field holding the first name (the app's first-name field); it is only read.
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `add-automation-unsubscribe-action`

**Add unsubscribe action**

Adds an automation action that unsubscribes the contact from the account when reached, stopping all mailings; a new opt-in is needed to resubscribe. Add only when requested. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving. Place it with afterActionId and branch (next after a regular action, yes/no after a decision).

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `afterActionId`* — integer (minimum 1)
- `branch`* — string (einer von `next`, `yes`, `no`)
- `settings`* — object
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `update-automation-unsubscribe-action`

**Update unsubscribe action**

Updates an automation unsubscribe action's name or colour, not its effect on future contacts. Omitted settings stay; supplied lists replace prior lists. Requires an unscheduled, inactive automation and its current revision from get-automation; dryRun previews without saving.

Parameter:

- `automationId`* — integer (minimum 1)
- `actionId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `settings`* — object
  - `name` — string (maxLength 250)
  - `color` — string (einer von ``, `teal-light`, `peach-light`, `pink-light`, `violet-light`, `blue-light`, `silver-light`, `brown-light`, `yellow-light`, `green-light`, `coldgreen-light`, `teal-dark`, `peach-dark`, `pink-dark`, `violet-dark`, `blue-dark`, `silver-dark`, `brown-dark`, `yellow-dark`, `green-dark`, `coldgreen-dark`): Card colour from the editor palette, e.g. green-dark or blue-light. An empty string uses the default colour of the action type.
- `dryRun` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `estimate-automation-audience` · RI

**Estimate initial automation audience**

Estimates an automation's initial audience in batches. When continue=true, pass the returned offset, min and max to the next call. Future entrants are not a fixed recipient list.

Parameter:

- `automationId`* — integer (minimum 1)
- `offset` — integer (minimum 0; Default `0`)
- `min` — integer (minimum 0; Default `0`)
- `max` — integer (minimum 0; Default `0`)
- `accountId` — null | integer (minimum 1)

## `prepare-automation-activation` · RI

**Prepare automation activation**

Validates the current automation and returns its activation dialog link; it does not start, schedule or publish. The user reviews the current state and confirms activation there; the link is not bound to a saved snapshot.

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `accountId` — null | integer (minimum 1)

## `stop-automation` · DO

**Stop automation**

Requests an automation stop; pass confirm=true only after the user explicitly asked to stop it. Requires the current revision. Already dispatched email and external side effects cannot be recalled.

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `confirm` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `move-automation-contacts` · DO

**Move automation contacts**

Previews moving eligible contacts from source actions to a target action; confirm=true queues the move; pass it only after the user has seen the sources, target and effects and explicitly requested it. A queued response is not completion and has no completion tracker; counts may change before processing.

Parameter:

- `automationId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `sourceActionIds`* — array<integer> (minItems 1; maxItems 100)
- `targetActionId`* — integer (minimum 1)
- `confirm` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `get-contact-automation-status` · RI

**Get Contact Marketing Campaign Status**

Reads a contact's current automation positions by campaign and reference, including action, state, dueAt and skippable status (only skippable waits can be ended with move-contact-past-automation-wait). state is scheduled, processing, waiting-for-condition, waiting-for-time-condition, waiting-for-restart, enriching, generating-email, open-end (stays at the end of a branch) or paused (automation paused). dueAt: when a scheduled action runs, when a time condition is checked next, when a paused action was due (past = runs on activation), when the open end was reached; else empty. Finished or exited automations are omitted. Reads only.

Parameter:

- `contactId`* — integer (minimum 1): Numeric contact ID returned by search-contacts
- `automationId` — null | integer (minimum 1): Only this automation; omit for every automation the contact is in
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account of the access token

## `move-contact-past-automation-wait` · DO

**Move Contact Past Marketing Campaign Wait**

Moves a contact past a skippable automation wait early. A scheduled action runs now or a timed condition is treated as met; following emails, SMS and tags may reach the contact early, without undo. Without confirm it previews, listing in immediateActions what the contact gets at once up to stopsAt; confirm only after the user agreed to this contact and automation. Requires administrator permission.

Parameter:

- `contactId`* — integer (minimum 1): Numeric contact ID returned by search-contacts
- `automationId`* — integer (minimum 1): Automation the contact waits in, from get-contact-automation-status
- `referenceId` — integer (minimum 0; Default `0`): Reference of that position, from get-contact-automation-status; 0 for the contact-wide reference
- `confirm` — boolean (Default `false`): false returns what would happen without writing; true ends the wait
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account of the access token

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
  - `type`* — string (einer von `tag`, `custom-field`, `email`, `outbound`)
  - `incomingId`* — string (minLength 1; maxLength 100)
  - `useExistingId` — string (minLength 1; maxLength 100)
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
- `settings` — object (Default `[]`)
  - `metaLabels` — array<string>
  - `gmailPreview` — string (maxLength 1000)
  - `crmTemplate` — integer (einer von `0`, `1`)
  - `invoiceTemplate` — integer (einer von `0`, `1`)
  - `firstAsTransactional` — integer (einer von `0`, `1`)
  - `aiContext` — object
    - `id` — string
    - `name` — string
    - `userPrompt` — string (maxLength 50000)
    - `fieldIds` — array<string>
    - `tagIds` — array<integer>
  - `aiSubject` — object
    - `id` — string
    - `name` — string
    - `userPrompt` — string (maxLength 50000)
    - `fieldIds` — array<string>
    - `tagIds` — array<integer>
  - `name` — string (maxLength 250)
  - `notes` — string (maxLength 10000)
  - `subject` — string (maxLength 1000)
  - `senderName` — string (maxLength 1000): From name. "dispatchProfile" takes it from the signature, or the account's name when the signature has none; empty uses the account's name.
  - `senderEmail` — string (maxLength 1000): From address. "dispatchProfile" takes it from the signature, or the account address when the signature has none; empty uses the account address.
  - `replyEmail` — string (maxLength 1000): Reply address. "dispatchProfile" takes it from the signature, or the account address when the signature has none; empty uses the account address.
  - `ccEmail` — string (maxLength 1000)
  - `bccEmail` — string (maxLength 1000)
  - `senderDomain` — string (maxLength 1000)
  - `signature` — integer (minimum 0): Signature ID; 0 picks the signature by the contact's tags.
  - `linkTracking` — integer (einer von `0`, `1`): 1 enables click tracking; 0 disables it.
  - `reportSpamEnabled` — integer (einer von `0`, `1`)
- `accountId` — null | integer (minimum 1)

## `update-automation-email-draft`

**Update automation-email draft**

Updates supplied automation email settings at the current revision. Refuses emails used by active or scheduled automations. Content and action assignment use separate tools; sends nothing.

Parameter:

- `emailId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `settings`* — object
  - `metaLabels` — array<string>
  - `gmailPreview` — string (maxLength 1000)
  - `crmTemplate` — integer (einer von `0`, `1`)
  - `invoiceTemplate` — integer (einer von `0`, `1`)
  - `firstAsTransactional` — integer (einer von `0`, `1`)
  - `aiContext` — object
    - `id` — string
    - `name` — string
    - `userPrompt` — string (maxLength 50000)
    - `fieldIds` — array<string>
    - `tagIds` — array<integer>
  - `aiSubject` — object
    - `id` — string
    - `name` — string
    - `userPrompt` — string (maxLength 50000)
    - `fieldIds` — array<string>
    - `tagIds` — array<integer>
  - `name` — string (maxLength 250)
  - `notes` — string (maxLength 10000)
  - `subject` — string (maxLength 1000)
  - `senderName` — string (maxLength 1000): From name. "dispatchProfile" takes it from the signature, or the account's name when the signature has none; empty uses the account's name.
  - `senderEmail` — string (maxLength 1000): From address. "dispatchProfile" takes it from the signature, or the account address when the signature has none; empty uses the account address.
  - `replyEmail` — string (maxLength 1000): Reply address. "dispatchProfile" takes it from the signature, or the account address when the signature has none; empty uses the account address.
  - `ccEmail` — string (maxLength 1000)
  - `bccEmail` — string (maxLength 1000)
  - `senderDomain` — string (maxLength 1000)
  - `signature` — integer (minimum 0): Signature ID; 0 picks the signature by the contact's tags.
  - `linkTracking` — integer (einer von `0`, `1`): 1 enables click tracking; 0 disables it.
  - `reportSpamEnabled` — integer (einer von `0`, `1`)
- `accountId` — null | integer (minimum 1)

## `delete-automation-email-draft` · D

**Delete automation-email draft**

Deletes an unreferenced automation email draft at the current revision without undo. Automation actions remain; confirm only for the email the user asked to delete.

Parameter:

- `emailId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `confirm`* — boolean
- `accountId` — null | integer (minimum 1)

## `copy-automation-email`

**Copy Marketing Campaign Email**

Copies a campaign (automation) email into an independent draft using its revision from get-automation-email. Active sources can be copied; the original is unchanged. Does not attach the copy to a campaign or send.

Parameter:

- `emailId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `name`* — string (minLength 1; maxLength 250)
- `accountId` — null | integer (minimum 1)

## `send-automation-email-test` · DO

**Send Test Marketing Campaign Email**

Sends a published campaign (automation) email as a test to one specified address. An address not yet in the account becomes a tagged test contact and may start automations; name the address and disclose that effect before calling. Pass confirm=true only after the user requested this test. Emails without published content are refused; unpublished edits are not sent. Notification emails use send-notification-email-test.

Parameter:

- `emailId`* — integer (minimum 1)
- `recipientEmail`* — string (minLength 3; maxLength 250)
- `confirm` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `preview-personalized-email` · DO

**Preview personalized automation email**

Previews a published campaign (automation) or notification email personalized for one existing contact; unpublished edits are not shown (preview-email-editor shows the draft). AI email previews can call the configured AI service and consume credits. Sends nothing. Newsletters use preview-personalized-newsletter, follow-ups preview-personalized-autoresponder-email.

Parameter:

- `emailId`* — integer (minimum 1)
- `subscriberId`* — integer (minimum 1)
- `referenceId` — integer (minimum 0; Default `0`)
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
- `settings` — object (Default `[]`)
  - `metaLabels` — array<string>
  - `gmailPreview` — string (maxLength 1000)
  - `crmTemplate` — integer (einer von `0`, `1`)
  - `invoiceTemplate` — integer (einer von `0`, `1`)
  - `firstAsTransactional` — integer (einer von `0`, `1`)
  - `aiContext` — object
    - `id` — string
    - `name` — string
    - `userPrompt` — string (maxLength 50000)
    - `fieldIds` — array<string>
    - `tagIds` — array<integer>
  - `aiSubject` — object
    - `id` — string
    - `name` — string
    - `userPrompt` — string (maxLength 50000)
    - `fieldIds` — array<string>
    - `tagIds` — array<integer>
  - `name` — string (maxLength 250)
  - `notes` — string (maxLength 10000)
  - `subject` — string (maxLength 1000)
  - `senderName` — string (maxLength 1000): From name. "dispatchProfile" takes it from the signature, or the account's name when the signature has none; empty uses the account's name.
  - `senderEmail` — string (maxLength 1000): From address. "dispatchProfile" takes it from the signature, or the account address when the signature has none; empty uses the account address.
  - `replyEmail` — string (maxLength 1000): Reply address. "dispatchProfile" takes it from the signature, or the account address when the signature has none; empty uses the account address.
  - `ccEmail` — string (maxLength 1000)
  - `bccEmail` — string (maxLength 1000)
  - `senderDomain` — string (maxLength 1000)
  - `signature` — integer (minimum 0): Signature ID; 0 picks the signature by the contact's tags.
  - `linkTracking` — integer (einer von `0`, `1`): 1 enables click tracking; 0 disables it.
  - `reportSpamEnabled` — integer (einer von `0`, `1`)
- `accountId` — null | integer (minimum 1)

## `update-notification-email-draft`

**Update notification-email draft**

Updates supplied notification email settings at the current revision. Refuses emails used by active or scheduled automations. Content and action assignment use separate tools; sends nothing.

Parameter:

- `emailId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `settings`* — object
  - `metaLabels` — array<string>
  - `gmailPreview` — string (maxLength 1000)
  - `crmTemplate` — integer (einer von `0`, `1`)
  - `invoiceTemplate` — integer (einer von `0`, `1`)
  - `firstAsTransactional` — integer (einer von `0`, `1`)
  - `aiContext` — object
    - `id` — string
    - `name` — string
    - `userPrompt` — string (maxLength 50000)
    - `fieldIds` — array<string>
    - `tagIds` — array<integer>
  - `aiSubject` — object
    - `id` — string
    - `name` — string
    - `userPrompt` — string (maxLength 50000)
    - `fieldIds` — array<string>
    - `tagIds` — array<integer>
  - `name` — string (maxLength 250)
  - `notes` — string (maxLength 10000)
  - `subject` — string (maxLength 1000)
  - `senderName` — string (maxLength 1000): From name. "dispatchProfile" takes it from the signature, or the account's name when the signature has none; empty uses the account's name.
  - `senderEmail` — string (maxLength 1000): From address. "dispatchProfile" takes it from the signature, or the account address when the signature has none; empty uses the account address.
  - `replyEmail` — string (maxLength 1000): Reply address. "dispatchProfile" takes it from the signature, or the account address when the signature has none; empty uses the account address.
  - `ccEmail` — string (maxLength 1000)
  - `bccEmail` — string (maxLength 1000)
  - `senderDomain` — string (maxLength 1000)
  - `signature` — integer (minimum 0): Signature ID; 0 picks the signature by the contact's tags.
  - `linkTracking` — integer (einer von `0`, `1`): 1 enables click tracking; 0 disables it.
  - `reportSpamEnabled` — integer (einer von `0`, `1`)
- `accountId` — null | integer (minimum 1)

## `delete-notification-email-draft` · D

**Delete notification-email draft**

Deletes an unreferenced notification email draft at the current revision without undo. Automation actions remain; confirm only for the email the user asked to delete.

Parameter:

- `emailId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `confirm`* — boolean
- `accountId` — null | integer (minimum 1)

## `copy-notification-email`

**Copy Notification Email**

Copies a notification email into an independent draft using its revision from get-notification-email. Active sources can be copied; the original is unchanged. Does not attach the copy to a campaign or send.

Parameter:

- `emailId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `name`* — string (minLength 1; maxLength 250)
- `accountId` — null | integer (minimum 1)

## `send-notification-email-test` · DO

**Send Test Notification Email**

Sends a published notification email as a test to one specified address. An address not yet in the account becomes a tagged test contact and may start automations; name the address and disclose that effect before calling. Pass confirm=true only after the user requested this test. Emails without published content are refused; unpublished edits are not sent. Campaign emails use send-automation-email-test.

Parameter:

- `emailId`* — integer (minimum 1)
- `recipientEmail`* — string (minLength 3; maxLength 250)
- `confirm` — boolean (Default `false`)
- `accountId` — null | integer (minimum 1)

## `send-email-for-gmail-placement-preview` · DO

**Request Gmail placement preview**

Sends a published campaign or notification email to the configured Gmail preview address and starts the inbox placement check; pass confirm=true only after the user explicitly requested it. Returns pending or reported state; get-email-gmail-placement-preview-result reads later results. Does not change campaign scheduling.

Parameter:

- `emailId`* — integer (minimum 1)
- `confirm` — boolean (Default `false`)
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
- `settings` — object (Default `[]`)
  - `name` — string (minLength 1; maxLength 250)
  - `notes` — string (maxLength 1000)
  - `metaLabels` — array<string>
  - `smsSenderName` — string (maxLength 250)
  - `senderSms` — string (maxLength 32): Use 0 with smsSenderName for an alphanumeric sender; otherwise use the configured sender number.
  - `smsProvider` — string (einer von ``, `nexmo`, `twilio`)
  - `linkTracking` — integer (einer von `0`, `1`): 1 enables click tracking; 0 disables it.
- `accountId` — null | integer (minimum 1)

## `update-automation-sms-draft`

**Update automation-sms draft**

Updates supplied automation SMS settings at the current revision. Settings save only while the SMS has a provider and sender, as in the app. Refuses SMS used by active or scheduled automations. Content and action assignment use separate tools; sends nothing.

Parameter:

- `smsId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `settings`* — object
  - `name` — string (minLength 1; maxLength 250)
  - `notes` — string (maxLength 1000)
  - `metaLabels` — array<string>
  - `smsSenderName` — string (maxLength 250)
  - `senderSms` — string (maxLength 32): Use 0 with smsSenderName for an alphanumeric sender; otherwise use the configured sender number.
  - `smsProvider` — string (einer von ``, `nexmo`, `twilio`)
  - `linkTracking` — integer (einer von `0`, `1`): 1 enables click tracking; 0 disables it.
- `accountId` — null | integer (minimum 1)

## `delete-automation-sms-draft` · D

**Delete automation-sms draft**

Deletes an unreferenced automation SMS draft at the current revision without undo. Automation actions remain; confirm only for the SMS the user asked to delete.

Parameter:

- `smsId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `confirm`* — boolean
- `accountId` — null | integer (minimum 1)

## `replace-automation-sms-content`

**Replace Marketing Campaign SMS Content**

Replaces automation SMS plaintext at its current draft revision. Empty text is allowed; active or scheduled uses are refused. Does not send. Notification SMS use replace-notification-sms-content.

Parameter:

- `smsId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `plain`* — string (maxLength 5000)
- `accountId` — null | integer (minimum 1)

## `copy-automation-sms`

**Copy Marketing Campaign SMS**

Copies an automation SMS into an independent draft with its own new smart tags. Active sources are allowed; the original stays. Does not attach or send the copy. Creation is not automatically retryable.

Parameter:

- `smsId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `name`* — string (minLength 1; maxLength 250)
- `accountId` — null | integer (minimum 1)

## `send-automation-sms-test` · DO

**Send Test Marketing Campaign SMS**

Sends a saved automation SMS test to the specified phone number via its provider, charging SMS credits without recall. Personalization uses a matching or random account contact. Pass confirm=true only when the user asked for a test to exactly this number; do not automatically retry.

Parameter:

- `smsId`* — integer (minimum 1)
- `recipientPhone`* — string (Muster `^\+[1-9][0-9]{5,14}$`)
- `confirm`* — boolean
- `accountId` — null | integer (minimum 1)

## `check-sms-readiness` · RI

**Check SMS Readiness**

Checks a saved automation or notification SMS for content, sender and provider readiness. Returns blockers or unavailable checks. Inbound shared-number keywords are for subscriptions, not outbound SMS. Does not test email domains, send SMS, spend credits or change content.

Parameter:

- `smsId`* — integer (minimum 1): ID of the saved SMS, not the automation action ID
- `kind`* — string (einer von `automation`, `notification`): Whether this is an automation or notification SMS
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account of the access token

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
- `settings` — object (Default `[]`)
  - `name` — string (minLength 1; maxLength 250)
  - `notes` — string (maxLength 1000)
  - `metaLabels` — array<string>
  - `smsSenderName` — string (maxLength 250)
  - `senderSms` — string (maxLength 32): Use 0 with smsSenderName for an alphanumeric sender; otherwise use the configured sender number.
  - `smsProvider` — string (einer von ``, `nexmo`, `twilio`)
  - `linkTracking` — integer (einer von `0`, `1`): 1 enables click tracking; 0 disables it.
- `accountId` — null | integer (minimum 1)

## `update-notification-sms-draft`

**Update notification-sms draft**

Updates supplied notification SMS settings at the current revision. Settings save only while the SMS has a provider and sender, as in the app. Refuses SMS used by active or scheduled automations. Content and action assignment use separate tools; sends nothing.

Parameter:

- `smsId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `settings`* — object
  - `name` — string (minLength 1; maxLength 250)
  - `notes` — string (maxLength 1000)
  - `metaLabels` — array<string>
  - `smsSenderName` — string (maxLength 250)
  - `senderSms` — string (maxLength 32): Use 0 with smsSenderName for an alphanumeric sender; otherwise use the configured sender number.
  - `smsProvider` — string (einer von ``, `nexmo`, `twilio`)
  - `linkTracking` — integer (einer von `0`, `1`): 1 enables click tracking; 0 disables it.
- `accountId` — null | integer (minimum 1)

## `delete-notification-sms-draft` · D

**Delete notification-sms draft**

Deletes an unreferenced notification SMS draft at the current revision without undo. Automation actions remain; confirm only for the SMS the user asked to delete.

Parameter:

- `smsId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `confirm`* — boolean
- `accountId` — null | integer (minimum 1)

## `copy-notification-sms`

**Copy Notification SMS**

Copies a notification SMS into an independent draft with its own new smart tags. Active sources are allowed; the original stays. Does not attach or send the copy. Creation is not automatically retryable.

Parameter:

- `smsId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `name`* — string (minLength 1; maxLength 250)
- `accountId` — null | integer (minimum 1)

## `replace-notification-sms-content`

**Replace Notification SMS Content**

Replaces notification SMS plaintext at its current draft revision. Empty text is allowed; active or scheduled uses are refused. Does not send. Automation SMS use replace-automation-sms-content.

Parameter:

- `smsId`* — integer (minimum 1)
- `revision`* — string (Muster `^[a-f0-9]{64}$`)
- `plain`* — string (maxLength 5000)
- `accountId` — null | integer (minimum 1)

## `send-notification-sms-test` · DO

**Send Test Notification SMS**

Sends a saved notification SMS test to the specified phone number via its provider, charging SMS credits without recall. Personalization uses a matching or random account contact. Pass confirm=true only when the user asked for a test to exactly this number; do not automatically retry.

Parameter:

- `smsId`* — integer (minimum 1)
- `recipientPhone`* — string (Muster `^\+[1-9][0-9]{5,14}$`)
- `confirm`* — boolean
- `accountId` — null | integer (minimum 1)
