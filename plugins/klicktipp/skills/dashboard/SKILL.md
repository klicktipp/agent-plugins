---
name: dashboard
description: Build read-only KlickTipp dashboards and explain account activity, top tags, newsletter performance, and differences between statistics and contact counts.
---

# KlickTipp dashboard

Read the relevant measurements first. Keep their units, time windows and denominators visible. Answer numeric questions directly; create a page only when the user asks for a visual dashboard.

## Choose the source

| Question | Read |
| --- | --- |
| Analytics account overview | `get-account-statistics` |
| One newsletter or follow-up campaign | `get-campaign-statistics` |
| One newsletter's dispatch snapshot or audience estimate | `get-newsletter` with `deliveryStatus` or `audienceReach` |
| Newsletter inventory or recent sends outside the account overview | `search-newsletters`, then relevant details |
| A tag's current contact count and meaning | `get-tag` |
| Contact channels matching a manual tag | `search-contacts` |
| Current tag carriers grouped by last tagging date | `get-tag-statistics` |
| A saved statistics report | `get-statistics-report` |

The published contracts of the statistics tools, word for word, are in [references/contracts.md](references/contracts.md).

Use the same account and connector for comparisons. Record the retrieval time when a response has no server measurement timestamp. Paginate searches before calling the returned set complete. Missing fields are unavailable, never zero.

## Account overview

`get-account-statistics.days` (1–90) filters only daily `activity`. It does **not** filter `topTags`, `recentCampaigns`, `ispShares` or `bounces`.

- The daily chart's **Eintragungen**, **Austragungen** and **SMS Eintragungen** are `activity.subscriptions`, `unsubscriptions` and `smsSubscriptions`. They count daily events, not a running contact balance or necessarily distinct people. `imports` is separate and can rise for the same operation as `subscriptions`; do not add them as separate contacts. Check aggregates against the daily rows.
- **Top 5 Tags** selects the tags most frequently assigned during the last three days. This is a recent tagging trend, not a ranking by overall current size. Preserve the returned order. `addedToday`, `addedYesterday` and `addedDayBefore` are recent additions. A dated UI column can show a balance with an arrow for that day's change; do not mistake that balance for the `added...` value.
- `topTags.contacts` is the overview's displayed total. It can count digital IDs: one contact with two email IDs can appear twice. `get-tag.contactCount` counts contacts. When they differ, report both units and, if needed, inspect the filtered contact list. A search can return multiple channel rows for one contact or omit a contact with no returned channel.
- **Aktuelle Newsletter** shows the most recently sent newsletters. Its columns map to `recentCampaigns.sent`, `opensUnique`, `openRate`, `clicksUnique` and `clickRate`. Opened and clicked are **unique recipients**; other newsletter views can show repeat opens and clicks as totals. The dashboard's `clickRate` is unique clickers per **unique opener**; `openRate` is unique openers per sent email. Use the supplied percentages and label their denominators. `days` does not restrict this list.
- ISP and bounce percentages each use the sum of their **own categories** as denominator. Their totals need not agree and neither establishes the account's total contacts. Account bounce categories are not campaign bounce rates. Zero bounce events in the selected daily window do not date or explain an existing bounce classification.

The account overview does not provide an account-wide contact total. A newsletter's `audienceReach` estimates recipients for **that newsletter** under its audience and sending rules; it is not the account population.

## Distinguish statistics

State each number's unit, filters and time window before comparing it with another. `get-tag-statistics` counts only **current tag carriers**, grouped by their **last tagging** in the requested period. It is not a complete tagging event history: removals and overwritten earlier tagging times can disappear. A zero recent value does not prove no assignment or removal happened. Do not use it to reconstruct Top 5 selection or missing `added...` fields of an excluded tag. This plugin has no tool for one contact's tagging history; say so instead of inferring it.

Tag holders, digital IDs, contact-channel search rows, daily list events, newsletter recipients and historical tagging events are different units. Do not reconcile a difference by treating them as the same count. A `subscribed` channel is not a delivery guarantee.

## Newsletter rates

For one campaign, `get-campaign-statistics` supplies `openRate` per send, `clickRate` per unique opener and `clickRateOfRecipients` per send. It separates `opensUnique` from `opensTotal` and `clicksUnique` from `clicksTotal`. Use those supplied rates. SMS has no open metric; its open-related fields may be null.

For a newsletter's `deliveryStatus`, calculate only rates supported by the returned counters:

| Metric | Calculation |
| --- | --- |
| Delivery | `sentCount / estimatedRecipients` (the estimate precedes sending) |
| Open | `uniqueOpenCount / sentCount` |
| Recipient click | `uniqueClickCount / sentCount` |
| Click-to-open | `uniqueClickCount / uniqueOpenCount` |
| Bounce | `(hardBounceCount + softBounceCount) / sentCount`; show types separately |
| Unsubscribe | `unsubscriptionCount / sentCount` |
| Complaint | `spamComplaintCount / sentCount`; show the count too |

When a denominator is zero or absent, show the rate as unavailable rather than zero. Treat open tracking as an imperfect signal and avoid deliverability or trend conclusions from tiny samples. `search-newsletters.count` is a page count; follow `nextCursor` with unchanged filters before reporting a complete inventory. Drafts have no send date. Email newsletter search does not cover SMS newsletters or follow-ups.

## Present the result

For a numeric question, give the measured figures, source, retrieval time, window and relevant limits. For a visual dashboard, create one self-contained page and read [references/craft.md](references/craft.md) first. Keep the underlying values in a small structured object so the display can be checked. Label a send's observation time separately from the account activity window; never imply every overview block shares `days`. Link campaign rows through returned app URLs where available. Show absolute counts beside percentages.

This skill is read-only. Do not create contacts, assign tags, change campaigns or send messages as part of making a dashboard.
