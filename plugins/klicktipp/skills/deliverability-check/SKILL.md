---
name: "deliverability-check"
description: "Read-only diagnosis of a KlickTipp account's deliverability — inbox placement, bounces, spam-folder issues and what to fix first; for account health checks."
---

# KlickTipp deliverability check

Give the customer an evidence-based diagnosis of the **selected account**: facts, risks, next steps and limits. This skill reads and explains; every change or send belongs to the specialist skill named below. Inbox placement of future emails can never be promised.

## Read

Read only what the question needs; for a general account check read all of it. Keep the same `accountId` on every call.

1. `validate-account-sending-readiness` — report its blocking findings first. It covers technical readiness only, not a complete setup.
2. `list-sender-domains`, then `get-sender-domain` and `get-sender-domain-dns-setup` for the relevant domain. Interpret record status as `dns-setup` defines it, including stored versus live results; always give the date of the stored check.
3. `search-sender-addresses` and `search-signatures` — which sender identity is usable. Judge a signature's readiness as `signatures` defines it.
4. `search-opt-in-processes` — which processes are single opt-in and which is the default.
5. `get-account-settings` — blocklist and the passive-contacts setting, as exposed by the tool.
6. `get-account-statistics`; recent newsletters via `search-newsletters` (status sent) and `get-campaign-statistics`; automation emails: read only active automations that have sent, read each for its email IDs, then `get-automation-email-statistics`, and name in the answer how many automations and emails were read; `search-unsubscription-feedback`. Compute and label every rate exactly as `dashboard` defines it, and show hard bounces, soft bounces, spam bounces and spam complaints as separate counts.
7. For a named draft, let `newsletter` check it. For a split test, ask which variant.

Report counts, never individual contacts. For one contact's bounce or complaint history, hand to `contacts`.

## Rules you may state

Each rule is backed by the account itself or by consistent knowledge-base articles. Link the article in brackets.

- **Account wins:** set the DNS records KlickTipp lists as required. Keep an existing valid DMARC policy even if it differs from KlickTipp's suggestion, and never add a second one. No separate SPF record is required unless the record table lists one.
- A sender address on a freemail domain cannot be used; the customer needs their own domain. [Sender addresses with DKIM, SPF and DMARC]
- A sender without valid DKIM has limited deliverability. [Sender addresses with DKIM, SPF and DMARC]
- A hard bounce excludes the address from future sends. [Global bounce management]
- A manual spam complaint blocks the contact permanently. [Global bounce management]
- Contacts without opens or clicks for more than six months should not be mailed. [Improve email deliverability], [Tag inactive contacts]
- Single opt-in is a deliverability risk. Whether contacts consented is assessed by `opt-in`; never call single opt-in contacts unconsented. [Improve email deliverability]
- Send at a steady volume; after a pause or with a new domain, increase volume gradually. [Mail server best practice]
- The sending domain should have a reachable website with imprint over https. [Mail server best practice]
- Content: no disguised words, no fake "Re:"/"Fwd:" subjects, no hidden text. [Improve email deliverability]

## Report

Answer in the customer's language and form of address; choose the format that fits the question. Keep it short: blockers and the first next step come first, details follow only when they change what the customer should do or when asked. Make sure the answer:

- says early whether the account can send right now;
- keeps what the tools returned apart from your assessment, and ties each risk to a rule above;
- gives the most important next steps, each with who acts and which skill takes over;
- names what the check could not see, such as live DNS, bounce reasons, or placement at a mailbox provider without a placement test;
- does not promise inbox placement.

State an impact only with a number behind it; without one, say what is unknown instead of estimating ("many contacts", "most emails").

Put every rate in context: how many emails it is based on and which period it covers. Draw conclusions from the volume actually sent, and say so when the base is too small to be meaningful, for example test sends to a handful of recipients.

## Hand over, never run unasked

| Action | Owner |
|---|---|
| DNS edits, requesting a new DNS check | `dns-setup` |
| Creating a sender address or signature | `account-setup`, `signatures` |
| Test send, publishing or checking one newsletter | `newsletter` |
| Excluding inactive contacts from a send | `newsletter`; building the segment: `tags` |
| Reactivation campaign | `automation` |
| Consent scope of a sign-up | `opt-in` |
| Switching an opt-in process mode | `opt-in` |
| Passive-contact tag, blocklist, other account settings | `account-setup` |

**Gmail placement test** (owned by this skill): `send-email-for-gmail-placement-preview` sends a real email to a Gmail seed inbox. Before offering it, confirm in the live tool contract which email types it accepts. Run it only after an explicit yes, then read `get-email-gmail-placement-preview-result`. The result covers this one email at Gmail only.

## Stop

- If the account cannot be read (authentication, account selection, MCP access), explain the returned reason and hand to `account-setup`.
- If a tool returns an error, report what was returned instead of guessing.
- If statuses contradict each other (for example a domain "checked but not verified" while its records show no check date), do not repeat both. State the stored result once with its date, say the status is unclear, and name the step that would clarify it.

## Done

The customer knows whether the account can send, what to fix first and what remains unknown; every fact traces to a tool result or a linked article, and nothing was changed or sent without approval.

## Knowledge-base articles

- [Global bounce management](https://www.klicktipp.com/de/support/wissensdatenbank/globales-bounce-management/)
- [Mail server best practice](https://www.klicktipp.com/de/support/wissensdatenbank/best-practice-guide-fuer-deinen-klicktipp-mailserver-nutzen/)
- [Improve email deliverability](https://www.klicktipp.com/support/knowledge-base/improve-email-deliverability/)
- [Sender addresses with DKIM, SPF and DMARC](https://www.klicktipp.com/support/knowledge-base/create-sending-addresses-dkim-spf-dmarc/)
- [Tag inactive contacts](https://www.klicktipp.com/support/knowledge-base/tag-inactive-contacts/)