# KlickTipp: import and adapt

## Import

Template link (prod, test phase): `https://app.klicktipp.com/template/4pv8zp13tzfz03bb`.
Use only this link — never a campaign template linked in the knowledge-base article, never a
Masterclass template. It is not in the `search-automation-templates` catalogue.

**All six mails come with the import.** Never create new mails, never replace their content or
design; you only swap links and placeholders. The mails are drag-and-drop by design.

1. `get-automation-template` → objects: the action tag, field Vorname, the field "E-Mail-Adresse
   (Kopie für Google-Weiche)", 6 mails (ProvenExpert request, reminder, thank-you, improvement;
   Google request, Google reminder). The ProvenExpert conditions and the survey link belong to the source
   account; they are rewired in § Adapt.
2. Mappings: pass every tag, mail and the copy field **without** `useExistingId` (copy); keep
   `FirstName`. In the
   source account the default would point at the source's own tag and mails.
3. `import-automation-template` with name and `objectPrefix` **without trailing space** (the import
   adds one). Report `created`, `mapped`, `failed`, `notTransferable`.

## Structure (what the imported campaign looks like)

```
Start: action tag AND active email subscriber        (+ add: survey NOT "bewertet")
→ remove action tag → copy email address into the copy field
→ copy field without @gmail./@googlemail.? no → Google branch (below)
→ [survey NOT "bewertet"]? (no → exit)
→ wait 1 day → request mail → wait 1 day (upper bound)
→ ["betreten" AND NOT "bewertet"]? yes → reminder now │ no → wait 1 day → reminder
→ wait 3 days (upper bound) → ["bewertet"]? no → restart │ yes → goal
Goal ["bewertet"] (fires anywhere) → wait 5 min → ["4 oder 5 Sterne"]? yes → thank-you → exit
                                                     │ no → ["bewertet"]? → improvement → exit
Google branch: Google link clicked before? yes → exit │ no → wait 1 day → Google request
→ wait 2 days → clicked? yes → exit │ no → Google reminder → wait 3 days → restart
```
The Gmail check reads the copy field because a decision cannot test the email address itself:
pointed at the address directly, the condition arrives empty after an import, no check reports
it, and every contact runs into the ProvenExpert branch. Leave the copy action and the decision
as imported.
[…] = left empty in the template. Every step with an empty condition says in its name, after
"SETZEN" or "ERGÄNZEN", which condition belongs there; the campaign notes repeat the setup steps.

## Adapt (campaign is paused after import)

`get-automation`; keep the revision for every write; `dryRun` first when unsure.

What the import leaves: the ProvenExpert conditions are empty — `validate-automation` reports
`empty segment in condition` for every decision and the goal, and the start lacks its survey
condition (no finding). The mails arrive unpublished. The survey link `%Link:Redirect(<id>)%` in
request and reminder still names the template's survey, and **no check reports it**.

1. **ProvenExpert conditions** — fill each step that says "SETZEN" or "ERGÄNZEN" with the smart
   tags of the user's survey (ids from Order step 3), as its name says: `plugin is started`,
   `plugin is not finished`, `plugin is finished`, `plugin is in progress`; value `0` (any time).
   Five decisions, the goal and the start. Rename the steps afterwards (drop the "SETZEN …" part).
2. **Start** — action tag AND "is active email subscriber" AND add `plugin is not finished`. All three.
3. **Mails** — order per mail: subject first (`update-automation-email-draft`), then content, then
   publish; a subject change after the content edit makes the publish refuse with
   `newsletter_content_changed`. Request and reminder: replace the survey link in the linked
   paragraph "Jetzt bewerten" with the user's `%Link:Redirect(<id>)%` from
   `search-email-editor-placeholders` (keep it a linked paragraph; a button loses the link in the
   plain text). Thank-you mail may show `%Subscriber:CustomFieldPlugin:Val-<id>%`. Point out placeholders
   such as `[Produkt-Name]` and `[Dein Name]` in subjects and texts; the wording is the user's.
   Team copy (Questions first #5): set `bccEmail` on the improvement mail only.
4. **Google branch** — with a Google review link (Questions first #6): in the Google request and
   reminder replace `https://g.page/r/ERSETZEN-GOOGLE-BEWERTUNGSLINK/review` in the linked paragraph
   "Jetzt auf Google bewerten" and rename both steps (drop "SETZEN …"). Without a link: delete the
   decision "Google: Link schon einmal geklickt?" with `subtree`, then the Gmail decision with
   `keep_yes`; the copy action may stay, the two Google mails stay unused in the account — say so.
5. Publish every mail the campaign uses (six, or four without Google). `validate-automation` — no
   findings expected.
6. **Notes** — drop the "EINRICHTEN" block once done; ≤ 1000 characters, while paused (activation
   refuses longer notes and `validate-automation` does not warn).

## Bridge (purchase tag → action tag)

Default: on every purchase tag of this product, add the action tag under "Automatische
Tag-Vergabe" (tag settings, "Erweiterte Einstellungen"). It fires on the first purchase and again
on a repeat purchase, even if the purchase tag is already on the contact. The MCP can only read it
(`get-tag` → `subscribesToTagIds`), so set it with the browser extension or guide the user. It
changes the user's existing tag: list it and get an "ok". Never start the review campaign on the
purchase tag itself — it removes its start tag.
