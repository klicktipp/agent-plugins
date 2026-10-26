---
name: webinaris-webinar
description: Sets up a complete KlickTipp campaign for a Webinaris auto-webinar — confirmation, reminders, a "we are live" mail for latecomers, a thank-you or missed-you mail with the recording, rebooking — by importing the Webinaris campaign template, adapting it to the account, and guiding the user through the matching Webinaris settings. Use when the user mentions Webinaris, an auto-webinar or evergreen webinar together with KlickTipp, or webinar reminders and follow-ups, even if they only say "I use Webinaris and want a campaign for it".
prerequisites: "A Webinaris account with an auto-webinar, a KlickTipp account the plugin is signed in to, and a double opt-in process in it"
---

# Webinaris webinar campaign

One webinar = one campaign. Each webinar gets its own import with its own prefix. Never build the
old pattern of several follow-up campaigns.

The campaign only works when Webinaris sends the right tags and fields at the right minutes. Half of
this skill is therefore the Webinaris setup. Webinaris has no MCP server: you either guide the user
step by step, or — if the Claude browser extension is connected — make the changes yourself after
the user has confirmed them as one batch.

Build on the `automation` skill for the KlickTipp mechanics (template import, revision, decisions,
validation, activation). This skill adds what is specific to Webinaris.

## Ground rules

- **Language.** Talk to the user in their language. Quoted German labels (Webinaris screens, KlickTipp
  names, Webinaris variables) are the exact UI texts — keep them verbatim.
- **Ask before you build.** Collect the answers of *Questions first* before the first write.
- **One step at a time in Webinaris.** Say what to open, what to set, then wait for "ok" or a
  screenshot. Never stack several Webinaris screens into one message.
- **Browser extension:** list *all* planned Webinaris changes first (screen, field, old → new value),
  get one "ok", then apply them. Read back every screen after saving. The KlickTipp password in the
  Webinaris plugin is always typed by the user — never by you, never into chat.
- **Existing accounts are the normal case.** Before importing, look for what is already there
  (tags, fields, opt-in processes, campaigns with "Webinar"/"Webinaris" in the name, an existing
  Webinaris plugin connection). Offer to reuse or to create new; default to a **new prefix** so a
  second webinar never shares tags with the first.
- **Nothing goes live without the user.** The import creates a paused campaign. Activation is the
  user's click in the dialog from `prepare-automation-activation`.
- Wording of the emails belongs to the user (or their marketing). You adapt placeholders, dates and
  links; you do not rewrite copy unless asked.

## Questions first

Ask in one message, with a recipient-side example for each, and offer the defaults:

| # | Question | Default | Why it matters |
|---|---|---|---|
| 1 | Does the webinar already exist in Webinaris? New or cloned from another webinar? | — | A clone already carries plugin and settings; check, don't redo. |
| 2 | Which dates: 3/5/7 automatic, or own dates (incl. spontaneous slots)? | 5 automatic | All work; spontaneous slots simply skip reminders that are already in the past. |
| 3 | Reminder times before the start | 24 h, 1 h, 15 min | Configures the three `[CFG: Erinnerungszeitpunkt]` slots. Fewer reminders = remove a slot. Count the mails one recipient can get within 24 h (see *Mails per day*). |
| 4 | Recording link: 3 or 7 days, with or without pause/seek? | 7 days with pause/seek | Chooses the Webinaris variable for the recording field and the "7 Tage" text in the missed-you mail. |
| 5 | Name and prefix of the campaign | "Webinar <Thema> \|" | Keeps tags/fields of this webinar apart. Example of a resulting tag: "Webinar Masterclass \| Webinaris \| Angemeldet". |
| 6 | Which opt-in process should Webinaris use? | a dedicated double opt-in | Webinaris' own DOI stays off. |
| 7 | Is the Claude browser extension connected? May I make the Webinaris changes after you confirm them? | ask | Decides between guided and automated setup. |

## Order

Copy this checklist into your reply and tick it off:

```
- [ ] 1 Inventory  - [ ] 2 Import  - [ ] 3 Adapt + validate  - [ ] 4 Webinaris setup
- [ ] 5 Cross-check  - [ ] 6 Activate + smoke test  - [ ] 7 Notes
```

1. **Inventory** the account (read only): tags, custom fields, opt-in processes, sender, existing
   webinar campaigns. Report in three lines what you found and what you propose to reuse.
2. **Import** the template with the agreed name, prefix and mappings
   ([references/klicktipp-adapt.md](references/klicktipp-adapt.md) § Import).
3. **Adapt** the campaign: placeholders in all emails, recording-link button, reminder slots,
   `[CFG]` actions, publish the emails, `validate-automation`
   ([references/klicktipp-adapt.md](references/klicktipp-adapt.md) § Adapt).
4. **Webinaris setup** with the field and tag names from step 2
   ([references/webinaris-setup.md](references/webinaris-setup.md)).
5. **Cross-check** Webinaris values against the campaign (alignment rules below). Fix whichever side
   the user prefers.
6. **Test registration** before activation is not possible (paused campaigns do not run). Activate
   via `prepare-automation-activation`, then run the smoke test
   ([references/tests.md](references/tests.md)).
7. **Notes**: write the campaign note (≤ 1000 characters, human-readable) while the campaign is
   still paused — notes cannot be saved on an active campaign.

## Alignment rules (Webinaris ↔ campaign)

All minutes count from the webinar start.

1. Webinaris tag "Nicht im Raum nach Start" at minute **N** (default 5).
2. Campaign LIVE-CHECK wait = **N + 4** (default 9). Webinaris delivers tags 1–2 min late.
3. Webinaris "Webinarraum schließen" **R ≥ N + 4 + 5** (default 15), so whoever gets the live mail
   can still enter.
4. Campaign decision "ZU SPÄT FÜR LIVE" = start + **R** minutes. It also decides whether old
   result tags are removed: only while the room is still open (*no* branch). Later, the result
   tags Webinaris already set stay, so a late confirmer still gets the result mail.
5. Webinaris "Startverzögerung" = **Nein**. Otherwise every campaign time is too early.
6. Webinaris "Erneute Registrierung" = **"Schnittstellen-Aufrufe sollen immer nur für die letzte
   Registrierung gesendet werden"**. With "alle Aufrufe" the old booking keeps sending and overwrites
   date and link with the old values.
7. "Teilgenommen" / "Nicht teilgenommen" 1 min after the end; the result loop ends 12 h after the
   start — fine for any webinar under ~11 h.

## What the campaign does (for explaining it to the user)

- Start: registration tag **and** "can receive emails". Unconfirmed contacts start with their
  confirmation; bounced or unsubscribed contacts never start.
- Normal path: confirmation → reminders → at N+4 the live mail to everyone not in the room →
  after the end thank-you (attended) or missed-you with recording (not attended).
- Registered after the start, room still open → only the live mail with the room link, then result.
- Confirmed only after the room closed, even after the webinar ended → no mail until the result
  mail. Webinaris sets the result tags for unconfirmed contacts too; the campaign keeps them.
- Rebooking (also before opt-in confirmation) → the **first** rebooking in a run gets a new
  confirmation immediately. Any further rebooking in the same run is confirmed at the next check
  point (next reminder slot or the live check). Reminders always follow the new date. Repeat
  registrations weeks later restart the campaign automatically.

## Known behaviour worth telling the user

- Webinaris transfers registrations and tags 1–2 min late; the campaign is built for that.
- Two mails in a row (opt-in, then confirmation) are expected.
- Activation lists several hundred notes (about 600 for the template), one per possible path,
  each under a go-to action such as "ENDE nach Follow-up: Neubuchung → zurück zum Start-Ablauf",
  worded: "Info: Diese Aktion sendet E-Mails in einer Schleife. Wir begrenzen den Versand als
  Schutz vor Dauer-Versand auf maximal sechs E-Mails in Folge pro 24 Stunden an denselben
  Empfänger." (API: "possible delay"). Tell the user before they open the dialog: these are
  *possible* paths, not loops that happen. Every path back to the start passes "Angemeldet
  entziehen" and needs a new registration from Webinaris. Activating is fine.

## Mails per day

Count the mails one recipient can get within any 24 hours: confirmation, reminders inside that
window, live mail, result mail. The default plan reaches 5 for a same-day registration. If the
user's choice gives **6 or more**, say so before building: KlickTipp sends at most six mails in a
row per 24 hours from a loop to the same recipient and delays the rest (possibly the recording
mail), and recipients feel spammed long before that. Each rebooking adds one confirmation.

## Rules to tell the user

- Only Webinaris sets "Angemeldet". No other campaign, import, form, tagging pixel or smart link
  may set it or react to it. A campaign that sets it, e.g. on "missed-you mail sent", creates a
  real endless loop with mails.
- Do not change the date field ("Webinar Termin") or the result tags by hand. An empty date makes
  every wait "now"; a result tag sends the thank-you or missed-you mail at once.
- One webinar = one prefix. Two webinars must never share tags or fields.
- Webinaris only transfers into **Zeile** (single-line) fields, except the Unix timestamp, which
  must go into a **Datum & Zeit** field. A URL field also works for links.

## Boundaries

Webinars without Webinaris, or any other dated campaign → `automation` (BP‑2). Email content and
styling → `email`. Opt-in wording and consent scope → `opt-in`. Tags and fields as such → `tags`,
`custom-fields`.

## Sources

- Template: the template source in [references/klicktipp-adapt.md](references/klicktipp-adapt.md) § Import.
- Webinaris help: the plugin hint in "Schnittstellen" lists the data types; there is no public API.
