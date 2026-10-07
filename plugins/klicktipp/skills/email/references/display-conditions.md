# Dynamic content: a row for part of the recipients only

In the editor it is called *Dynamic content → Display condition*, in the tools a **decision**
(`decision`). A row bound to one appears only for the contacts that satisfy the condition — for
everyone else it drops out of the dispatch entirely.

**The most important thing first, because it is the error nobody sees:** a condition that matches
nobody is not an error. The newsletter goes out, nothing is reported, and the row is missing for
*everyone*. That is exactly how a test tag from an old session stayed on the main row of a draft and
would have made the core message invisible. So before sending, check with `list-email-editor-display-conditions` which
rows are bound — and whether the condition matches anybody at all.

## Contents

- The procedure
- What makes up a condition
- The time frames
- The catalogue of condition types
- A complete example
- When a row does not appear

## The procedure

1. **`get-email-editor-display-condition-capabilities`** — without arguments, the catalogue of condition types; with
   `conditionTypes`, additionally for those types: the permitted comparisons, the entities *of this
   account* (tags, automations, emails …) and the time frames. At most five types per call; the
   entity list is capped at 200, and `entityCount` says how many there really are.
2. **`update-email-editor-display-condition`** — create the named condition. You state only the choice; operator,
   seconds and the smart-tag field are derived from it. The response contains the `decisionId`.
3. **`configure-email-editor-row-display-condition`** — bind the row, addressed by the `uuid` from `contentOutline`.
   `decisionId: null` releases the binding again.
4. **`list-email-editor-display-conditions`** — what the email carries and which rows each condition controls. The
   binding sits as a marker *inside* the row and appears in no other projection; this is the only way
   to see it.

A condition with no bound row controls nothing and is discarded the next time the editor saves. One
condition can control several rows.

## What makes up a condition

You choose four things, everything else follows:

| Field | what it is | from |
| --- | --- | --- |
| `conditionType` | **what** is checked | catalogue below, class name |
| `condition` | **how** it is compared | `has`, `has-not`, `has-any`, `has-not-any` |
| `entity` | **which** entity — only for `has` and `has-not` | this account's capabilities |
| `timeframe` | **when** — default `anytime` | fixed list below |
| `action` | which event of the entity counts | per type, see catalogue |

`has` and `has-not` need an `entity`; `has-any` and `has-not-any` ask "any entity of this kind" and
take none. An `entity` that does not belong to the account is **rejected**, not stored.

**Segments and how they join.** `segments` is a list; within a segment `conditionsOpAND` joins the
conditions, between segments `segmentsOpAND` (both default to `true`). A contact sees the row when
the tree as a whole is satisfied.

## The time frames

A fixed list, the same for every type: `anytime`, `24h`, `3d`, `30d`, `90d`, `1y`. They count back
from the moment of dispatch.

## The catalogue of condition types

All 22 types with their actions. The comparisons are `has`, `has-not`, `has-any`, `has-not-any`
everywhere — with **one** exception, marked below. `conditionType` is the full class name, so
`App\Klicktipp\Tag` and not `Tag`.

| `conditionType` (without `App\Klicktipp\`) | in the editor | `action` |
| --- | --- | --- |
| `Tag` | Manual tag | `received` |
| `TagCategorySmartLink` | SmartLink | `clicked` |
| `CampaignsProcessFlow` | Automation | `started`, `finished` |
| `EmailsAutomationEmail` | Emails (automation) | `sent`, `opened`, `clicked`, `viewed` |
| `EmailsAutomationSMS` | SMS (automation) | `sent`, `clicked` |
| `CampaignsNewsletter` | Newsletter/autoresponder | `sent`, `opened`, `clicked`, `viewed`, `converted` |
| `Requests` | Sign-up by email | `subscribed` |
| `SMSListbuildings` | Sign-up by SMS | `subscribed` |
| `APIKey` | API key | `subscribed` |
| `BusinessCardReader` | Business card scanner | `subscribed` |
| `Event` | Business card scanner event | `subscribed` |
| `SubscriptionFormsCustom` | Sign-up form | `subscribed` |
| `LandingPage\LandingPage` | Landing page | `subscribed` |
| `PaymentIPNs` | Product | `bought` |
| `PaymentRefund` | Refund | `refunded` |
| `PaymentChargeback` | Chargeback | `chargedback` |
| `PaymentSubsequent` | Subsequent payment | `bought subsequently` |
| `PaymentDeferred` | Deferred payment | `bought deferred` |
| `PaymentRebill` | Subscription | `canceled`, `resumed` |
| `PaymentRebillStatus` | Subscription status | `completed`, `expired` — **only `has` and `has-any`** |
| `PaymentAffiliation` | Digistore affiliate | `affiliated` |
| `ToolOutbound` | Outbound | `triggered` |

The action decides *which* event counts: for a newsletter `sent` is something other than `clicked`,
and both are permitted conditions on the same email. Omitting `action` takes the first of the list.

Do not rely on this table alone when it matters: which types an account can actually offer, and which
entities it has for them, is answered by `get-email-editor-display-condition-capabilities` — the table here says
what you can ask for.

## A complete example

"This row only to contacts carrying the tag *Kunde*":

```json
// 1. get-email-editor-display-condition-capabilities  { "conditionTypes": ["App\\Klicktipp\\Tag"] }
//    -> entities: [{ "entity": 499, "label": "Kunde", "actionFields": { "received": 499 } }, ...]

// 2. update-email-editor-display-condition
{
  "editorUrl": "…",
  "contentRevision": "…",
  "name": "Customers only",
  "segments": [
    {
      "conditionsOpAND": true,
      "conditions": [
        { "conditionType": "App\\Klicktipp\\Tag", "condition": "has", "entity": 499 }
      ]
    }
  ]
}
//    -> decisionId "1"

// 3. configure-email-editor-row-display-condition
{ "editorUrl": "…", "contentRevision": "…", "rowUuid": "a4fac5c0-…", "decisionId": "1" }
```

Both write calls are bound to the `contentRevision` and store the draft; publishing still happens
through `publish-newsletter-email-content`.

## When a row does not appear

The usual case is not broken but empty: the condition matches nobody.

1. `list-email-editor-display-conditions` — which condition controls this row, and what does its tree look like?
2. Check the `entity` in the condition against the account: does anybody carry that tag at all? A tag
   from a test typically carries **zero** contacts.
3. Either rewrite it onto a sensible entity with `update-email-editor-display-condition` and the same `decisionId` —
   the binding stays — or make the row visible to everyone again with `configure-email-editor-row-display-condition` and
   `decisionId: null`.
