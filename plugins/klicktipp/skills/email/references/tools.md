# What the tool descriptions do not say

**This file does not repeat the tool descriptions.** The MCP server already sends you every
description and every parameter with its type and limits. Here is what those cannot say: the order
between calls, the pitfalls, and what one tool means for another. The procedure is in `../SKILL.md`.

`R` reads only · `D` replaces without undo · `O` reaches outside the account.

## Reading and publishing

| | |
|---|---|
| `get-email-editor-content` | The three document projections exist only for drag-and-drop drafts, `publishedContent` always. Take the outline, not `content` — a quarter of the bytes. A style property the document does not carry is **absent** from the outline rather than empty: the editor applies defaults at render time. `writeBlockers` names states that allow reading but block every write. `importWarnings` applies to `replace-email-editor-content-from-html` only. |
| `validate-email-editor-content` | Severity says what the **next** step does, not what the dispatch does. `publish-newsletter-email-content` refuses without `%Link:Unsubscribe%` (or `%User:Signature%`, which brings it) — so a missing unsubscribe link is a **lock**, while a missing `%Link:SubscriberInfo%` is a decision. `blockCount` distinguishes "found nothing" from "empty document". An unconfigured add-on cannot be fixed from here at all. |
| `publish-newsletter-email-content` | Takes no HTML, only the stored revision. `operation: unchanged` means the draft was already the dispatch content. Editor features the server may not publish on someone's behalf are rejected with the editor URL. |

## Filling a body — which of the three

| Source | Tool | Note |
|---|---|---|
| another email of this account | `replace-email-editor-content-from-email` | source may be sent long ago and is only read; target loses its body completely; source ≠ target; an empty source is rejected rather than emptying the target |
| an editor document (JSON) | `replace-email-editor-content-from-document` | converts nothing, so loses nothing — layout, spacing, dividers, tables, decisions and AI blocks arrive as sent. `page`-rooted or the page itself. A refusal saying "The document you sent" is about **your** input, not the newsletter |
| HTML only | `replace-email-editor-content-from-html` | add-ons, decisions and AI blocks do not survive; the footer needs `%User:Signature%` or the spelled-out mandatory details |

All three: full replacement without undo, first call over existing content is **refused with a list
of what would be lost**, only `replaceExistingContent: true` on the second converts, bound to the
`contentRevision`, and none of them publishes (`nextAction: review_and_publish_content`). `created`
in the result names new uuids plus the next revision; for a coordinated revision of an existing
document, independently read back the retained structure and display conditions as described in
[`template-revision.md`](template-revision.md). The overwrite guard is not an exact field-level diff.

**After an HTML import, read the result's `warnings` and pass them on.** They say what *this*
conversion cost: the layout was rebuilt (rows, columns and spacing are the editor's now, plus
spacers nobody sent), and one line with numbers per construction that did not come back as its own
block — dividers, lists, tables, images, videos, each naming the tool to restore it. Never report
"the import worked" without them.

## Templates

| | |
|---|---|
| `search-email-editor-templates` | The **number** in the answer is for pointing at a design; **apply and preview take the `id`** (`monthly-marketing-dispatch`). Category, collection and tag are free text from the catalogue's own vocabulary: a value the tool answered with is always accepted back, an unknown one matches nothing rather than being refused. The catalogue is large — `events` alone is ~300 designs — so narrow with a facet from the answer instead of paging. Categories name the occasion, tags name the purpose. |
| `preview-email-editor-template` | Renders the **design itself**, not the catalogue thumbnail — so what is approved here is what gets written. A number instead of the id is refused by name. **The preview is what a template request is answered with**, not the search grid and not a description of it. A host without MCP Apps gets `contentHtml` only (30–70 KB, sometimes saved to a file instead of returned) — display that HTML unchanged, with any gallery wrapper clearly separate. See `../SKILL.md`, "Picking a template", step 2. |
| `replace-email-editor-content-from-template` | The design is fetched from the catalogue on the call. Works for any email the editor opens: newsletter draft, automation email, notification email. |

**Never describe a template in prose.** Its name does not describe it, and neither can you — show
it. See `../SKILL.md`, "Picking a template".

## Blocks

Every add takes `editorUrl`, `contentRevision`, `columnUuid`, optionally `position`, and brings its
content along. Kinds, fields, pitfalls and import cost → [`blocks.md`](blocks.md).

`move-email-editor-block` · `remove-email-editor-block` work on every kind. **Remove and re-add is not a change** —
typography, add-on configuration and the uuid are lost. See `../SKILL.md`.

## Images — ⚠ not on production

"unknown tool" there is the pending release, not a defect.

| | |
|---|---|
| `list-email-editor-images` | **Lists, does not search by subject** — `query` matches a file name or folder path fragment: "logo" finds logo.png, "car" finds no photo of a car. No total; page with `cursor` returned unchanged and the same `query`. |
| `search-email-editor-stock-images` | Pexels/Pixabay. `query` one or two words **in English** (the archives are indexed in English), `limit` 1–12, `minWidth` 1200 for a full-width image. **Never comes back empty** — without matches it returns unrelated photos, so say what is actually there. The URLs never go into a newsletter. Licence needs no attribution but restricts recognisable people — the user's decision. |
| `upload-email-editor-image-from-url` | The way in for a stock photo: pass `sourceUrl` and `fileName`, use the URL that comes back. |
| `open-email-editor-image-upload` | Opens the **upload form**; takes nothing and stores nothing, the user picks the file in the window. Never ask for base64. Without an app host you only see "form opened" — then `upload-email-editor-image-from-url` is the only way. |
| `upload-email-editor-image-file` | The form calls this itself. `visibility: [app]`, so not in your tool list — you have no file to send. |
| `preview-email-editor-image` | Shows one image URL as an image before it goes into an email. "1200x800, autumn-hero.jpg" is not an image. Only the library CDNs, the editor's resource host, Pexels and Pixabay — the host declares the iframe CSP before knowing which image is asked for, so the list is fixed. An image on the customer's own server is **rejected by name**; the way in is `upload-email-editor-image-from-url`. `https` only. |
| `list-email-editor-image-folders` · `create-email-editor-image-folder` · `delete-email-editor-image-folder` | Paths like `Kampagnen/Herbst`; intermediate levels are created with; only an **empty** folder can be deleted. |

## Dynamic content

`get-email-editor-display-condition-capabilities` · `update-email-editor-display-condition` · `configure-email-editor-row-display-condition` ·
`list-email-editor-display-conditions` — the procedure, the full catalogue of condition types and the failure mode
(a condition matching nobody is not an error) are in
[`display-conditions.md`](display-conditions.md).

## Two response shapes worth knowing

- **Every content write** returns the next `contentRevision` and `created` with the uuids it made.
  That is why creating and carrying on is one write after another with no read in between.
- **A refusal is not a defect.** It names the state and, where there is one, the way on. Pass the
  code, not a paraphrase.
