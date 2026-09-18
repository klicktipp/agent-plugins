# Die veröffentlichten Verträge — Newsletter, Versand und Signaturen

Wort für Wort das, was der Server in `tools/list` für die 14 Werkzeuge dieses Skills
ausliefert: Beschreibung, Annotationen, jeder Parameter mit Typ, Grenzen und Beschreibung. Ein `*`
markiert Pflichtparameter. `R` liest nur · `D` löscht oder ersetzt ohne Undo · `O` erreicht etwas
außerhalb des Kontos · `I` ein zweiter gleicher Aufruf ändert nichts mehr.

Generiert aus `build/tools-list.json` (Stand 2026-09-18) mit `build/contracts.py` — nicht von Hand
ändern, sondern den Dump erneuern und neu erzeugen. Wofür ein Werkzeug da ist, was es nicht tut
und woran man sich stößt, steht in [tools.md](tools.md).

## `email-signature-search` · RI

**Search email signatures**

Lists the email signatures of a KlickTipp account that a newsletter can carry, with ID, name, the sender name and address of their sender profile, the state of that address, and the tags that make KlickTipp pick a signature by itself. A signature that cannot go under a newsletter as it stands -- no content, missing legally required placeholders, or a sender address that may not be sent from -- is left out unless unusable signatures are asked for, in which case it comes with the reasons why. The signature text is not part of the list; use email-signature-get for that. To have KlickTipp pick the signature by tagging instead of naming one, pass signature ID 0 to email-newsletter-delivery-configure; that is not an entry of this list.

Parameter:

- `query` — null | string (maxLength 250): Text the name of a signature has to contain; omit to list them all
- `includeUnusable` — null | boolean: True to also return signatures that cannot currently be used, with their blockers; omit to leave them out
- `limit` — null | integer (minimum 1; maximum 200): How many signatures to return at most, 1 to 200, 50 by default
- `accountId` — null | integer (minimum 1): User ID of the account to list signatures for; omit for the token account, or pass an accessible subaccount ID

## `email-signature-get` · RI

**Get email signature**

Returns one email signature with its name, notes, labels, tag IDs, sender profile, digital business card, content flags, usability and blockers. includeContent adds the HTML, plain and transactional content itself, which is the bulk of the answer.

Parameter:

- `signatureId`* — integer (minimum 1): ID of the signature to read
- `includeContent` — null | boolean: True to include HTML, plain and transactional content; omit to return only content flags
- `accountId` — null | integer (minimum 1): User ID of the account that owns the signature; omit for the token account, or pass an accessible subaccount ID

## `email-signature-create` · O

**Create email signature**

Creates or copies an email signature. Name and tag IDs replace source values; supplied content, sender and business-card fields override copied values, while omitted copied fields stay. HTML needs %Link:Unsubscribe% as the href of a link plus %User:FirstName%, %User:LastName%, %User:Street%, %User:Zip%, %User:City% and %User:Country%; allowed address omissions are exempt. Plain needs the same, but unsubscribe may be text; it is stored only when plain-content editing is allowed, otherwise regenerated from HTML. Transactional HTML needs the address placeholders and no %Link:Unsubscribe%; %Link:SubscriberInfo% is recommended. Tags, addresses and domains must exist, and an assigned sender domain must match. Returns content flags only; use email-signature-get with includeContent true. No newsletter changes.

Parameter:

- `name`* — string (minLength 1; maxLength 250): Unique name of the new signature
- `tagIds`* — array<integer> (maxItems 50): At least one existing tag ID for the new signature; every tag must be unassigned to another signature
- `sourceSignatureId` — null | integer (minimum 1): Existing signature of the same account to copy; omit when supplying content for a new signature
- `content` — object: Complete HTML, plain and transactional content block; required without a source and replaces copied content when supplied
  - `html`* — string (minLength 1; maxLength 65536)
  - `plain` — string (maxLength 65536)
  - `useInTransactionalEmails` — boolean
  - `transactionalHtml` — string (maxLength 65536)
- `senderProfile` — object: Optional sender, reply, CC, BCC, recipient and sender-domain fields; omitted copied fields are preserved, and a sender address with an assigned domain requires that matching senderDomain
  - `senderName` — string (maxLength 250)
  - `senderEmail` — string (maxLength 250)
  - `replyToEmail` — string (maxLength 250)
  - `ccEmail` — string (maxLength 250)
  - `bccEmail` — string (maxLength 250)
  - `toEmail` — string (maxLength 250)
  - `senderDomain` — string (maxLength 250)
- `vCard` — object: Optional plain-text digital-business-card fields; supplied fields override copied values, omitted copied fields stay, and empty strings clear fields
  - `firstName` — string (maxLength 128)
  - `lastName` — string (maxLength 128)
  - `companyName` — string (maxLength 128)
  - `emailAddress` — string (maxLength 128)
  - `phone` — string (maxLength 128)
  - `cellPhone` — string (maxLength 128)
  - `street` — string (maxLength 128)
  - `zip` — string (maxLength 128)
  - `city` — string (maxLength 128)
  - `state` — string (maxLength 128)
  - `country` — string (maxLength 128)
  - `website` — string (maxLength 250)
- `notes` — null | string (maxLength 1000): Internal note; on a copy, omit to preserve the source note
- `metaLabels` — array | null (maxItems 50): Labels; on a copy, omit to preserve the source labels
- `accountId` — null | integer (minimum 1): User ID of the account in which to create the signature; omit for the token account, or pass an accessible subaccount ID

## `email-signature-update` · I

**Update email signature**

Changes the name, internal note, labels or digital business card of an email signature. Omitted fields stay unchanged and empty business-card strings clear those fields. Content, tag IDs and sender profile are never changed.

Parameter:

- `signatureId`* — integer (minimum 1): ID of the signature to update
- `name` — null | string (minLength 1; maxLength 250): New unique name; omit to keep it, and note that the default signature cannot be renamed
- `notes` — null | string (maxLength 1000): New internal note; omit to keep it, or pass an empty string to clear it
- `metaLabels` — array | null (maxItems 50): Replacement labels; omit to keep them, or pass an empty array to clear them
- `vCard` — object: Plain-text digital-business-card fields to change; omitted fields stay unchanged and empty strings clear fields
  - `firstName` — string (maxLength 128)
  - `lastName` — string (maxLength 128)
  - `companyName` — string (maxLength 128)
  - `emailAddress` — string (maxLength 128)
  - `phone` — string (maxLength 128)
  - `cellPhone` — string (maxLength 128)
  - `street` — string (maxLength 128)
  - `zip` — string (maxLength 128)
  - `city` — string (maxLength 128)
  - `state` — string (maxLength 128)
  - `country` — string (maxLength 128)
  - `website` — string (maxLength 250)
- `accountId` — null | integer (minimum 1): User ID of the account that owns the signature; omit for the token account, or pass an accessible subaccount ID

## `email-signature-content-replace` · DOI

**Replace email signature content**

Replaces normal HTML and plain content with no MCP undo. Transactional fields change only when supplied; false plus an empty transactionalHtml disables and clears them. HTML needs %Link:Unsubscribe% as the href of a link plus %User:FirstName%, %User:LastName%, %User:Street%, %User:Zip%, %User:City% and %User:Country%; allowed address omissions are exempt. Plain needs the same, but unsubscribe may be text; it is stored only when plain-content editing is allowed, otherwise regenerated from HTML. Transactional HTML needs the address placeholders and no %Link:Unsubscribe%; %Link:SubscriberInfo% is recommended. Returns content flags only; use email-signature-get with includeContent true. Name, notes, labels, tags, sender profile and business card stay unchanged.

Parameter:

- `signatureId`* — integer (minimum 1): ID of the signature whose normal content is replaced and whose transactional content may be changed
- `html`* — string (minLength 1; maxLength 65536): Complete HTML signature content
- `plain` — null | string (maxLength 65536): Complete plain content; stored trimmed only when plain-content editing is enabled, otherwise regenerated from HTML
- `useInTransactionalEmails` — null | boolean: Whether the signature is used in transactional emails; omit to keep the current setting
- `transactionalHtml` — null | string (maxLength 65536): Complete transactional HTML content; omit to keep it, or pass an empty string with useInTransactionalEmails false to clear it
- `accountId` — null | integer (minimum 1): User ID of the account that owns the signature; omit for the token account, or pass an accessible subaccount ID

## `email-signature-delivery-configure` · OI

**Configure email signature delivery**

Changes only assigned tag IDs and sender, reply, CC, BCC, recipient and sender-domain fields. Omitted fields stay unchanged. Every ID must already belong to the account; this tool never creates tags, addresses or domains. A sender address with an assigned domain requires that matching senderDomain. Content, metadata and the digital business card stay unchanged.

Parameter:

- `signatureId`* — integer (minimum 1): ID of the signature whose delivery configuration is changed
- `tagIds` — array | null (maxItems 50): Replacement tag IDs that already exist; ordinary signatures require at least one, and every tag must be unassigned to another signature, while the default signature may use an empty array
- `senderProfile` — object: Sender name and configured account address/domain values; reply options are also used for CC, BCC and recipient, empty strings clear optional fields, omitted fields stay unchanged, and a sender address with an assigned domain requires that matching senderDomain
  - `senderName` — string (maxLength 250)
  - `senderEmail` — string (maxLength 250)
  - `replyToEmail` — string (maxLength 250)
  - `ccEmail` — string (maxLength 250)
  - `bccEmail` — string (maxLength 250)
  - `toEmail` — string (maxLength 250)
  - `senderDomain` — string (maxLength 250)
- `accountId` — null | integer (minimum 1): User ID of the account that owns the signature; omit for the token account, or pass an accessible subaccount ID

## `email-newsletter-search` · RI

**Search newsletters**

Lists the email newsletters of a KlickTipp account, newest first: newsletter ID, email ID, name, delivery state, creation and dispatch moment, split-test flag and deep links. Narrow by a name fragment, by status (draft, scheduled, outgoing, sent) and by two half-open time windows on creation (createdFrom/createdBefore) and dispatch (sendDateFrom/sendDateBefore), ISO 8601 with UTC offset. Paged by cursor: hand nextCursor back unchanged with the same filters. A draft has no dispatch moment and never matches a sendDate window; a split test has no single email, its emailId is null. Subject, content, audience and statistics are read per newsletter through email-newsletter-get. SMS newsletters, autoresponders and automations are not included.

Parameter:

- `query` — null | string (maxLength 250): Text the name of a newsletter has to contain; omit to list them all
- `status` — null | string (einer von `draft`, `scheduled`, `outgoing`, `sent`): Only newsletters in this delivery state: "draft", "scheduled", "outgoing" or "sent"
- `createdFrom` — null | string (Muster `^\d{4}-\d{2}-\d{2}[Tt ]\d{2}:\d{2}(:\d{2})?([Zz]|[+-]\d{2}:?\d{2})$`): Created at or after this moment, ISO 8601 with UTC offset ("2026-09-01T10:00:00+02:00")
- `createdBefore` — null | string (Muster `^\d{4}-\d{2}-\d{2}[Tt ]\d{2}:\d{2}(:\d{2})?([Zz]|[+-]\d{2}:?\d{2})$`): Only newsletters created before this moment, exclusive, same format
- `sendDateFrom` — null | string (Muster `^\d{4}-\d{2}-\d{2}[Tt ]\d{2}:\d{2}(:\d{2})?([Zz]|[+-]\d{2}:?\d{2})$`): Dispatch moment at or after this one, same format; a draft has none and never matches
- `sendDateBefore` — null | string (Muster `^\d{4}-\d{2}-\d{2}[Tt ]\d{2}:\d{2}(:\d{2})?([Zz]|[+-]\d{2}:?\d{2})$`): Only newsletters whose dispatch moment lies before this one, exclusive, same format
- `limit` — null | integer (minimum 1; maximum 100): How many newsletters to return at most, 1 to 100, 25 by default
- `cursor` — null | string (minLength 8; maxLength 200): nextCursor of the previous page, with the same filters; omit for the first page
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-newsletter-get` · RI

**Get newsletter**

Returns one email newsletter of a KlickTipp account: identity, lifecycle state, editor type, split-test flag and deep links. Everything else is a projection requested through "include": "metadata" (name, note, labels, subject), "audience", "deliveryConfiguration" (sender, reply address, signature), "deliveryStatus" (send date, recipients, counters, what is missing), "audienceReach" (contacts it would reach now) and "conversionPixel" (tracking snippets for a thank-you page, one per sender domain; hand one to the user verbatim). The body is not here -- read it with email-get. Reads only; requested projections are answered whole or the call fails. A split test has one email per variant and no single email: emailId, contentUrl and metadata.subject are null, splitTestVariants lists the variants, and deliveryConfiguration needs one of their editorUrl.

Parameter:

- `newsletterId`* — integer (minimum 1): ID of the newsletter, as shown in the KlickTipp app URL
- `include` — array<string> (maxItems 6): Projections to add: "metadata", "audience", "deliveryConfiguration", "deliveryStatus", "audienceReach", "conversionPixel"; omit for identity and lifecycle only. The body is email-get
- `editorUrl` — null | string (minLength 12; maxLength 500): Editor URL naming one variant of a split test, from splitTestVariants; omit for a newsletter with a single email
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-newsletter-draft-create`

**Create newsletter draft**

Creates an email newsletter draft in KlickTipp -- name, subject, optional preheader -- and returns newsletter ID, email ID and deep links. Nothing is sent. A draft has no audience filter yet: an unfiltered audience means every active contact of the account (mode "all_contacts"). The subject is the line every recipient sees; changing it later through email-newsletter-draft-update invalidates the content revisions read before. Body: block tools (email-text-write and siblings). Audience: email-newsletter-draft-update. Sender: email-newsletter-delivery-configure. "splitTest" makes it a split test, irreversibly, with one variant -- more via email-split-test-variant-add, settings via email-split-test-configure; needs a premium account, "conversions"/"revenue" the conversion pixel, refused before creation.

Parameter:

- `name`* — string (minLength 1; maxLength 250): Name of the newsletter, unique within the account
- `subject`* — string (minLength 1; maxLength 998): Subject line, without HTML. It is the line every recipient sees, and no part of it is derived from anything else in this call. Correcting it later is email-newsletter-draft-update, which invalidates the content revisions read before
- `notes` — null | string (maxLength 1000): Internal note about the purpose of this newsletter, never part of the email
- `preheader` — null | string (maxLength 120): Inbox preview line, at most 120 characters, without HTML; omit to leave it empty. Not part of the content document: an HTML import cannot set it
- `splitTest` — object | null: Makes the newsletter a split test, irreversibly: "testSizePercent" (2-98), "testDurationHours" (1-27777), "winnerBy" ("opens", "clicks", "conversions", "revenue"; the last two need the conversion pixel). All three are required and KlickTipp has no default for any of them, so any value here is a choice somebody made; together they settle what share of real recipients gets a test version and for how long. Needs a premium account; omit for a normal newsletter
  - `testSizePercent`* — integer (minimum 2; maximum 98)
  - `testDurationHours`* — integer (minimum 1; maximum 27777)
  - `winnerBy`* — string (einer von `opens`, `clicks`, `conversions`, `revenue`)
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-newsletter-draft-update` · I

**Update newsletter draft**

Writes name, internal note, subject, preheader, audience and UTM campaign name of an email newsletter draft. Nothing is sent and no send date is set. Only drafts can be written; omitted arguments keep their value, a call without any change is refused. Writing subject or preheader invalidates every contentRevision read before, so read the content again before changing it. The audience replaces the previous one entirely and is given with an explicit mode -- "all_contacts" addresses every active contact of the account. The body is changed by the block tools, delivery configuration and scheduling by their own tools. Refuses a split test: its subject lives on the variants, see email-split-test-variant-update.

Parameter:

- `newsletterId`* — integer (minimum 1): ID of the newsletter to write, as returned by email-newsletter-draft-create
- `name` — null | string (maxLength 250): New name, unique within the account, at most 250 characters, without HTML; omit to keep
- `note` — null | string (maxLength 1000): Internal note, at most 1000 characters, without HTML; omit to keep
- `subject` — null | string (maxLength 998): New subject line, without HTML. Invalidates every contentRevision read before
- `audience` — object: Replaces the audience: "mode" is "all_contacts", "saved_audience" (with "audienceId") or "tag_conditions" (with the tag fields, at most 50 tags together); omit to keep
  - `mode`* — string (einer von `all_contacts`, `saved_audience`, `tag_conditions`): "all_contacts" (every active contact, no further field), "saved_audience" or "tag_conditions".
  - `audienceId` — integer (minimum 1): ID of the saved audience, for mode "saved_audience" only.
  - `includeTagIds` — array<integer> (maxItems 50): Tags a contact must carry, for "tag_conditions"; include and exclude together at most 50.
  - `includeTagsMatch` — string (einer von `any`, `all`): Whether "any" required tag is enough or "all" are needed.
  - `excludeTagIds` — array<integer> (maxItems 50): Tags that keep a contact out, for "tag_conditions"; include and exclude together at most 50.
  - `excludeTagsMatch` — string (einer von `any`, `all`): Whether "any" excluded tag already excludes or only "all" together do.
- `preheader` — null | string (maxLength 120): New inbox preview line, at most 120 characters, without HTML; empty string removes it, omit keeps it. Invalidates every contentRevision read before
- `utmCampaignName` — null | string (maxLength 120): Campaign name appended to tracked links as utm_campaign, at most 120 characters, without HTML; empty string restores the account default, omit keeps it
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-newsletter-draft-delete` · D

**Delete newsletter draft**

Deletes an email newsletter draft in KlickTipp, along with its email, its audience conditions and its system tags. Only drafts can be deleted: a newsletter that is scheduled, on its way out or already sent is refused, and so is one that other entities still refer to -- the refusal names them. This cannot be undone, so only call it for a newsletter the user has explicitly asked to delete.

Parameter:

- `newsletterId`* — integer (minimum 1): ID of the newsletter to delete
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-newsletter-delivery-configure` · I

**Configure newsletter delivery**

Writes the delivery configuration of an email newsletter in KlickTipp: sender name, sender address, reply address, sending domain and signature. Reports back what is still missing before the newsletter could be sent, together with the sender addresses, sending domains and signatures the account may use -- and refuses anything outside those lists before writing, naming what would be accepted. An explicit sender address and the sending domain have to belong together: changing the address alone is refused when the stored domain is not the one bound to it. This tool neither schedules nor activates anything and reaches no recipient -- activation is a separate tool. Arguments that are left out keep their current value. Only a newsletter that was never scheduled can be configured: any other lifecycle state is refused before anything is written.

Parameter:

- `newsletterId`* — integer (minimum 1): ID of the newsletter to configure
- `senderNameMode` — null | string (einer von `explicit`, `account_default`, `signature_dispatch_profile`): "explicit" (pass senderName), "account_default" or "signature_dispatch_profile"; omit to keep
- `senderName` — null | string (maxLength 250): Name the recipients see as the sender, for mode "explicit" only; omit to keep the current one
- `senderEmailMode` — null | string (einer von `explicit`, `account_default`, `signature_dispatch_profile`): "explicit" (pass senderEmail), "account_default" or "signature_dispatch_profile"; omit to keep
- `senderEmail` — null | string (maxLength 250): Sender address, one of the account's sender addresses; for mode "explicit"; omit to keep
- `replyToEmailMode` — null | string (einer von `explicit`, `account_default`, `signature_dispatch_profile`): "explicit" (pass replyToEmail), "account_default" or "signature_dispatch_profile"; omit to keep
- `replyToEmail` — null | string (maxLength 250): Address answers go to, for mode "explicit" only; omit to keep the current one
- `senderDomainMode` — null | string (einer von `explicit`, `account_default`, `signature_dispatch_profile`): "explicit" (pass senderDomain), "account_default" or "signature_dispatch_profile"; omit to keep
- `senderDomain` — null | string (maxLength 250): Domain the newsletter is sent through, one of availableSenderDomains; for mode "explicit"; omit to keep
- `signatureId` — null | integer (minimum 0): ID of the signature under the newsletter; 0 lets KlickTipp pick one by tagging; omit to keep
- `linkTracking` — null | boolean: Whether KlickTipp rewrites the links so clicks are counted; true is the normal case, omit to keep
- `headerLinks` — null | boolean: Whether KlickTipp puts its own line above the body with browser view, unsubscribe and report-spam links; omit to keep
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-newsletter-test-send` · DO

**Send newsletter test**

Sends one email newsletter as a test to a single address, so its content can be checked before it goes out -- the same send the test dialog of KlickTipp performs, with the same rules. Any address may receive one, and an address that is not a contact of the account yet becomes one and is tagged as a test recipient, which can start automations; name the address and say what it will become before calling this. A test carries the PUBLISHED content of the email: a body that was never published is refused -- publish it with email-content-publish -- and one changed after publication is sent with a warning that the test shows the older content. The audience of the newsletter is never a recipient, and its delivery state does not change.

Parameter:

- `newsletterId`* — integer (minimum 1): ID of the newsletter to send a test of
- `recipientEmail`* — string (minLength 3; maxLength 250): Address to send the test to; any address, and one that is not a contact yet becomes one
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-newsletter-send` · DO

**Activate newsletter**

Prepares the dispatch of an email newsletter, immediately or at a given moment, and sends, schedules and publishes nothing itself. It checks permission, published content, audience and sender, estimates the recipients and returns a short-lived single-use confirmation URL bound to that exact summary. Only the logged-in user, by opening the URL in KlickTipp and confirming there, hands the newsletter over -- that reaches real recipients and cannot be taken back. Content that was changed but not published is refused; publish it first with email-content-publish. The mode has to be given explicitly; a scheduled moment carries its own UTC offset. If a bound value changes or the URL expires, a new preparation is needed. The dispatch state is read through email-newsletter-get with deliveryStatus.

Parameter:

- `newsletterId`* — integer (minimum 1): ID of the newsletter to send
- `mode`* — string (einer von `immediate`, `scheduled`): "immediate" or "scheduled"; no default
- `scheduledAt` — null | string (Muster `^\d{4}-\d{2}-\d{2}[Tt ]\d{2}:\d{2}(:\d{2})?([Zz]|[+-]\d{2}:?\d{2})$`): Moment to send at, ISO 8601 with UTC offset; required for "scheduled", forbidden for "immediate"
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in
