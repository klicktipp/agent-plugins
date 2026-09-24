# Die veröffentlichten Verträge — Newsletter und Versand

Wort für Wort das, was der Server in `tools/list` für die 9 Werkzeuge dieses Skills
ausliefert: Beschreibung, Annotationen, jeder Parameter mit Typ, Grenzen und Beschreibung. Ein `*`
markiert Pflichtparameter. `R` liest nur · `D` löscht oder ersetzt ohne Undo · `O` erreicht etwas
außerhalb des Kontos · `I` ein zweiter gleicher Aufruf ändert nichts mehr.

Stand 2026-09-18. Diese Datei spiegelt den Server, sie interpretiert ihn nicht: ändert sich eine
Werkzeugbeschreibung, wird sie hier wörtlich nachgezogen. Wofür ein Werkzeug da ist, was es nicht
tut und woran man sich stößt, steht in [tools.md](tools.md).

## Inhalt

`email-newsletter-search` · `email-newsletter-get` · `email-newsletter-draft-create` ·
`email-newsletter-draft-update` · `email-newsletter-draft-delete` ·
`email-newsletter-delivery-configure` · `email-newsletter-test-send` · `email-newsletter-send` ·
`email-newsletter-cancel`

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

## `email-newsletter-cancel` · D

**Cancel a newsletter dispatch**

Takes back the dispatch of an email newsletter that was scheduled or has just started, so it becomes a draft again and reaches nobody further. THIS IS THE ANSWER TO "stop it", "cancel the send" AND "undo the schedule". Only while the delivery status says canBeCancelled: once a dispatch is far enough along it cannot be called off, and the refusal says so rather than pretending. What already went out stays out -- this stops what has not been sent yet, it does not recall mail. The newsletter itself, its content and its audience are untouched; only the dispatch is undone, and activating it again is email-newsletter-send. Ask the person before calling this: a dispatch someone set up deliberately is not yours to stop on your own reading of a situation.

Parameter:

- `newsletterId`* — integer (minimum 1): ID of the newsletter whose dispatch is to be called off
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in
