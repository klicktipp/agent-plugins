---
name: "automation"
description: "Build, change and check the automations (process flows, marketing cockpit) of a KlickTipp account — entry condition, emails, SMS, waits, decisions, tags, goals, jumps — or start one from a ready-made campaign template (Business Automation Masterclass catalogue, or a shared template link). Use it as soon as a flow, a multi-step campaign, a welcome series, a webinar or dated campaign, a campaign template, or \"what happens after X\" is involved — and especially when you were about to say that some part of it only works in the editor."
---

# KlickTipp automations

Every step of an automation has a tool — start, email, SMS, wait, decision, tag, goal, jump,
notification, split test, exit. If one is missing, it is missing from your connection, not from the
platform. Never point at "that only works in the editor".

The tool descriptions come from a template and barely distinguish the action types. Choose by
[references/actions.md](references/actions.md), not by description.

Before designing or materially rewriting customer-facing email, SMS or notification copy, use `company-context` and pass its confirmed snapshot or task-only context to the message owner. Do not run the gate for graph inspection, waits, conditions, tags, goals or movement of existing approved messages. `email` continues to own email content; this skill owns the automation graph.

## Start from a template when one fits

Before building a flow step by step, check whether a ready-made one exists:
`search-automation-templates` with the user's goal ("Termin nachfassen", "Bewertungen sammeln",
"Geburtstag"). The catalogue holds the automations of the Business Automation Masterclass —
appointments, offers, reviews, onboarding, events, sales funnels — with their emails. A user who
pastes a link `…/template/…` means a shared template; it goes through the same tools.

Find → `get-automation-template` → settle name and mappings with the user →
`import-automation-template` → finish with the tools below. The import creates the automation
**paused** and sends nothing. Procedure, arguments and what the answer means:
[references/templates.md](references/templates.md).

## Best practices — the default, not an option

Check before the first action. BP‑1/BP‑2 outrank the user's literal wording; say in one sentence
that you deviated. BP‑3/BP‑4 you build in without asking.

| | When | instead of | do | because |
|---|---|---|---|---|
| **BP‑1** | waiting for a reaction (clicked, opened, bought) | wait → decision | **goal**, wait only as the upper bound | whoever clicks at once lies idle for 2 days |
| **BP‑2** | a fixed date (webinar, launch, course start) | "wait 6 days" | **date field** as the anchor of every wait | late entrants get everything too late |
| **BP‑3** | entry shortly before the date | let reminders run | **gate** before each reminder | past moments fire immediately |
| **BP‑4** | a branch hanging on "opened"/"clicked" | build it silently | build it **and** state the bot caveat | providers open and click by themselves |

## Model

A graph of actions with fixed IDs. Each new action attaches to an existing one: `afterActionId`
says to what, `branch` says where — `next` after ordinary actions, `yes`/`no` only at decisions.

- **`revision`** from the last `get-automation` belongs in every write. Rejected = someone changed
  the graph; read again, retry.
- **Only inactive automations are writable.** Stop a running one with `stop-automation` — ask first.
- **`dryRun: true`** computes without storing. Always use it when the attachment point is unclear.

## Order

0. Is there a template for it? See *Start from a template* above.
1. Hold the flow against the best practices.
2. `create-automation-draft` — creates the draft **including** the start action. Do not create the
   start action yourself; configure it with `update-automation-start-action`.
3. **Message before action.** `create-automation-email-draft`, `create-automation-sms-draft`,
   `create-notification-email-draft` or `create-notification-sms-draft`, set the content, then
   `add-automation-email-action` / `add-automation-sms-action` with its ID.
4. `get-automation` — graph, action IDs, `revision`.
5. Attach actions in flow order. Every response carries the revision for the next step.
6. `validate-automation`. If it reports an unpublished email, say that the email must be published in the
   KlickTipp editor before activation.
7. `prepare-automation-activation` — **does not activate**, it returns the dialog. A human confirms
   the start. Never report an activation that did not happen.

## BP‑1 · Waiting for a reaction is a goal, not a wait

"Email, wait 2 days, then check whether they clicked" leaves whoever clicks after 5 minutes lying
there for 2 days.

A goal (`add-automation-goal-action`) is evaluated **wherever the contact currently stands** —
including mid-wait — and pulls them straight past it.

> Email → **goal "has clicked"** → tag, SMS, …
> alongside it the wait as an upper bound → branch for everyone who did not react

"Wait 2 days and then check" almost always means "as soon as, at the latest after 2 days". Keep a
fixed wait only when it is explicitly wanted (a deadline, an embargo).

- A goal acts across the **whole** automation, not at its position.
- **Only the first goal reached counts per run.** Several goals are alternatives, not stations.
- A goal **with nothing attached after it does nothing**; `validate-automation` reports it.
- A goal is a node **and** a global condition. Check the attachment point with `dryRun`, then read
  `get-automation`.

## BP‑4 · Opens and clicks can be machines

Providers and security scanners load images and prefetch links (Gmail routinely) → "opened" and
"clicked" without a human. With images off, a real open does not count.

A click is the stronger signal, not proof. Before a branch that does something visible (SMS, sales
email, discount): state the caveat. Machine-proof are only a reply, a form, a purchase.

## BP‑2 · Dated campaigns anchor on the date

`days` counts from the moment **this** contact reaches the action. Someone entering 5 days later
waits another 6. Invisible in the draft, surfaces only in production.

1. Behind the start action, `add-automation-set-field-action`: date **and time** into a date/time
   field. Operator from `get-automation-editor-capabilities`, field ID from
   `search-automation-editor-references`.
2. Every wait via `delayField`; `delayTime` **negative = before** the date:

   | target | settings |
   |---|---|
   | 24 h before | `{"delayType": "customfield hours", "delayTime": -24, "delayField": "<field>"}` |
   | 1 h before | `{"delayType": "customfield hours", "delayTime": -1, "delayField": "<field>"}` |
   | at the date | `{"delayType": "from field", "delayField": "<field>"}` |
   | the day after | `{"delayType": "customfield days", "delayTime": 1, "delayField": "<field>"}` |

3. Attach decisions and jumps to the same axis.
4. **Clear the field at the end** — otherwise the contact carries the date into every further run
   and into every automation reading the same field.

**Ask first:** date, time, whether it recurs. Without the time there is no "one hour before", and a
date-only field moves every reminder to midnight.

Without a fixed date (welcome series, follow-up sequence) ordinary waits are correct.

## BP‑3 · Late entrants and empty fields

**Past moments do not wait, they are due.** Signing up 1 h before the webinar runs through "24 h
before", "12 h before", "1 h before" without pausing → three reminders at once.

- **Gate before each reminder:** decision with `is after`, `field` = the date field, `value`
  relative (`+24 hours`, `+1 hour`). The no-branch jumps past it with
  `add-automation-go-to-action` to the next action still in the future.
- **Signing up after the date** is split off right behind setting the field → recording, next date
  or exit.
- **An empty date field means no wait at all**, for every following one too. Two weeks become
  seconds. Check once at the start with `is not empty`.

## Conditions and IDs

Guess neither IDs nor operators.

- `get-automation-editor-capabilities` — permitted action types, settings schema, required fields,
  condition operators, plugin conditions.
- `search-automation-editor-references` — name → ID for emails, SMS, tags, fields, signatures, calendars,
  outbounds, Facebook audiences, automations, segments.

**Opens and clicks are tags.** "Has opened email 1" runs through the message's smart tag from
`get-automation-email` / `get-notification-email`. That ID goes into `field` — not the email ID.

## Traps

| | |
|---|---|
| `emailID` for SMS | it is called `emailID` there too but means the ID of an **SMS** draft. Same for both notification actions. |
| empty decision branch | allowed. Attaching nothing is a finished flow. |
| `delete-automation-action` | needs `keep_yes`, `keep_no` or `subtree` at a decision, otherwise `keep_next` or `subtree`. |
| `move-automation-action` | `subtree` moves the following graph along; a decision with filled branches only as a subtree. |
| `copy-automation-action` | new action ID, **same** message. Editing the copy's text hits the original — copy it first with `copy-automation-email` / `copy-automation-sms` (`copy-notification-email` / `copy-notification-sms` for a notification). |
| `add-automation-go-to-action` | jumps to an action **ID** from `get-automation`, not to a name. |

## Boundaries

Email **content** (HTML, blocks, styling) → `email`. Single sends → `newsletter`. Contacts → `contacts`,
tags → `tags`, fields as such → `custom-fields`.

## Before you write

Building itself reaches nobody (the draft is inactive), and neither does importing a template —
the imported automation is paused. It does create objects in the account that stay there, so
settle name and mappings before the import, not after. `stop-automation` and
`move-automation-contacts` intervene in live operation: **say what will happen, get consent,
then call.**

A test send is a real email or SMS: an address that is not yet a contact becomes one and gets
tagged, which can start automations. Say so before sending, and send only to an address the user
names.