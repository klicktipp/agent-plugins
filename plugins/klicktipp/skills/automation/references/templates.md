# Automation templates: find, read, import

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
   obvious.
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
   listed take the default from step 2. **Omitting `mappings` entirely copies everything** — that is
   the dialog's default with smart import off.
5. **Report** from the answer, never from memory: `automationName` and `editUrl`, what was
   `created`, what was `mapped`, anything `failed`, and `notTransferable`.
6. **Finish the automation** with the other tools of this skill — the imported one is an ordinary
   automation. Set the start condition where `notTransferable` says it could not be carried over,
   replace placeholder text in the emails (the sales-funnel templates carry `[Was ist das Thema
   deines Angebots]` and the like), then `validate-automation`.

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
  editor document. Placeholders of copied custom fields are rewritten to the new fields.

## Resources

The catalogue is also published as MCP resources, for a person who wants to attach it rather than
for you to call: `klicktipp://automation-templates` (the catalogue),
`klicktipp://automation-templates/{code}` (the package manifest) and
`klicktipp://automation-templates/{code}/emails/{file}` (one email's `.html`, `.json` or `.txt`).
To choose and import, use the tools above — they work in every client.
