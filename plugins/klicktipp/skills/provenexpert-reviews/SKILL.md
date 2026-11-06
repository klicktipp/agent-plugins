---
name: provenexpert-reviews
description: Sets up a KlickTipp review campaign for ProvenExpert through the native integration — personalised survey link after a purchase, reminder until the contact has rated, thank-you mail for 4 or 5 stars, improvement mail for other ratings, optionally Google review mails for Gmail contacts — by connecting ProvenExpert as a marketing tool, syncing a ProvenExpert survey, importing the ProvenExpert campaign template and wiring it to the survey's smart tags. Use when the user mentions ProvenExpert together with KlickTipp, wants to collect ratings or feedback after a purchase, service or project, or asks why ProvenExpert ratings do not arrive in KlickTipp, even if they only say "I use ProvenExpert and want reviews after a sale".
prerequisites: "A ProvenExpert account (any plan), a KlickTipp account the plugin is signed in to, a double opt-in process, and a purchase tag set by a shop, payment provider or another campaign"
---

# ProvenExpert review campaign

One ProvenExpert survey = one campaign. Each survey gets its own import with its own prefix. The
Masterclass review templates (BK 1–4+, SKB, NLA) only send a portal link and never learn the
rating — do not offer them for ProvenExpert.

```
purchase tag ─(automatic tag assignment)→ action tag → campaign → mail with survey link
→ ProvenExpert survey → smart tags "betreten" / "bewertet" / "mit 4 oder 5 Sternen bewertet"
→ goal "bewertet" pulls the contact to thank-you or improvement mail

Gmail/Googlemail address (optional branch) → request + reminder with the Google review link
→ a click counts as done (Google reports no rating back)
```

Needed: ProvenExpert account, KlickTipp plugin signed in, the browser extension if you are to make
the ProvenExpert changes yourself.

Build on the `automation` skill for the campaign mechanics and on `email` for mail content. This
skill adds the order, the template and what is specific to ProvenExpert. The click paths live in
the KlickTipp knowledge-base article and the ProvenExpert help; read them when you guide the user,
do not copy them.

## Ground rules

- Talk to the user in their language; quoted UI labels ("KlickTipp Sync", "Neues Marketing Tool")
  stay verbatim.
- Ask before you build (Questions first).
- **ProvenExpert first.** Smart tags, the survey-link placeholder and the rating placeholder only
  exist in KlickTipp after a survey has been synced. Never import or wire the campaign before step 3
  of Order succeeded.
- Changes in ProvenExpert or KlickTipp: list them first (screen/object, field, old → new), one "ok",
  then apply and read back. With the browser extension you make the ProvenExpert changes yourself;
  without it, guide one screen at a time.
- The user signs in and authorises the connection; never type passwords.
- Nothing goes live without the user; activation via `prepare-automation-activation`.
- Copy belongs to the user; you set links, placeholders and the survey, not the wording.

## Questions first

| # | Question | Default | Why it matters |
|---|---|---|---|
| 1 | Which tag(s) mark the purchase (shop, payment provider, campaign)? May I add the action tag as "Automatische Tag-Vergabe" to them? | yes, on every purchase tag of this product | The campaign starts on the action tag and removes it; the purchase tag alone starts nothing and must never be removed. |
| 2 | Which product or service is rated? New survey or an existing one? | new survey named after the product | A person can rate each survey only once; different products need different surveys. |
| 3 | Name and prefix of the campaign | "<Produkt> Bewertung" | Keeps tags and mails of each survey apart. |
| 4 | Is the browser extension connected, may I make the ProvenExpert changes? | ask | Decides between doing and guiding. |
| 5 | Should someone on your team get a copy of the improvement mail (address in BCC)? | no | Lets the team follow up on a low rating. Ask it in these words; if the answer is no, say nothing more about it. |
| 6 | Do you have a Google business profile? If yes, its review link ("Rezensionen anfordern"). | ask | Contacts with a Gmail/Googlemail address get the Google mails instead. Without a link, remove the Google branch ([references/klicktipp-adapt.md](references/klicktipp-adapt.md) § Adapt 4). |

## Order

```
- [ ] 1 Connection  - [ ] 2 Survey + sync  - [ ] 3 Check smart tags  - [ ] 4 Import
- [ ] 5 Wire + validate  - [ ] 6 Activate + test  - [ ] 7 Notes
```

1. **Connection** — existing ProvenExpert smart tags only show that a connection existed once.
   Tell the user that step 3 is the real proof; if there are none at all, the user connects it
   ([references/provenexpert-setup.md](references/provenexpert-setup.md) § Connection).
2. **Survey + sync** — create (or pick) the survey in ProvenExpert and run "KlickTipp Sync"
   ([references/provenexpert-setup.md](references/provenexpert-setup.md) § Survey).
3. **Check** — `search-tags` with the survey name returns three smart tags;
   `search-email-editor-placeholders` returns its link and rating placeholder. Note the ids. This
   proves the connection points to this account. If nothing arrives within a few minutes, go to
   § Sync does not arrive in the same reference.
4. **Import** the template as a copy with the agreed name and prefix
   ([references/klicktipp-adapt.md](references/klicktipp-adapt.md) § Import).
5. **Wire** start condition, decisions, goal and mails, publish the mails, `validate-automation`
   ([references/klicktipp-adapt.md](references/klicktipp-adapt.md) § Adapt), then the bridge
   from the purchase tag to the action tag (same reference, § Bridge).
6. **Activate** — hand the user the activation link from `prepare-automation-activation` (always
   part of your hand-over, even when the user activates later), then test
   ([references/tests.md](references/tests.md)).
7. **Notes** — ≤ 1000 characters, only while paused.

## Alignment rules (ProvenExpert ↔ campaign)

1. Decision operators: `plugin is started` = "betreten", `plugin is finished` = "bewertet",
   `plugin is in progress` = "mit 4 oder 5 Sternen bewertet"; field = the smart-tag id from step 3.
2. "betreten" only chooses the reminder timing; everything that stops mails uses **"bewertet"**.
3. "Not yet rated" belongs in the **start condition**. The goal "bewertet" acts everywhere in the
   campaign, also at a restart action, so a rated contact must never sit in it.
4. After a rating the contact **leaves** the campaign (exit), never restarts: a survey can be rated
   once per email address. Restart only where nobody rated, so a later purchase asks again.
5. One survey, one campaign: start condition, every decision, the goal and both placeholders point
   to the same survey id.
6. The purchase tag stays; only the action tag is set and removed.

## What the campaign does (for explaining it to the user)

- Purchase → action tag → campaign starts only if this survey is not rated yet.
- 1 day later the request with the personal survey link.
- The moment the contact rates — even in the middle of a wait — the goal takes over: 5 minutes,
  then 4–5 stars → thank-you mail, any other rating → improvement mail, then the contact leaves.
- No rating after 1 day: opened the survey but did not submit → reminder at once; never opened →
  reminder one day later. Still nothing 3 days later → end without further mail.
- A later purchase asks again only if the contact has not rated.
- Google branch (Gmail/Googlemail addresses only): 1 day after the purchase the Google request;
  no click after 2 days → reminder; 3 days later end. A click on the Google link ends it, also on
  a later purchase. No thank-you or improvement mail here: Google reports no rating to KlickTipp.

## Known behaviour worth telling the user

- ProvenExpert shows no result for "KlickTipp Sync"; success is visible only in KlickTipp.
- One ProvenExpert account is connected to one KlickTipp account. After switching accounts, old
  surveys no longer sync — create a new survey.
- The survey owner cannot rate their own survey; test in a private window with a different person.
- ProvenExpert does not publish ratings automatically; the owner releases them.
- The contacts filter in KlickTipp can list everyone who rated 4–5 stars (testimonials).
- A restart waits 5 minutes, then re-checks the start condition at the next contact change.
- The Gmail check is a rough signal for a Google account: customers with other addresses may have
  one too, they simply get the ProvenExpert mails.
- A Google click can come from a mail scanner, not a person; the branch then ends early.
- Deleting an action in an active campaign aborts the runs of contacts waiting on it — say so
  before you change a running campaign.

## Boundaries

Google only as the optional Gmail branch of this template. Review campaigns for other portals
(Trustpilot …) or Google alone → `automation` with the Masterclass templates. Mail wording and design → `email`. Opt-in → `opt-in`. Tags as such → `tags`.

## Sources

- KlickTipp knowledge base: "ProvenExpert mit KlickTipp verbinden" (link in
  [references/provenexpert-setup.md](references/provenexpert-setup.md)); use it for click paths
  only, never its campaign template.
- ProvenExpert help: https://help.provenexpert.com/de
