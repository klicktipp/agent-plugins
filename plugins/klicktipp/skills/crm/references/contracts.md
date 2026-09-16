# Die veröffentlichten Verträge — Kontakte, Tags, Felder, Opt-in

Wort für Wort das, was der Server in `tools/list` für die 24 Werkzeuge dieses Skills
ausliefert: Beschreibung, Annotationen, jeder Parameter mit Typ, Grenzen und Beschreibung. Ein `*`
markiert Pflichtparameter. `R` liest nur · `D` löscht oder ersetzt ohne Undo · `O` erreicht etwas
außerhalb des Kontos · `I` ein zweiter gleicher Aufruf ändert nichts mehr.

Generiert aus `build/tools-list.json` (Stand 2026-09-16) mit `build/contracts.py` — nicht von Hand
ändern, sondern den Dump erneuern und neu erzeugen. Wofür ein Werkzeug da ist, was es nicht tut
und woran man sich stößt, steht in [tools.md](tools.md).

## `search-opt-in-processes` · RI

**Search opt-in processes**

Searches the active KlickTipp opt-in processes (also called subscription processes or subscriber lists) of an account, sorted by name, with ID, name, opt-in mode and the flags that tell them apart. Deleted processes are left out. Lists the account the access token belongs to, or one of its subaccounts when an account ID is given. Use get-opt-in-process for the full configuration of a single entry.

Parameter:

- `query` — null | string (maxLength 250): Case-insensitive name fragment to search for; omit to return every active process
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `get-opt-in-process` · RI

**Get opt-in process**

Returns the configuration of a single KlickTipp opt-in process (also called subscription process or subscriber list), looked up by its numeric ID: name, opt-in mode, confirmation email ID, redirect URLs, pending subscriber deletion, labels and notes. Reads from the account the access token belongs to, or from one of its subaccounts when an account ID is given.

Parameter:

- `optInProcessId`* — integer (minimum 1): ID of the opt-in process, as shown in the KlickTipp app URL
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-opt-in-process` · I

**Update opt-in process**

Changes the settings of one KlickTipp opt-in process (also called subscription process or subscriber list): name, opt-in mode, redirect URLs and their query parameters, confirmation resend, change-email role, deletion of unconfirmed contacts, labels and notes. Only the arguments that are given are written, the rest keeps its current value. Settings take effect for contacts subscribing from now on; contacts already in the process are not touched and nothing is sent. Single opt-in subscribes later contacts without confirming, which is not permitted everywhere - ask before setting it. The confirmation email itself is written with the email tools. A redirect page can carry the contact id, email or subscriber key: name a parameter and it is appended under that name, leave it empty and it is not -- but only together with that page`s URL in the same call. Read them with get-opt-in-process.

Parameter:

- `optInProcessId`* — integer (minimum 1): ID of the opt-in process to change
- `name` — null | string (minLength 1; maxLength 250): New name; omit to keep the current one
- `notes` — null | string (maxLength 2000): Internal note, not visible to contacts; empty string clears it
- `optInMode` — null | string (einer von `double`, `single`): "double" for a confirmation email, "single" without one
- `pendingRedirectUrl` — null | string (maxLength 2000): URL a contact reaches after subscribing, before confirming; empty string restores the KlickTipp page
- `confirmedRedirectUrl` — null | string (maxLength 2000): URL a contact reaches after confirming; empty string restores the KlickTipp page
- `resendConfirmationEmail` — null | boolean: Whether an already pending contact receives the confirmation email again on a repeated subscription
- `useForChangeEmail` — null | boolean: Whether this process handles email address changes; true takes that role away from the process that holds it
- `deletePendingSubscribersAfterDays` — null | integer (einer von `0`, `1`, `3`, `7`, `14`): Days after which unconfirmed contacts are deleted, one of 0, 1, 3, 7, 14; 0 keeps them
- `metaLabels` — array<string> (maxItems 50): Complete list of labels; replaces the existing labels, empty array removes them all
- `pendingPageParameters` — object: Query parameters appended to pendingRedirectUrl, by the name each is appended under; needs pendingRedirectUrl in the same call
  - `subscriberParameterName` — string (maxLength 100)
  - `emailParameterName` — string (maxLength 100)
  - `listParameterName` — string (maxLength 100)
  - `subscriberKeyParameterName` — string (maxLength 100)
- `confirmedPageParameters` — object: Query parameters appended to confirmedRedirectUrl, by the name each is appended under; needs confirmedRedirectUrl in the same call
  - `subscriberParameterName` — string (maxLength 100)
  - `emailParameterName` — string (maxLength 100)
  - `listParameterName` — string (maxLength 100)
  - `subscriberKeyParameterName` — string (maxLength 100)
  - `referralLinkParameterName` — string (maxLength 100)
  - `referralLinkId` — integer (minimum 0)
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `delete-opt-in-process` · D

**Delete opt-in process**

Deletes one KlickTipp opt-in process (also called subscription process or subscriber list) together with its confirmation email. The contacts that subscribed through it keep their subscription and are not deleted. Refused for the default process of the account, and for a process that forms, campaigns or other entities still refer to -- the refusal names what refers to it, so those can be pointed elsewhere first. This cannot be undone, so only call it for a process the user has explicitly asked to delete, named by the ID that get-opt-in-process reports.

Parameter:

- `optInProcessId`* — integer (minimum 1): ID of the opt-in process to delete
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `get-opt-in-confirmation-email` · RI

**Get opt-in confirmation email**

Reads the confirmation email a double opt-in process sends: its subject, the sender name and address, reply-to, CC and BCC, and the sender domain. THE BODY IS NOT HERE and cannot be read or written by this tool set: a confirmation email is not a drag-and-drop document, so the email and block tools do not accept it -- the answer carries bodyIsEditable false and an editUrl into the KlickTipp editor, which is where its text is written. Single opt-in processes still have this email stored; it is simply not sent. Change the settings with update-opt-in-confirmation-email.

Parameter:

- `optInProcessId`* — integer (minimum 1): ID of the opt-in process whose confirmation email is read
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-opt-in-confirmation-email` · I

**Update opt-in confirmation email**

Changes the settings of the confirmation email a double opt-in process sends: subject, sender name and address, reply-to, CC and BCC. Only the arguments that are given are written, the rest keeps its current value. THE BODY CANNOT BE WRITTEN HERE or by the email tools -- a confirmation email is not a drag-and-drop document; its text is written in the KlickTipp editor, and get-opt-in-confirmation-email returns the link. This email is the legal record of a contact`s consent in many countries: change its sender or subject only when the user asked for it, and say what was changed.

Parameter:

- `optInProcessId`* — integer (minimum 1): ID of the opt-in process whose confirmation email is changed
- `subject` — null | string (minLength 1; maxLength 250): Subject line of the confirmation email
- `senderName` — null | string (minLength 1; maxLength 250): Name the email comes from
- `senderEmail` — null | string (maxLength 250): Address the email comes from; must be one the account may send from
- `replyToEmail` — null | string (maxLength 250): Address a reply goes to; empty string removes it
- `ccEmail` — null | string (maxLength 250): Address that receives a copy; empty string removes it
- `bccEmail` — null | string (maxLength 250): Address that receives a blind copy; empty string removes it
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `subscribe` · DO

**Subscribe contact**

Subscribes exactly one email or SMS channel of a KlickTipp contact through an opt-in process and creates or reuses the contact and requested reference. THIS CHANGES A REAL RECIPIENT, MAY SEND A CONFIRMATION MESSAGE AND MAY START AUTOMATIONS. Pass either email or phone number, never both, and only call the tool after the user approved those effects. Assigning the optional tag may start further automations or outbound events. Other channels and references are not changed.

Parameter:

- `optInProcessId`* — integer (minimum 1): ID of the opt-in process to run
- `approval`* — string (einer von `subscribe-contact`): Exactly "subscribe-contact": acknowledges a confirmation message, automations and a changed real recipient
- `email` — null | string (maxLength 250): Email channel to subscribe; mutually exclusive with phoneNumber
- `phoneNumber` — null | string (maxLength 50): SMS channel to subscribe in E.164 format; mutually exclusive with email
- `referenceId` — integer (minimum 0; Default `0`): Subscription reference context to create or reuse; a non-zero ID must exist in the account
- `tagId` — null | integer (minimum 1): Tag to additionally assign to the contact after a successful subscription
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `unsubscribe` · DOI

**Unsubscribe contact**

Unsubscribes exactly one email or SMS channel of a KlickTipp contact. THIS CHANGES A REAL RECIPIENT: future subscribed-audience messages on that channel stop, and automations may run. Pass either email or phone number, never both, and only call the tool after the user approved those effects. Other channels of the same contact and all subscription references remain untouched.

Parameter:

- `approval`* — string (einer von `unsubscribe-contact`): Exactly "unsubscribe-contact": acknowledges a changed real recipient and automations
- `email` — null | string (maxLength 250): Email channel to unsubscribe; mutually exclusive with phoneNumber
- `phoneNumber` — null | string (maxLength 50): SMS channel to unsubscribe in E.164 format; mutually exclusive with email
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `search-contacts` · RI

**Search contacts**

Returns a cursor-paginated, email-sorted list of contacts in one KlickTipp account. The lean results contain the contact ID, email subscription status and edit link, but intentionally omit complete contact fields and reference data. Filter by an email fragment, subscription status or an existing writable manual tag. Pass the returned nextCursor unchanged, with the same filters, to fetch the next page. Use get-contact for the full permitted detail view.

Parameter:

- `query` — null | string (maxLength 250): Case-insensitive email-address fragment; omit to match every email contact
- `status` — null | string (einer von `pending`, `optin`, `subscribed`, `unsubscribed`): Email subscription status to filter by; omit for every status
- `manualTagId` — null | integer (minimum 1): ID of an existing manual tag the returned contacts must have
- `cursor` — null | string (maxLength 500): Opaque nextCursor value of the previous result page; omit for the first page
- `pageSize` — integer (minimum 1; maximum 100; Default `25`): Maximum contacts on the page, from 1 through 100
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `get-contact` · RI

**Get contact**

Returns the permitted detail view of one contact in a KlickTipp account: email address, email subscription status, contact fields for the requested reference, writable manual tag IDs and the edit link. Every field carries its data type, and the three that are stored as numbers are answered exactly as KlickTipp shows them on screen: a date as 16.09.2026, a moment as 16.09.2026 14:30, a time of day as 14:30, in the time zone the account is configured for. It does not expose complete channel or subscription-reference records.

Parameter:

- `contactId`* — integer (minimum 1): Numeric contact ID returned by search-contacts
- `referenceId` — integer (minimum 0; Default `0`): Reference whose multi-value fields and manual tags to read; 0 for contact-wide values
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `enrich-contact` · DO

**Enrich contact**

Updates explicitly listed contact-field values for one contact. It cannot change email or SMS addresses, opt-in state, subscriptions, lists or other channel data. Every custom-field ID and the contact itself must belong to the selected account; global contact fields remain available. Date, time and datetime fields take the forms get-contact answers with -- 16.09.2026, 16.09.2026 14:30, 14:30 -- and ISO 8601 as well, for a caller that computed a date rather than read one. Anything else is refused rather than stored as a date it was not meant to be, and the refusal names the form that works. An empty value clears the field.

Parameter:

- `contactId`* — integer (minimum 1): Numeric contact ID returned by search-contacts
- `fields`* — array<object> (minItems 1; maxItems 50): Contact field updates; fieldId must be a global field key or an account-owned numeric custom-field ID, a date, time or datetime value takes the form get-contact answers with, and referenceId defaults to 0
  - `fieldId`* — string (minLength 1; maxLength 15)
  - `value`* — string (maxLength 65535)
  - `referenceId` — integer (minimum 0; Default `0`)
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `assign-manual-tag` · O

**Assign manual tag**

Assigns one existing writable manual tag to one contact. This may immediately start or alter campaigns, autoresponders, outbound events and automations. The caller must explicitly approve those effects. Unknown, foreign or non-manual tags are rejected and never created.

Parameter:

- `contactId`* — integer (minimum 1): Numeric contact ID returned by search-contacts
- `manualTagId`* — integer (minimum 1): Existing writable manual tag ID; unknown tags are rejected and never created
- `approval`* — string (einer von `I_ACCEPT_AUTOMATION_EFFECTS`): Exactly I_ACCEPT_AUTOMATION_EFFECTS: tagging may start campaigns and automations
- `referenceId` — integer (minimum 0; Default `0`): Reference for a multi-value manual tag; use 0 for contact-wide tags
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `remove-manual-tag` · DOI

**Remove manual tag**

Removes one existing writable manual tag from one contact. This may immediately alter campaigns, autoresponder queues and automations, so the caller must explicitly approve those effects. Removing a tag does not unsubscribe the contact and changes no subscription or channel state.

Parameter:

- `contactId`* — integer (minimum 1): Numeric contact ID returned by search-contacts
- `manualTagId`* — integer (minimum 1): Existing writable manual tag ID to remove
- `approval`* — string (einer von `I_ACCEPT_AUTOMATION_EFFECTS`): Exactly I_ACCEPT_AUTOMATION_EFFECTS: removal may alter campaigns and automations
- `referenceId` — integer (minimum 0; Default `0`): Reference for a multi-value manual tag; use 0 for contact-wide tags
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `get-subscription-redirect-url` · RI

**Get subscription redirect URL**

Returns the URL a subscriber is redirected to by an opt-in process, looked up by email address: the pending page while the confirmation is still open, the thank-you page once the subscriber has confirmed. The URL carries the parameters configured for that page (subscriber ID, email, list, subscriber key, referral link) and therefore identifies the subscriber. Processes without a custom page fall back to the KlickTipp-hosted pending or thank-you page.

Parameter:

- `email`* — string: Email address of the subscriber
- `optInProcessId` — null | integer (minimum 1): Opt-in process to resolve for; omit for the one the subscriber signed up through
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `search-custom-fields` · RI

**Search custom fields**

Lists the custom field definitions of a KlickTipp account with ID, name, data type, the placeholder that renders the value of the receiving contact in newsletter content, and the group the account sorted the field into. Fields the account created itself come first, newest first, followed by the global fields every KlickTipp account has, such as first name or city; the global ones are marked with isGlobal and cannot be changed or deleted. Can be narrowed by a text the name has to contain, by data type, and to the fields the write tools may touch. This lists definitions -- what a contact has stored in a field is read through the contact tools.

Parameter:

- `query` — null | string (maxLength 250): Text the name of a field has to contain; omit to list them all
- `types` — array | null: Only fields of these data types, for example ["field-date", "field-datetime"]; omit for every type
- `onlyWritable` — null | boolean: Only the account's own fields, the ones the write tools may touch; omit to include the global fields
- `limit` — null | integer (minimum 1; maximum 200): How many fields to return at most, 1 to 200, 50 by default
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `get-custom-field` · RI

**Get custom field**

Returns one custom field definition of a KlickTipp account: its name and data type, the placeholder that renders the value of the receiving contact in newsletter content, the key the public API addresses it with, what the account wrote about what the field holds, its internal note, group and labels, the field its values are copied to, and whether a contact can hold more than one value in it. This returns the definition -- what a contact has stored in the field is read through the contact tools.

Parameter:

- `customFieldId`* — string (minLength 1; maxLength 100; Muster `^[A-Za-z0-9_]+$`): Field ID: a number for the account's own field, a name such as "FirstName" for a global one
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `create-custom-field`

**Create custom field**

Creates a custom field definition in KlickTipp and returns its ID and the placeholder that renders it in newsletter content. Creating a field stores no value and changes no contact. Fields are never created as a side effect elsewhere, so a field a contact should have a value in has to be created here first. The data type is picked once and for good: it cannot be changed afterwards, so pick the one that matches what will be stored -- a date field for a date, a number field for an amount. The name has to be unique within the account. Give a description: it is what tells a later reader what belongs in the field.

Parameter:

- `name`* — string (minLength 1; maxLength 250): Name of the field, which has to be unique within the account
- `type`* — string (einer von `field-single`, `field-paragraph`, `field-email`, `field-number`, `field-url`, `field-date`, `field-time`, `field-datetime`, `field-html`, `field-decimal`): Data type of the field, which decides what can be stored in it and cannot be changed afterwards
- `description` — null | string (maxLength 2000): What the field holds, so a person or a model reading it later knows what to write into it
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-custom-field` · I

**Update custom field**

Changes the name, the description, the group or the labels of a custom field in KlickTipp. The data type of a field cannot be changed here and is refused: an existing field keeps the type it was created with, because the values contacts already hold in it were stored in that type. Whether a contact can hold more than one value stays as it is as well. Only fields the account created itself can be changed; the global fields every KlickTipp account has are refused. Renaming a field does not move the values contacts hold in it and does not break the content and automations that read it, since those refer to its ID -- but the result lists what uses the field, because a rename shows up wherever the name is read.

Parameter:

- `customFieldId`* — string (minLength 1; maxLength 100; Muster `^[A-Za-z0-9_]+$`): ID of the field to change
- `name` — null | string (maxLength 250): New name of the field, which has to stay unique within the account; omit to keep the current one
- `description` — null | string (maxLength 2000): New description of what the field holds; omit to keep the current one
- `category` — null | string (maxLength 250): Group in the app; empty string sorts into none; omit to keep
- `metaLabels` — array | null (maxItems 50): New set of labels of the field, which replaces the current one; omit to keep the current labels
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `delete-custom-field` · DI

**Delete custom field**

Deletes a custom field definition in KlickTipp and with it every value the contacts of the account hold in that field. This destroys contact data and cannot be undone, so only call it for a field the user has explicitly asked to delete. Only fields the account created itself can be deleted; the global fields every KlickTipp account has are refused. A field that opt-in forms, automations or other entities still use is refused as well, and the refusal names them, so nothing that reads the field breaks silently. The placeholder of a deleted field renders an empty value wherever content still carries it.

Parameter:

- `customFieldId`* — string (minLength 1; maxLength 100; Muster `^[A-Za-z0-9_]+$`): ID of the field to delete
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `search-tags` · RI

**Search tags**

Lists the tags of a KlickTipp account with ID, name, type, whether they can be written and whether a contact can carry them more than once. Tags are either manual -- created and assigned deliberately -- or put on contacts by KlickTipp itself when something happens, for example a newsletter being sent, opened or clicked; the type says which. Can be narrowed by a text the name has to contain, by type, to the writable ones, by whether a contact can carry a tag once per subscription or only once overall, and to tags with a system role such as the test contact marker. The description of a tag is not part of the list -- use get-tag for that.

Parameter:

- `query` — null | string (maxLength 250): Text the name of a tag has to contain; omit to list them all
- `type` — null | string (maxLength 100): Only tags of this type, e.g. "tag" (manual), "campaign-sent", "email-opened"; omit for every type
- `onlyWritable` — null | boolean: Only manual tags the write tools may touch; omit to include the ones KlickTipp sets itself
- `multiValue` — null | boolean: true: tags a contact can carry once per subscription; false: once overall; omit for both
- `systemRole` — null | string (einer von `test-contact`): Only tags with this system role; "test-contact" marks contacts that receive test emails
- `limit` — null | integer (minimum 1; maximum 200): How many tags to return at most, 1 to 200, 50 by default
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `get-tag` · RI

**Get tag**

Returns one tag of a KlickTipp account with the context needed to tell what it means: its type, whether it can be written, what it stands for, the entity behind it for tags KlickTipp puts on contacts itself, the internal note and labels of the account, how many contacts carry it, and which tags a contact is subscribed to or unsubscribed from when this tag is assigned. Also says whether this is the tag the app marks test contacts with.

Parameter:

- `tagId`* — integer (minimum 1): ID of the tag, as shown in the KlickTipp app URL
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `create-manual-tag`

**Create manual tag**

Creates a manual tag in KlickTipp, one that is assigned deliberately rather than by KlickTipp itself. Creating a tag assigns it to nobody and changes no contact. Tags are never created as a side effect elsewhere, so a tag a contact should carry has to be created here first. The name has to be unique within the account. Give a description: it is what tells a later reader what the tag means.

Parameter:

- `name`* — string (minLength 1; maxLength 250): Name of the tag, which has to be unique within the account and cannot be a number alone
- `description` — null | string (maxLength 2000): What the tag stands for, so a person or a model reading it later knows when to assign it
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-manual-tag` · I

**Update manual tag**

Changes the name or the description of a manual tag in KlickTipp. Only manual tags can be changed: a tag KlickTipp puts on contacts itself takes its name from the newsletter, automation or form behind it and is refused. Renaming a tag does not change who carries it and does not break the campaigns and automations that use it, since those refer to its ID -- but the result lists them, because a rename shows up wherever the name is read. Everything else about the tag, including its auto-subscribe configuration and whether it is single value, stays as it is.

Parameter:

- `tagId`* — integer (minimum 1): ID of the manual tag to change
- `name` — null | string (maxLength 250): New name of the tag, which has to stay unique within the account; omit to keep the current one
- `description` — null | string (maxLength 2000): New description of what the tag stands for; omit to keep the current one
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `delete-manual-tag` · DOI

**Delete manual tag**

Deletes a manual tag in KlickTipp and takes it off every contact that carries it. Only manual tags can be deleted; a tag KlickTipp puts on contacts itself is refused. A tag that campaigns, automations or other entities still use is refused as well, and the refusal names them, so nothing that depends on the tag breaks silently. This cannot be undone, so only call it for a tag the user has explicitly asked to delete.

Parameter:

- `tagId`* — integer (minimum 1): ID of the manual tag to delete
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in
