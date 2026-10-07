# Bringing a new email into being

You land here when the body of an email has to **come into being** — there is no styling yet to take
over, or you have to write it yourself. If it is only about pulling in existing styling, the short
way is in `SKILL.md` and you do not need this file.

**First the question that decides everything else: does the styling already exist somewhere?**

- As **another email of this account** — the last issue, a template mail → `replace-email-editor-content-from-email`. One
  call.
- As an **editor document** — template, export → `replace-email-editor-content-from-document`. One call.
- **Only as HTML** — from an agency, from another tool → `replace-email-editor-content-from-html`. One call, plus the
  conversion cost listed in `importWarnings`.

Only when **none** of these exists does the body genuinely come into being — and even then it belongs
in one call: write the document yourself (`references/document-skeleton.json` for the form,
`references/simple-schema/` for the fields) and store it with `replace-email-editor-content-from-document`.

**Why this is not a matter of taste.** Every tool call costs 15–30 seconds, most of it not in the
server but in the model ahead of it. Assembling an email out of fifteen blocks is fifteen rounds plus
rows and styling — measured runs land at over ten minutes, for a result a single import reaches in
under one.

**Block by block** (`add-email-editor-row`, then one `add-email-editor-<kind>` per block) remains the way for the
**single additional** block in a draft that already stands — not for a whole body. And it is the
fallback when a document cannot be produced: tell the user it will take longer then.

What a newly created body does **not** bring along is styling. An empty draft has no block for a new
one to copy its look from — every block lands in its initial state, and without a countermeasure the
result looks thrown together, however good the texts are. So set typography, spacing and colours
yourself, and **for all blocks together**: `update-email-editor-page-style` for the page,
`update-email-editor-row-style` per row, `update-email-editor-block-style` for the individual block. **Set the page
first**, before the first block comes into being: the page's text colour goes into paragraphs,
headings, texts, lists and tables at creation time when they have no predecessor to copy from. Set
afterwards, it no longer reaches the existing ones. An email looks professional through spacing and
consistent typography, not through decoration; a half-converted scale looks worse than none.

Two things belong on the right level:

**Set the font once on the page**, with `fontFamily` in `update-email-editor-page-style` — not per block. The
blocks stand at `inherit` in their initial state and pick up the page setting by themselves. On offer
are the system fonts of the editor's own list, under **exactly the names used there**: `Arial`,
`Courier`, `Georgia`, `Helvetica Neue`, `Lucida Sans`, `Tahoma`, `Times New Roman`, `Trebuchet MS`,
`Verdana` plus the two Japanese ones `ヒラギノ角ゴ Pro W3` and `メイリオ`. You give the **name**, not
the stack — the server writes the fallback chain. `Helvetica` and `Courier New` are still accepted;
they used to be in the list.

**A web font such as Montserrat or Roboto cannot be set** even though the editor offers it: that also
needs an entry in `page.body.webFonts` with a Google Fonts URL so the editor produces the `<link>`.
Without it, it silently falls back to a system font at the recipient's end and nobody sees it. That is
why the eight — Bitter, Droid Serif, Lato, Montserrat, Open Sans, Roboto, Source Sans Pro, Ubuntu —
are not on offer here at all, rather than as names that do nothing. Whoever wants one sets it in the
KlickTipp editor.

**The alignment of the whole email** is `contentAlign` — `left`, `center` or `right` — in the same
tool, next to `contentWidth`. It decides where the message sits when the window is wider than it is;
it has nothing to do with the alignments *inside* a block (`textAlign` in
`update-email-editor-block-style`). A new draft starts from the default document, not from the look of another
newsletter — so whoever rebuilds a template sets width, alignment and font themselves.

**Put a border around a row on the row**, with `borderTop`/`-Right`/`-Bottom`/`-Left` in
`update-email-editor-row-style` — not on its columns. A border per column draws a box per column with visible
seams between them, instead of one line around the whole row. The same goes for padding: `paddingTop`
and siblings on the row keep the content away from the row's edge, the column variant only from the
column's.

If HTML already exists — from an agency, from another tool — `replace-email-editor-content-from-html` is the way for it
(see "Editing existing HTML" and the mandatory rules in `references/html-authoring.md`). **But do not
write HTML just to import it.** The conversion costs what `importWarnings` lists, and what you have
just built is already a document — the block tools get there without the detour.

### How to generate one

1. **Decide yourself, without asking** — order of rows, colours, imagery. The brief says what it is
   about; the styling follows from that. Say afterwards in one sentence what you decided — the user
   can correct that and then has something finished in front of them instead of a question. **This
   applies to styling, not to decisions about the audience**: subject, recipients, send time and a
   split test's settings you ask for rather than choose — and whatever you did choose yourself, you
   name as your choice and never as a default.
2. **Store the whole body in one call** — after the routing question above. If you write the document
   yourself, `references/blocks.md` is still the source for what fields each block kind carries; the
   add tools and the document know the same fields. Only if it
   has to be block by block: `add-email-editor-row`, then the blocks inside it — heading, paragraph, image,
   button, list, spacer as the basic kit.
3. **Set the styling, coherently.** Page, rows, blocks — with the style tools from the paragraph
   above, not block by block by feel.
4. **The footer belongs in every email**: unsubscribe link and provider identification. Whoever
   forgets it gets it held up by `validate-email-editor-content` at the latest — better beforehand.
5. **Getting images — in this order.** First `list-email-editor-images`: logo, product photo, team picture
   are in the account's media library and in no stock archive. The tool **lists, it does not search**
   — it hands out a page of the library, and `nextCursor` fetches the next. It takes no query,
   because the store knows file names and not subjects: "car" would never have found a photo of a
   car. So read a page and choose from it. If nothing is there, `search-email-editor-stock-images` — the same
   free archives (Pexels, Pixabay) the editor offers. Your own material comes in through
   `open-email-editor-image-upload`.

   **A stock URL must not go into the newsletter.** Pass `sourceUrl` and `fileName` of the chosen
   photo to `upload-email-editor-image-from-url` and use the URL that comes back. A foreign URL makes every
   mailbox contact a third party and breaks on the day the photo disappears there.

   Two things that will otherwise embarrass you: the stock search **never comes back empty** — for a
   query without matches it returns unrelated photos. Look at what came back and say what it shows,
   instead of presenting it as a find. And **let the user choose**: the licence requires no
   attribution but restricts recognisable people — that is their decision.
6. **`validate-email-editor-content`** before publishing — and pass the findings on instead of fixing silently.

**Where you do ask**, because it is not styling: before an import replaces existing content, before a
block is removed, and when choosing a stock photo — its licence restricts recognisable people, and
that is the user's decision. You decide styling, they decide losses and rights.
