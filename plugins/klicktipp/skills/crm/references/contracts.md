# Die veröffentlichten Verträge — Kontakte, Tags, Felder, Opt-in

Wort für Wort das, was der Server in `tools/list` für die 30 Werkzeuge dieses Skills
ausliefert: Beschreibung, Annotationen, jeder Parameter mit Typ, Grenzen und Beschreibung. Ein `*`
markiert Pflichtparameter. `R` liest nur · `D` löscht oder ersetzt ohne Undo · `O` erreicht etwas
außerhalb des Kontos · `I` ein zweiter gleicher Aufruf ändert nichts mehr.

Diese Datei spiegelt den Server, sie interpretiert ihn nicht: ändert sich eine
Werkzeugbeschreibung, wird sie hier wörtlich nachgezogen. Wofür ein Werkzeug da ist, was es nicht
tut und woran man sich stößt, steht in [tools.md](tools.md).

## Inhalt

`search-opt-in-processes` · `get-opt-in-process` · `create-opt-in-process` · `update-opt-in-process` ·
`delete-opt-in-process` · `get-opt-in-confirmation-email` · `update-opt-in-confirmation-email` ·
`get-opt-in-confirmation-email-content` · `update-opt-in-confirmation-email-content` ·
`preview-opt-in-confirmation-email` · `send-opt-in-confirmation-email-test` · `search-contacts` ·
`get-contact` · `upsert-subscribed-contact` · `update-contact-values` · `tag-contact` ·
`untag-contact` · `subscribe-contact-via-opt-in-process` · `unsubscribe-contact` · `get-opt-in-process-redirect-url` ·
`search-custom-fields` · `get-custom-field` · `create-custom-field` · `update-custom-field` ·
`delete-custom-field` · `search-tags` · `get-tag` · `create-manual-tag` · `update-manual-tag` ·
`delete-manual-tag`

## `search-opt-in-processes` · RI

**Search opt-in processes**

Searches the active KlickTipp opt-in processes (also called subscription processes or subscriber lists) of an account, sorted by name, with ID, name, opt-in mode and the flags that tell them apart. Deleted processes are left out. Lists the account the access token belongs to, or one of its subaccounts when an account ID is given. The full configuration of a single entry is get-opt-in-process.

Parameter:

- `query` — null | string (maxLength 250): Case-insensitive name fragment to search for; omit to return every active process
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `get-opt-in-process` · RI

**Get opt-in process**

Returns the configuration of a single KlickTipp opt-in process (also called subscription process or subscriber list), looked up by its numeric ID: name, opt-in mode, confirmation email ID, redirect URLs with their query and UTM parameters, pending subscriber deletion, labels and notes. Reads from the account the access token belongs to, or from one of its subaccounts when an account ID is given.

Parameter:

- `optInProcessId`* — integer (minimum 1): ID of the opt-in process, as shown in the KlickTipp app URL
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `create-opt-in-process`

**Create opt-in process**

Creates a KlickTipp opt-in process (also called subscription process or subscriber list) and the confirmation email that belongs to it, which the platform always creates with it. Takes the same settings as update-opt-in-process except the change-email role. copyFromOptInProcessId copies an existing process including the text of its confirmation email, and the arguments given here still win over the copy. The new process is empty and sends nothing until a form, an automation or an API call subscribes someone to it. Single opt-in subscribes contacts without confirming, which is not permitted everywhere - ask before setting it. The answer carries the new ID and confirmationEmailId; the confirmation email tools write that email.

Parameter:

- `name`* — string (minLength 1; maxLength 250): Name of the new process; must be free within the account
- `notes` — null | string (maxLength 2000): Internal note, not visible to contacts
- `optInMode` — null | string (einer von `double`, `single`): "double" for a confirmation email, "single" without one; defaults to double
- `pendingRedirectUrl` — null | string (maxLength 2000): URL a contact reaches after subscribing, before confirming; omit for the KlickTipp page
- `confirmedRedirectUrl` — null | string (maxLength 2000): URL a contact reaches after confirming; omit for the KlickTipp page
- `resendConfirmationEmail` — null | boolean: Whether an already pending contact receives the confirmation email again on a repeated subscription
- `deletePendingSubscribersAfterDays` — null | integer (einer von `0`, `1`, `3`, `7`, `14`): Days after which unconfirmed contacts are deleted, one of 0, 1, 3, 7, 14; 0 keeps them
- `metaLabels` — array | null (maxItems 50): Labels of the new process
- `pendingPageParameters` — object: Query parameters appended to pendingRedirectUrl, by the name each is appended under; needs pendingRedirectUrl in the same call
- `confirmedPageParameters` — object: Query parameters appended to confirmedRedirectUrl, by the name each is appended under; needs confirmedRedirectUrl in the same call
- `pendingUtmParameters` — object: Campaign tracking values appended to pendingRedirectUrl, by query name; the value, not the name; needs pendingRedirectUrl in the same call
- `confirmedUtmParameters` — object: The same for confirmedRedirectUrl; needs confirmedRedirectUrl in the same call
- `copyFromOptInProcessId` — null | integer (minimum 1): Existing process to copy settings and confirmation email from; the arguments above still win
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-opt-in-process` · I

**Update opt-in process**

Changes the settings of one KlickTipp opt-in process (also called subscription process or subscriber list): name, opt-in mode, redirect URLs with their query and UTM parameters, confirmation resend, change-email role, deletion of unconfirmed contacts, labels and notes. Only the arguments that are given are written, the rest keeps its current value. Settings take effect for contacts subscribing from now on; contacts already in the process are not touched and nothing is sent. Single opt-in subscribes later contacts without confirming, which is not permitted everywhere - ask before setting it. The confirmation email is written with the opt-in confirmation email tools. A page parameter is a NAME the platform fills with contact data; a UTM parameter is a VALUE under a fixed name. Both reach a page only together with that page's URL in the same call. get-opt-in-process reads them.

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
- `metaLabels` — array | null (maxItems 50): Complete list of labels; replaces the existing labels, empty array removes them all
- `pendingPageParameters` — object: Query parameters appended to pendingRedirectUrl, by the name each is appended under; needs pendingRedirectUrl in the same call
- `confirmedPageParameters` — object: Query parameters appended to confirmedRedirectUrl, by the name each is appended under; needs confirmedRedirectUrl in the same call
- `pendingUtmParameters` — object: Campaign tracking values appended to pendingRedirectUrl, by query name; the value, not the name; needs pendingRedirectUrl in the same call
- `confirmedUtmParameters` — object: The same for confirmedRedirectUrl; needs confirmedRedirectUrl in the same call
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `delete-opt-in-process` · D

**Delete opt-in process**

Deletes one KlickTipp opt-in process (also called subscription process or subscriber list) together with its confirmation email. The contacts that subscribed through it keep their subscription and are not deleted. Refused for the default process of the account, and for a process that forms, campaigns or other entities still refer to -- the refusal names what refers to it, so those can be pointed elsewhere first. This cannot be undone, so only call it for a process the user has explicitly asked to delete, named by the ID that get-opt-in-process reports.

Parameter:

- `optInProcessId`* — integer (minimum 1): ID of the opt-in process to delete
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `get-opt-in-confirmation-email` · RI

**Get opt-in confirmation email**

Reads who the confirmation email of a double opt-in process comes from: its subject, the sender name and address, reply-to, CC and BCC, and the sender domain. It also names what may be chosen: senderEmailOptions are the addresses the account can send from, senderDomainOptions the domains it may pick between, empty when it has no choice. An empty stored sender or reply-to is reported as the account's own address; senderIdentity reports its current status and concrete choices. The body is not part of this answer -- it is get-opt-in-confirmation-email-content. A confirmation email is not a drag-and-drop document, so the block tools do not accept it; the answer carries bodyIsEditable false for that reason and an editUrl into the KlickTipp editor. Single opt-in processes still have this email stored; it is simply not sent. Change it with update-opt-in-confirmation-email.

Parameter:

- `optInProcessId`* — integer (minimum 1): ID of the opt-in process whose confirmation email is read
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-opt-in-confirmation-email` · I

**Update opt-in confirmation email**

Changes the settings of the confirmation email a double opt-in process sends: subject, sender name and address, reply-to, CC, BCC and sender domain. Only the arguments that are given are written, except that senderDomain may be normalized when account domain state changed. A sender address has to be configured and covered by a live verified domain. For an ordinary sender address, senderDomain is checked and derived when omitted; a dispatch profile keeps deciding both values itself. The body is not written here: that is update-opt-in-confirmation-email-content, and the block tools do not accept this email at all. This email is the legal record of a contact's consent in many countries: change its sender or subject only when the user asked for it, and say what was changed.

Parameter:

- `optInProcessId`* — integer (minimum 1): ID of the opt-in process whose confirmation email is changed
- `subject` — null | string (minLength 1; maxLength 250): Subject line of the confirmation email
- `senderName` — null | string (minLength 1; maxLength 250): Name the email comes from
- `senderEmail` — null | string (maxLength 250): Configured address the email comes from, or empty for the account's own address
- `replyToEmail` — null | string (maxLength 250): Address a reply goes to; empty string returns it to the account's own address
- `ccEmail` — null | string (maxLength 250): Address that receives a copy; empty string removes it
- `bccEmail` — null | string (maxLength 250): Address that receives a blind copy; empty string removes it
- `senderDomain` — null | string (maxLength 250): Domain the email is sent through; omit to derive it from the resulting sender address
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `get-opt-in-confirmation-email-content` · RI

**Get opt-in confirmation email content**

Reads the body of the confirmation email a double opt-in process sends: its subject, its HTML body and its plain-text body, and which of the two it actually sends. Both bodies are always returned, because which one a recipient sees is their mail client's choice. This email is not a drag-and-drop document and the block tools do not work on it -- its text is rich text, written with update-opt-in-confirmation-email-content or by hand in the KlickTipp editor the answer links to. Sender, reply-to and the rest are get-opt-in-confirmation-email.

Parameter:

- `optInProcessId`* — integer (minimum 1): ID of the opt-in process whose confirmation email is read
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-opt-in-confirmation-email-content` · I

**Update opt-in confirmation email content**

Replaces the body of the confirmation email a double opt-in process sends. html and plain are each written whole, not patched, and a part that is not given keeps its text -- so writing only one leaves the email saying two different things to two recipients. Write both. The platform checks the result the way the editor does: errors, such as a missing unsubscribe link or an empty subject, stop the write and are returned in validationMessages with stored false; warnings do not. This email is the legal record of a contact's consent in many countries -- it must still say who is subscribing them to what. Change it only when the user asked for it, and say what changed.

Parameter:

- `optInProcessId`* — integer (minimum 1): ID of the opt-in process whose confirmation email is written
- `html` — null | string (maxLength 500000): Complete HTML body; replaces the current one, empty string makes the email plain-text only
- `plain` — null | string (maxLength 500000): Complete plain-text body; replaces the current one
- `subject` — null | string (minLength 1; maxLength 150): Subject line
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `preview-opt-in-confirmation-email` · ROI

**Preview opt-in confirmation email**

Displays the confirmation email of an opt-in process in an MCP App, so it can be looked at before a contact gets it. Shows the body as STORED: the signature, the confirmation link and the recipient's own data behind the placeholders are added per recipient when it is sent, so they are not in this picture and their absence is not a fault. A plain-text-only email is shown as its text. Changes nothing and creates no contact -- unlike the preview screen of the app, which makes a preview contact. The result carries contentHtml for hosts without MCP Apps support; to receive a real one, use send-opt-in-confirmation-email-test.

Parameter:

- `optInProcessId`* — integer (minimum 1): ID of the opt-in process whose confirmation email is shown
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `send-opt-in-confirmation-email-test` · DO

**Send opt-in confirmation email test**

Sends the confirmation email of an opt-in process as a test to a single address, so its text can be read before a contact gets it -- the same send the test dialog of KlickTipp performs. Any address may receive one, and an address that is not a contact of the account yet becomes one and is tagged as a test recipient, which can start automations; name the address and say what it will become before calling this. The confirmation link in a test does not confirm anybody. Nothing about the opt-in process changes, and no contact of it is a recipient. Read the body first with get-opt-in-confirmation-email-content.

Parameter:

- `optInProcessId`* — integer (minimum 1): ID of the opt-in process whose confirmation email is sent
- `recipientEmail`* — string (minLength 3; maxLength 250): Address the test goes to; becomes a contact of the account if it is not one yet
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in
## `search-contacts` · RI

**Search contacts**

Returns a cursor-paginated list of contact channels in one KlickTipp account, sorted by address. One row is one channel: a contact reachable by email and by SMS appears twice, each time with that channel's own address and subscription status, and channel says which it is. The lean results carry the contact ID, address, status and edit link, and intentionally omit contact fields and reference data. query takes an email fragment or a mobile number written with its country code (+49... or 0049...); a number in a form the account cannot read is refused by name rather than answered with nothing. Filter further by status, channel or a writable manual tag. The returned nextCursor, unchanged and with the same filters, is the next page. One contact in full is get-contact.

Parameter:

- `query` — null | string (maxLength 250): Case-insensitive email-address fragment; omit to match every email contact
- `status` — null | string (einer von `pending`, `optin`, `subscribed`, `unsubscribed`): Email subscription status to filter by; omit for every status
- `channel` — null | string (einer von `email`, `sms`): Restrict to one channel, email or sms; omit for both
- `manualTagId` — null | integer (minimum 1): ID of an existing manual tag the returned contacts must have
- `cursor` — null | string (maxLength 500): Opaque nextCursor value of the previous result page; omit for the first page
- `pageSize` — integer (minimum 1; maximum 100; Default `25`): Maximum contacts on the page, from 1 through 100
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `get-contact` · RI

**Get contact**

Returns the permitted detail view of one contact in a KlickTipp account: email address and email subscription status, mobile number and SMS subscription status, contact fields for the requested reference, writable manual tag IDs and the edit link. A contact reachable on only one of the two channels is answered with the other one empty, and is found either way. Every field carries its data type, and the three that are stored as numbers are answered exactly as KlickTipp shows them on screen: a date as 16.09.2026, a moment as 16.09.2026 14:30, a time of day as 14:30, in the time zone the account is configured for. It does not expose complete channel or subscription-reference records.

Parameter:

- `contactId`* — integer (minimum 1): Numeric contact ID returned by search-contacts
- `referenceId` — integer (minimum 0; Default `0`): Reference whose multi-value fields and manual tags to read; 0 for contact-wide values
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `upsert-subscribed-contact` · D O

**Create contact**

Adds one contact to a KlickTipp account by hand, with its contact-field values in the same call -- the Add Contact screen of the app. Takes an email address, a mobile number, or both. The contact is subscribed at once, through no opt-in process and without a confirmation message, so it is reachable by the next mailing; automations may start. Only for addresses the account may write to by hand: an address that unsubscribed is refused, the account needs the add-contacts permission, and the call counts against its daily import limit. An address the account already has is updated rather than added twice, and the values given overwrite what it held; the answer says so in alreadyExisted. An unknown field ID or tag is refused, never skipped. Use subscribe-contact-via-opt-in-process to let an address opt in through a named process instead.

Parameter:

- `email` — null | string (maxLength 250): Email address of the contact; at least one of email and phoneNumber is required
- `phoneNumber` — null | string (maxLength 50): Mobile number with country code, as +49170... or 0049170...; at least one of email and phoneNumber is required
- `tagId` — null | integer (minimum 1): Manual tag to assign to the contact; omit for none
- `fields` — array (maxItems 50): Contact field values to write with the contact, each {fieldId, value} as get-contact and search-custom-fields name them
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-contact-values` · DO

**Update contact**

Updates explicitly listed contact-field values for one contact. It cannot change email or SMS addresses, opt-in state, subscriptions, lists or other channel data. Every custom-field ID and the contact itself must belong to the selected account; global contact fields remain available. Date, time and datetime fields take the forms get-contact answers with -- 16.09.2026, 16.09.2026 14:30, 14:30 -- and ISO 8601 as well, for a caller that computed a date rather than read one. Anything else is refused rather than stored as a date it was not meant to be, and the refusal names the form that works. An empty value clears the field.

Parameter:

- `contactId`* — integer (minimum 1): Numeric contact ID returned by search-contacts
- `fields`* — array<object> (minItems 1; maxItems 50): Contact field updates; fieldId must be a global field key or an account-owned numeric custom-field ID, a date, time or datetime value takes the form get-contact answers with, and referenceId defaults to 0
  - `fieldId`* — string (minLength 1; maxLength 15)
  - `value`* — string (maxLength 65535)
  - `referenceId` — integer (minimum 0; Default `0`)
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `tag-contact` · O

**Assign manual tag**

Assigns one existing writable manual tag to one contact. This may immediately start or alter campaigns, autoresponders, outbound events and automations. The caller must explicitly approve those effects. Unknown, foreign or non-manual tags are rejected and never created.

Parameter:

- `contactId`* — integer (minimum 1): Numeric contact ID returned by search-contacts
- `manualTagId`* — integer (minimum 1): Existing writable manual tag ID; unknown tags are rejected and never created
- `approval`* — string (einer von `I_ACCEPT_AUTOMATION_EFFECTS`): Exactly I_ACCEPT_AUTOMATION_EFFECTS: tagging may start campaigns and automations
- `referenceId` — integer (minimum 0; Default `0`): Reference for a multi-value manual tag; use 0 for contact-wide tags
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `untag-contact` · DOI

**Remove manual tag**

Removes one existing writable manual tag from one contact. This may immediately alter campaigns, autoresponder queues and automations, so the caller must explicitly approve those effects. Removing a tag does not unsubscribe-contact the contact and changes no subscription or channel state.

Parameter:

- `contactId`* — integer (minimum 1): Numeric contact ID returned by search-contacts
- `manualTagId`* — integer (minimum 1): Existing writable manual tag ID to remove
- `approval`* — string (einer von `I_ACCEPT_AUTOMATION_EFFECTS`): Exactly I_ACCEPT_AUTOMATION_EFFECTS: removal may alter campaigns and automations
- `referenceId` — integer (minimum 0; Default `0`): Reference for a multi-value manual tag; use 0 for contact-wide tags
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `subscribe-contact-via-opt-in-process` · DO

**Subscribe contact**

Subscribes exactly one email or SMS channel of a KlickTipp contact through an opt-in process and creates or reuses the contact and requested reference. Its effects reach a real recipient: it may send a confirmation message and may start automations. It takes either an email address or a phone number, never both. Assigning the optional tag may start further automations or outbound events. Other channels and references are not changed.

Parameter:

- `optInProcessId`* — integer (minimum 1): ID of the opt-in process to run
- `approval`* — string (einer von `subscribe-contact`): Exactly "subscribe-contact": acknowledges a confirmation message, automations and a changed real recipient
- `email` — null | string (maxLength 250): Email channel to subscribe; mutually exclusive with phoneNumber
- `phoneNumber` — null | string (maxLength 50): SMS channel to subscribe in E.164 format; mutually exclusive with email
- `referenceId` — integer (minimum 0; Default `0`): Subscription reference context to create or reuse; a non-zero ID must exist in the account
- `tagId` — null | integer (minimum 1): Tag to additionally assign to the contact after a successful subscription
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `unsubscribe-contact` · DOI

**Unsubscribe contact**

Unsubscribes exactly one email or SMS channel of a KlickTipp contact. Its effects reach a real recipient: future subscribed-audience messages on that channel stop, and automations may run. It takes either an email address or a phone number, never both. Other channels of the same contact and all subscription references remain untouched.

Parameter:

- `approval`* — string (einer von `unsubscribe-contact`): Exactly "unsubscribe-contact": acknowledges a changed real recipient and automations
- `email` — null | string (maxLength 250): Email channel to unsubscribe; mutually exclusive with phoneNumber
- `phoneNumber` — null | string (maxLength 50): SMS channel to unsubscribe in E.164 format; mutually exclusive with email
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `get-opt-in-process-redirect-url` · RI

**Get subscription redirect URL**

Returns the URL one contact is redirected to by an opt-in process. The contact's email address is required and is what the answer is about: the URL carries that contact's own id, address and subscriber key, so an address nobody named produces a URL about the wrong person. Which page comes back follows the contact's state, reported as redirectPage: while the double opt-in confirmation is still open it is the pending page, and only a confirmed contact gets the thank-you page -- a pending answer means that contact has not confirmed yet, not that the process is misconfigured. The URL also carries the page's campaign tracking. Processes without a custom page fall back to the KlickTipp-hosted pending or thank-you page.

Parameter:

- `email`* — string (minLength 3; maxLength 250): Email address of the contact the URL is resolved for; required, and it identifies which contact the URL points at
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

Creates a custom field definition in KlickTipp and returns its ID and the placeholder that renders it in newsletter content. Creating a field stores no value and changes no contact. Fields are never created as a side effect elsewhere, so a field a contact should have a value in has to be created here first. The data type is picked once and for good: it cannot be changed afterwards, so pick the one that matches what will be stored -- a date field for a date, a number field for an amount. multiValue decides whether a contact holds one value PER SUBSCRIPTION (true, the default when omitted) or one value overall (false); it is worth deciding here, because an existing field can only go from true to false and never back. The name has to be unique within the account. The description is what tells a later reader what belongs in the field.

Parameter:

- `name`* — string (minLength 1; maxLength 250): Name of the field, which has to be unique within the account
- `type`* — string (einer von `field-single`, `field-paragraph`, `field-email`, `field-number`, `field-url`, `field-date`, `field-time`, `field-datetime`, `field-html`, `field-decimal`): Data type of the field, which decides what can be stored in it and cannot be changed afterwards
- `description` — null | string (maxLength 2000): What the field holds, so a person or a model reading it later knows what to write into it
- `multiValue` — null | boolean: True: one value per subscription; false: one value overall; omit for true
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-custom-field` · I

**Update custom field**

Changes the name, description, group, labels, cardinality, subscription-email key, note or copy target of a custom field. Only what is passed is written; an empty string clears a text setting. The data type cannot be changed and is refused: an existing field keeps the type its stored values were written in. multiValue false collapses the field to ONE value per contact and DELETES the extra values contacts hold per subscription -- ask the person first, it cannot be undone and true is then refused for good. requestName is the key a contact writes as "key = value" in the body of a subscription email to fill this field; it addresses the field, so two fields sharing one means the first wins. copyToFieldId must name a field of a compatible type or the change is refused. Only fields the account created itself can be changed; the global ones are refused.

Parameter:

- `customFieldId`* — string (minLength 1; maxLength 100; Muster `^[A-Za-z0-9_]+$`): ID of the field to change
- `name` — null | string (maxLength 250): New name of the field, which has to stay unique within the account; omit to keep the current one
- `description` — null | string (maxLength 2000): New description of what the field holds; omit to keep the current one
- `category` — null | string (maxLength 250): Group in the app; empty string sorts into none; omit to keep
- `metaLabels` — array | null (maxItems 50): New set of labels of the field, which replaces the current one; omit to keep the current labels
- `multiValue` — null | boolean: False collapses the field to one value per contact and DELETES the others; true is refused on a field that is already false; omit to keep
- `requestName` — null | string (maxLength 250): Key this field is addressed by in a subscription email body; empty string removes it; omit to keep
- `copyToFieldId` — null | string (maxLength 100; Muster `^[A-Za-z0-9_]*$`): ID of the field every value written here is also copied into; empty string stops the copying; omit to keep
- `notes` — null | string (maxLength 1000): Internal note on the field, which nobody outside the account sees; empty string removes it; omit to keep
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

Creates a manual tag in KlickTipp, one that is assigned deliberately rather than by KlickTipp itself. Creating a tag assigns it to nobody and changes no contact. Tags are never created as a side effect elsewhere, so a tag a contact should carry has to be created here first. The name has to be unique within the account. The description is what tells a later reader what the tag means.

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
