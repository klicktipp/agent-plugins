# Die veröffentlichten Verträge — Opt-in-Prozesse und Bestätigungsmail

Wort für Wort das, was der Server in `tools/list` für die 12 Werkzeuge dieses Skills
ausliefert: Beschreibung, Annotationen, jeder Parameter mit Typ, Grenzen und Beschreibung. Ein `*`
markiert Pflichtparameter. `R` liest nur · `D` löscht oder ersetzt ohne Undo · `O` erreicht etwas
außerhalb des Kontos · `I` ein zweiter gleicher Aufruf ändert nichts mehr.

Diese Datei spiegelt den Server, sie interpretiert ihn nicht: ändert sich eine
Werkzeugbeschreibung, wird sie hier wörtlich nachgezogen. Wofür ein Werkzeug da ist, was es nicht
tut und woran man sich stößt, steht in [tools.md](tools.md).

## Inhalt

`search-opt-in-processes` · `get-opt-in-process` · `create-opt-in-process` · `update-opt-in-process` · `delete-opt-in-process` · `get-opt-in-confirmation-email` · `update-opt-in-confirmation-email` · `get-opt-in-confirmation-email-content` · `update-opt-in-confirmation-email-content` · `preview-opt-in-confirmation-email` · `send-opt-in-confirmation-email-test` · `get-opt-in-process-redirect-url`

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

## `get-opt-in-process-redirect-url` · RI

**Get subscription redirect URL**

Returns the URL one contact is redirected to by an opt-in process. The contact's email address is required and is what the answer is about: the URL carries that contact's own id, address and subscriber key, so an address nobody named produces a URL about the wrong person. Which page comes back follows the contact's state, reported as redirectPage: while the double opt-in confirmation is still open it is the pending page, and only a confirmed contact gets the thank-you page -- a pending answer means that contact has not confirmed yet, not that the process is misconfigured. The URL also carries the page's campaign tracking. Processes without a custom page fall back to the KlickTipp-hosted pending or thank-you page.

Parameter:

- `email`* — string (minLength 3; maxLength 250): Email address of the contact the URL is resolved for; required, and it identifies which contact the URL points at
- `optInProcessId` — null | integer (minimum 1): Opt-in process to resolve for; omit for the one the subscriber signed up through
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in
