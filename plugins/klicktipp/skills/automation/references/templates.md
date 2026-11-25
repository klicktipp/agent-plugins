# Automation templates: find, read, import

## Contents
Order (find, read, settle, import, report, finish) · What the import is and is not · Resources

Two kinds of templates, one pair of tools for both:

| Source | What the user has | What you pass as `templateLink` |
|---|---|---|
| **Catalogue** — the ready-made automations of the Business Automation Masterclass (BAM), shipped with KlickTipp | nothing, or a use case ("Termin nachfassen") | the `uri` from `search-automation-templates`, e.g. `klicktipp://automation-templates/teve` |
| **Shared template** — a template another account published | a link `https://app.klicktipp.com/template/…` | the link as pasted; host, trailing slash and line breaks do not matter |

## Order

1. **Find.** `search-automation-templates` with the user's goal in their words as `query`
   (German works best — the catalogue is German). Omit `query` to list everything; `module`
   narrows to one Masterclass module. Each hit carries `description`, `startsWhenTagged`,
   `emailSubjects`, `tagNames`, `customFieldNames` and `includedAutomations`. Pick by those, not
   by the name. Present two or three candidates with one sentence each when the choice is not
   obvious. When several templates serve one goal at different stages, ask the one question that
   decides between them (offer: already sent?) before importing, and recommend one — also when the
   user names or links all of them. Do not suggest importing all.
2. **Read.** `get-automation-template` with the uri or link. It answers with:
   - `objects` — every tag, custom field, email and outbound the import brings, each with
     `suggestedExistingId`: the account's object of the same name the import maps it onto by
     default. `''` means a copy is the default.
   - `smartImportAvailable` — whether this account may choose the automation name, a prefix,
     labels and mappings at all.
   - `importable` / `refusal` — whether an import would be refused now (for instance the outbound
     limit), and why.
   - `notTransferable` — references the import cannot carry over, typically a start condition on a
     form or an API key of the account the template came from. They have to be set again after the
     import; say so before importing.
3. **Settle with the user**, only what the account can choose (`smartImportAvailable`):
   - the **name** of the new automation — ask, do not invent; the default is the template name and
     a name already used is refused;
   - an optional **prefix** for every created object, so the imported tags and emails stay
     recognisable;
   - **mappings**: for each tag and custom field, reuse an existing one or create a copy. Reusing
     matters for tags and fields the account already works with (`per Du`, `Kunde`, first name).
     The account may hold the same meaning under another name ("Käufer", "Bestandskunde"): look
     with `search-tags` / `search-custom-fields` and ask before copying. A template that fills a
     date field itself (DaZu sets "Kunde seit") writes today's date: ask where existing contacts get
     their real value, which has to be imported first (skill `contacts`).
   - **templates that belong together** — one sets the tag the other starts on, or fills a field
     the other's start condition or waits read: in the second import, map that tag and those
     fields with `useExistingId` to the ones the first import created. Otherwise it is
     copied (with a prefix always) and the second automation never starts. Without smart import,
     read both with `get-automation` afterwards and set the second one's start tag with
     `update-automation-start-action`.
4. **Import.** `import-automation-template`:

   ```json
   {
     "templateLink": "klicktipp://automation-templates/teve",
     "automationName": "Terminvereinbarung",
     "objectPrefix": "TEVE",
     "mappings": [
       {"type": "tag", "incomingId": "1234", "useExistingId": "987"},
       {"type": "custom-field", "incomingId": "5678"}
     ]
   }
   ```

   A mapping with `useExistingId` reuses that object; without it the object is copied. Objects not
   listed — and all objects when `mappings` is omitted — take the default from step 2: the
   same-named object where `suggestedExistingId` is set, otherwise a copy. To copy everything, list
   every object without `useExistingId`.
5. **Report** from the answer, never from memory: `automationName` and `editUrl`, what was
   `created`, what was `mapped`, anything `failed`, and `notTransferable`.
6. **Finish the automation** with the other tools of this skill — the imported one is an ordinary
   automation. Set the start condition where `notTransferable` says it could not be carried over,
   replace placeholder text in the emails (the sales-funnel templates carry `[Was ist das Thema
   deines Angebots]` and the like) with the user's real values — sales address, phone, URLs; from
   `company-context` if confirmed, otherwise ask — then `validate-automation`. Check the start
   condition with `get-automation` even when `notTransferable` is empty (see below). Then:
   - **Check every imported email's plain text.** The import rewrites field placeholders only in
     the HTML. For each classic (rich-text) email, read it with `get-email-editor-rich-text-content`;
     if `plain` still names a field ID from the template's `objects` (`incomingId`), call
     `replace-email-editor-rich-text-content` with `html` and `contentRevision` exactly as read and
     without `plain`. The answer's `plainSource` `derived` means the plain text is now generated
     from the HTML; `custom` means the account maintains its plain text itself: tell the user to fix
     it in the editor. In drag-and-drop emails, have each old `incomingId` placeholder replaced with the new
     field's (from `created` / `mapped`) via skill `email`. Say which emails you fixed.
   - Read `settings.notes` from `get-automation` and tell the user how a contact enters (start tag,
     required fields) and which limits the notes name.
   - Offer one test run before real contacts get the start tag: after the user has activated the
     automation in the dialog, tag one test contact the user names (skill `tags`), check every email
     and notification, and skip waits with `move-contact-past-automation-wait` (preview first,
     `confirm` only after the user agreed).

## What the import is and is not

- **It is additive and there is no undo.** Every created object stays in the account, listed in
  the answer. A second call imports a second time.
- **Nothing is sent.** The automations are created **paused** — not started. Starting one is
  `prepare-automation-activation`, which a person confirms in KlickTipp.
- **Refused before anything is written** when the outbound limit would be exceeded, the name is
  taken, a mapping points at an object the account does not have, or two template objects are
  mapped onto the same one. The refusal says which; fix that and call again.
- **Without smart import** the account cannot choose name, prefix, labels or mappings; passing any
  of them is refused. Every object is then copied with the prefix `Importiert`, as in the dialog.
- The emails arrive with their content: classic emails as HTML, drag-and-drop emails with their
  editor document. Placeholders of copied custom fields are rewritten only in the HTML of classic
  (rich-text) emails, not in their plain text and not in drag-and-drop emails; step 6 fixes both.
- An email referenced only in the start condition, not in an email action, does not come along;
  the condition then points at nothing.
- Smart links come along with their URL; a click counts only if the email link matches it exactly.
  When you replace a URL in an email, set the smart link to the same URL with `update-smart-link`.
  A smart link shared by two templates arrives twice (the second `<name>_1`); check that each
  email links to its own.

## Resources

The catalogue is also published as MCP resources, for a person who wants to attach it rather than
for you to call: `klicktipp://automation-templates` (the catalogue),
`klicktipp://automation-templates/{code}` (the package manifest) and
`klicktipp://automation-templates/{code}/emails/{file}` (one email's `.html`, `.json` or `.txt`).
To choose and import, use the tools above — they work in every client.
