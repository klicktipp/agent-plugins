# Tests after activation

Use plus-addresses of the user (`name+wa@…`). Webinaris needs 1–2 min to transfer; the result
mails come up to 5 min after the Webinaris tag.

## Smoke test (≈ 25 min + webinar length)

Create a date ~25 min ahead.

| Contact | Action | Expected |
|---|---|---|
| A | register, confirm, be in the room at start, stay ≥ 10 % | confirmation, 15-min reminder, **no** live mail, thank-you |
| B | register, confirm, stay away | confirmation, reminder, live mail at N+4, missed-you with recording |
| C | register 2–3 min after the start, confirm | **only** the live mail, then result mail |

Check after each step with `get-contact-history`; compare field values with `get-contact`.

## Simulating Webinaris (no Webinaris connection, e.g. a test account)

Only on the user's request, only with their plus-addresses, and only after activation. Do what
Webinaris would do, at the same minutes; announce each step with its time before you do it.

1. Registration, in this order: `subscribe-contact-via-opt-in-process` with the webinar's opt-in
   process (no tag); `update-contact-values` with the five fields (Datum `TT.MM.JJJJ`, Uhrzeit
   `HH:MM`, Link and Aufzeichnung as URLs, Termin as date and time); then `tag-contact` with
   `<P> Angemeldet`. The fields must be set before the tag. The user confirms the opt-in mail.
2. Minute N after the start: `tag-contact` with `<P> Nicht im Raum nach Start` for everyone who is
   "not in the room".
3. One minute after the end: `<P> Teilgenommen` or `<P> Nicht teilgenommen`.
4. Rebooking: new field values first, then `<P> Angemeldet` again.

Say clearly that a simulation tests the campaign, not the Webinaris settings.

## Extended cases (already passed on the reference setup, repeat when settings differ)

- Rebook after confirmation (≥ 6 min after start of the run) → new confirmation, reminders follow.
- Rebook before confirming the opt-in → new date is used.
- Confirm only after the room closed → no mail until the result mail.
- Confirm only after the webinar ended (after Webinaris set the result tag) → the result mail
  still comes, within 5 min of the confirmation.
- Repeat registration of a contact who finished an earlier run → restarts, no opt-in mail.
