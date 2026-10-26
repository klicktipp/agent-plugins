# KlickTipp: import and adapt

## Import

Template source: https://app.klicktipp.com/template/4pjhzv3bzfzd6bc — the Webinaris campaign
template "Webinaris | Webinar Erinnerungskampagne" that ships with this skill. Use no other
template or campaign as the source.

1. `get-automation-template` → present the objects: 4 tags from Webinaris (Angemeldet, Nicht im Raum
   nach Start, Teilgenommen, Nicht teilgenommen) plus helper tags (In Kampagne, Bestätigung vorab
   gesendet, Statistik: Jemals angemeldet), 5 fields, 7 emails (the confirmation is used twice: normal path and rebooking).
2. Mappings: `suggestedExistingId` proposes reusing objects of the same name. In the account that
   owns the source campaign (and in any account that imported before) that means the source's own
   tags, fields **and emails** — editing them would change the source. Therefore pass a mapping for
   **every** tag, field and email **without** `useExistingId` (= copy), except `FirstName`/`LastName`.
   Never map two webinars onto the same Webinaris tags.
3. `import-automation-template` with name, prefix, mappings. Pass the prefix without a trailing
   space (`Webinar Masterclass |`): the import adds the space before each name itself. Report
   `created`, `mapped`, `failed`, `notTransferable` from the answer and keep the `created` list —
   it is the map for the email placeholders below.
4. **Sender** — read every imported email with `get-automation-email` (`effectiveSender`). The
   import can leave an explicit sender on the emails that is not the one this account sends with.
   Set name, address and reply address to the account's sender (ask which one if there are
   several) with `update-automation-email-draft`; `validate-automation` reports an unusable one as
   "email sender cannot send".

## Adapt (campaign is paused after import)

Read the campaign with `get-automation`; keep the revision for every write.

1. **Start action** — tag = `<P> Angemeldet` AND "is active email subscriber". Fix if
   `notTransferable` lists it.
2. **Email placeholders** — every email (confirmation ×2, reminders ×3, live, thank-you, missed-you):
   - **text** holds readable markers: `[[Webinar Datum]]` and `[[Webinar Uhrzeit]]` (confirmation,
     reminders). Replace each with the placeholder of the matching new field,
     `%Subscriber:CustomField<id of "<P> Webinar Datum">%` resp. `… Webinar Uhrzeit`. No `[[…]]`
     may be left in any email — a recipient would read it literally;
   - **links** (buttons) hold the real placeholder of the source field
     (`%Subscriber:CustomField<id>%`), because publishing refuses a link without a URL scheme.
     The link's `title` names the field: "Webinar Link" (room link, emails 1–5), "Webinar
     Aufzeichnung Link" (recording, missed-you mail). Build the map *source field id → new
     field id* from the import answer (`incomingId` → created `id`) and swap only the number in
     the href; keep the `title`;
   - **subjects** are remapped by the import itself — check them, but they normally need nothing;
   - the source ids are the fields' `incomingId` in the template answer — read them from there,
     never assume them. After the swap no `incomingId` of a field may be left in any email;
   - recording button → `<P> Webinar Aufzeichnung Link`;
   - "7 Tage" in the missed-you mail = answer to question 4.
   Publish each email, then look at the preview: button text must be readable (white on blue; the
   editor can override the link colour on publish).
3. **Reminder slots** — three `[CFG: Erinnerungszeitpunkt n]` pairs (decision "noch mehr als X
   entfernt?" + wait "bis X vor Termin"). Set X per question 3; keep the mail name and subject in
   line with X. The decision's *no* branch already leads to the next slot. Fewer reminders: let the
   step before the slot lead straight to the next slot decision (`move-automation-action`) and
   remove the unused slot actions only after the user agreed.
4. **LIVE-CHECK** wait = N + 4 minutes after `<P> Webinar Termin`.
5. **ZU SPÄT FÜR LIVE** decision = date field "is before" `-R minutes`; **SCHON GESTARTET** =
   `-1 minutes`. Date operators take plural units; "now" is refused. The removal of old
   "Teilgenommen"/"Nicht teilgenommen" tags sits on the *no* branch of ZU SPÄT FÜR LIVE; keep it
   there, otherwise late confirmers lose the result tags Webinaris already set.
6. **Result loop** — 5-minute check cadence, ends 12 h after the date or when the date field is
   empty: leave as is.
7. `validate-automation` — only "possible delay" warnings at go-to actions may remain (about 600
   for the template). Do not add go-to actions without need: each one multiplies the paths and
   the notes in the activation dialog.
8. **Notes** (≤ 1000 characters) while paused.
9. **Opt-in mail** of the webinar's DOI process: KlickTipp's default text is formal ("Sie") and does
   not mention the webinar. Offer a short webinar-specific text (purpose of the sign-up, du/Sie as
   the account's mails); change it only after the user agreed — wording is theirs.
10. `prepare-automation-activation` → link to the user. Activation must happen **before** any test
    registration: a paused campaign does not pick contacts up later in a useful order.

## Known limitation: plain-text part

All buttons are linked paragraphs, not button blocks: a button block loses its link in the
generated plain text. Keep it that way when editing the mails. KlickTipp numbers the footnotes of
the mail body and of the signature separately, so `[1]` can appear twice in the plain text; the
links are right and the HTML part is unaffected. Do not store a plain text to work around it — a
stored plain text blocks every later body edit.

## Editing pitfalls

- Active campaigns cannot be changed (graph or notes). Ask, then `stop-automation`.
- Inserting a decision hangs the old follow-up on its **yes** branch; move it with
  `move-automation-action` (subtree) to **no** where needed.
- Stale revision → read again, retry once.
