# Die veröffentlichten Verträge — Kontakte und Konto-Einstellungen

Wort für Wort das, was der Server in `tools/list` für die 8 Werkzeuge dieses Skills
ausliefert: Beschreibung, Annotationen, jeder Parameter mit Typ, Grenzen und Beschreibung. Ein `*`
markiert Pflichtparameter. `R` liest nur · `D` löscht oder ersetzt ohne Undo · `O` erreicht etwas
außerhalb des Kontos · `I` ein zweiter gleicher Aufruf ändert nichts mehr.

Diese Datei spiegelt den Server, sie interpretiert ihn nicht: ändert sich eine
Werkzeugbeschreibung, wird sie hier wörtlich nachgezogen. Wofür ein Werkzeug da ist, was es nicht
tut und woran man sich stößt, steht in [tools.md](tools.md).

## Inhalt

`search-contacts` · `get-contact` · `upsert-subscribed-contact` · `update-contact-values` · `subscribe-contact-via-opt-in-process` · `unsubscribe-contact` · `get-account-settings` · `update-account-settings`

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

## `get-account-settings` · RI

**Get Account Settings**

Reads the settings of a KlickTipp account, the ones its settings screen shows: the feature switches, the preview marker tag and the email blacklist. Only the settings this account may actually edit are in the answer -- one it may not edit is absent rather than false, because the platform keeps several of them for support. Credentials of connected services are reported as configured or not, never by value, so no API key ends up in an answer. Personal information, privacy settings, the data processing order and sender addresses are not part of this tool. Change a setting with update-account-settings. Reads only: this writes nothing.

Parameter:

- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-account-settings` · I

**Update Account Settings**

Changes settings of a KlickTipp account and answers with the settings as they now stand. Only the settings named in the call are written; everything else keeps its value, so a caller does not have to send back what it does not change. A setting this account may not edit is refused by name rather than ignored -- the platform keeps several of them for support, and get-account-settings reports which ones this account has. Credentials of connected services cannot be set here at all; that stays in the KlickTipp app. Read the current state with get-account-settings first. Every named value is checked first -- a preview tag must exist in the account, the blacklist must be well formed -- and one bad or forbidden setting refuses the whole call with nothing written. refusals only lists what the platform turned down while saving; the other changes are then saved.

Parameter:

- `settings`* — object: The settings to change, by name; every setting left out keeps its value
  - `enableMetaLabels` — boolean
  - `enableNotes` — boolean
  - `enableDdEditorManualSaveButton` — boolean
  - `disableEmailSignatureSeparator` — boolean
  - `deactivateUserNotificationEmails` — boolean
  - `plainTextContentByUser` — boolean
  - `useEnglishSubscriberArea` — boolean
  - `deactivateGlobalBounceManagement` — boolean
  - `unlimitedEmailsPerDay` — boolean
  - `allowSingleOptInProcess` — boolean
  - `allowSignaturesWithoutParameters` — boolean
  - `allowKlicktippSenderAddress` — boolean
  - `allowEmailRewriting` — boolean
  - `knownForSpamActivity` — boolean
  - `previewSubscriberMarkerTag` — string (maxLength 100; pattern ^[0-9]*$): ID of an existing tag of this account that marks preview subscribers; empty string removes it
  - `emailBlacklist` — string (maxLength 100000): Addresses and domains this account never sends to, one per line; empty string clears it
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in
