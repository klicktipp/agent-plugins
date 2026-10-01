# Die veröffentlichten Verträge — Statistik

Wort für Wort das, was der Server in `tools/list` für die 7 Werkzeuge dieses Skills
ausliefert: Beschreibung, Annotationen, jeder Parameter mit Typ, Grenzen und Beschreibung. Ein `*`
markiert Pflichtparameter. `R` liest nur · `D` löscht oder ersetzt ohne Undo · `O` erreicht etwas
außerhalb des Kontos · `I` ein zweiter gleicher Aufruf ändert nichts mehr.

Diese Datei spiegelt den Server, sie interpretiert ihn nicht: ändert sich eine
Werkzeugbeschreibung, wird sie hier wörtlich nachgezogen. Wie die Zahlen zu lesen und zu rechnen
sind, steht in [../SKILL.md](../SKILL.md). Die Auswertung eines Splittests,
`get-newsletter-split-test-statistics`, steht beim Skill `splittest`.

## Inhalt

`get-account-statistics` · `get-campaign-statistics` · `get-tag-statistics` ·
`get-automation-statistics` · `get-automation-waiting-contact-counts` ·
`get-automation-email-statistics` · `get-automation-sms-statistics`

## `get-account-statistics` · RI

**Read account statistics**

Reads how one KlickTipp account is doing -- the five blocks of its dashboard in one call. recentCampaigns: the last ten mailings with what they achieved, including the same open and click rates get-campaign-statistics reports. topTags: the tags that gained the most contacts today, with their totals. activity: one entry per day with subscriptions, unsubscriptions, SMS subscriptions, imports, the three bounce kinds and spam complaints -- no sends, opens or clicks, which are only counted per campaign. ispShares: which mail providers the contacts are at. bounces: how many contacts are bouncing, by kind. An SMS campaign reports opensUnique and openRate as null -- it has no opens to count. For one campaign in detail use get-campaign-statistics.

Parameter:

- `days` — integer (minimum 1; maximum 90): How many days of daily activity to return, 1 through 90; the other blocks are unaffected
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `get-campaign-statistics` · RI

**Read campaign statistics**

Reads what one campaign achieved -- an email or SMS newsletter, or any autoresponder (subscription, date field or birthday) in either channel: recipients, sent and failed, opens and clicks each as a total and as unique contacts, browser views, conversions, unsubscriptions, the three bounce kinds and spam complaints, plus every tracked link with its clicks, most-clicked first. Three rates come as the KlickTipp dashboard computes them: openRate over what was SENT, clickRate over what was OPENED (the share of readers who clicked), clickRateOfRecipients over the sends. Do not divide the counters yourself. An SMS campaign has no opens, so opensTotal, opensUnique, openRate, clickRate and browser views are null -- use clickRateOfRecipients. Totals are lifetime and not restricted to a period. A campaign that has not gone out answers with zeroes. For an automation use get-automation-statistics.

Parameter:

- `campaignId`* — integer (minimum 1): ID of the campaign whose statistics are read
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `get-tag-statistics` · RI

**Read tag statistics over time**

Reads how many contacts were tagged with each of up to ten tags, per hour, day, month or year within a period. This is the only statistics tool that answers about a period: the others report lifetime totals. It counts the contacts that carry the tag now, each in the period they last got it. A tag that was removed again is not counted anywhere, and a contact tagged a second time moves to the period of the latest tagging. The statistics report in the app counts the same way. So this is not a log of every tagging that ever happened; for the full history of one contact use get-contact-history. A period in which nothing happened is left out rather than reported as zero, so absence means no taggings. Works with any tag the account has, manual or automatic. Refuses a request whose answer would carry more than 2000 periods: narrow the period or ask for a coarser granularity.

Parameter:

- `tagIds`* — array<integer> (minItems 1; maxItems 10; uniqueItems): IDs of the tags to count, one to ten; from search-tags or get-tag
- `granularity` — string (einer von `hour`, `day`, `month`, `year`): Period each count covers: hour, day, month or year
- `from` — null | integer (minimum 0): Unix timestamp the period begins at; omit for the first tagging there is
- `to` — null | integer (minimum 0): Unix timestamp the period ends at; omit for now
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `get-automation-statistics` · RI

**Read automation statistics**

Reads how many contacts started and finished one automation, are active in it, ended on an open, wait for a queue job or failed -- lifetime totals, not restricted to a period -- and, when the account has conversion statistics, how many finished or reached a goal between from and to and how many of them reached each goal action. Only automations: a newsletter or autoresponder ID is refused, read those with get-campaign-statistics. Reads only.

Parameter:

- `automationId`* — integer (minimum 1): ID of the automation; a newsletter or autoresponder ID is refused
- `from` — null | integer (minimum 0): Unix timestamp where the conversion period begins; omit for the beginning of the automation
- `to` — null | integer (minimum 0): Unix timestamp where the conversion period ends; omit for now
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `get-automation-waiting-contact-counts` · RI

**Read waiting contact counts**

Reads how many contacts are waiting at which action of one automation right now, with the action ID, type and name, most contacts first; an action nobody waits at is not listed. The counts are an observation, not a completion receipt for a queued move. Only automations: a newsletter or autoresponder ID is refused. Reads only.

Parameter:

- `automationId`* — integer (minimum 1): ID of the automation; a newsletter or autoresponder ID is refused
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `get-automation-email-statistics` · RI

**Read automation email statistics**

Reads what one campaign (automation) or notification email achieved: how many contacts it was sent to, opened and clicked, bounces and spam complaints, and the tracked links with their clicks, most-clicked first -- the numbers of its statistics screen, linked as statisticsUrl. Counters are lifetime totals across every use of the email and are not restricted to a period. A campaign email nothing has been sent of answers with zeroes. A notification email records no sends, opens or link clicks, so sent, opened and clicked are null and links is empty for it; only bounces and complaints are counted. The ID is the email ID from get-automation-email or get-notification-email. For an automation SMS use get-automation-sms-statistics, for a newsletter get-campaign-statistics.

Parameter:

- `emailId`* — integer (minimum 1): ID of the campaign or notification email whose statistics are read; this is not an automation action ID
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `get-automation-sms-statistics` · RI

**Read automation SMS statistics**

Reads what one automation SMS achieved: how many contacts it was sent to, how many clicked and how many did not, bounces, and every tracked link with its clicks, most-clicked first. An SMS has no opens -- nothing in a text message can report being read -- so there is no open rate and no clickRate over the opens; clickRateOfRecipients is the share of recipients who clicked, the same field get-campaign-statistics reports. Counters are lifetime totals across every use of the SMS and are not restricted to a period. An SMS nothing has been sent yet answers with zeroes rather than an error, and reports no bounces while it has no sends, exactly as the statistics screen does. The ID is the SMS ID from get-automation-sms, not an automation action ID.

Parameter:

- `smsId`* — integer (minimum 1): ID of the automation SMS whose statistics are read; this is not an automation action ID
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

