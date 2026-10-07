# Block kinds — one table

One row per kind: the tools, the fields with their storage path, the pitfall, and what an HTML
import costs it. The tool descriptions already carry purpose and parameters; this is what they
cannot say.

`remove-email-editor-block`, `move-email-editor-block` and `update-email-editor-block-style` work on **every** kind and are
not repeated per row.

| Kind | add / write | fields → stored at | import cost |
|---|---|---|---|
| **Heading** `heading` | `add-email-editor-heading` / `update-email-editor-text` | `text` → `descriptor.heading.text` · `level` → `descriptor.heading.title` | survives as itself |
| **Text** `text` | `add-email-editor-text` / `update-email-editor-text` | `html` → `descriptor.text.html` | survives as itself |
| **Paragraph** `paragraph` | `add-email-editor-paragraph` / `update-email-editor-text` | `html` → `descriptor.paragraph.html` | survives as itself |
| **List** `list` | `add-email-editor-list` / `update-email-editor-text` | `html` → `descriptor.list.html` | survives as itself |
| **Custom HTML** `html` | `add-email-editor-html` / `update-email-editor-text` | `html` → `descriptor.html.html` | comes back as the markup it renders to; the code block is gone |
| **Image** `image` | `add-email-editor-image-block` / `update-email-editor-image-block` | `src`, `alt`, `href` → `descriptor.image.*` | survives as itself |
| **Video** `video` | `add-email-editor-video` / `update-email-editor-video` | `src`, `thumbSrc` | comes back as a preview image with a link |
| **Icons** `icons` | `add-email-editor-icons` / `update-email-editor-icons` | entry list | comes back as images with links; the editable block is gone |
| **Button** `button` | `add-email-editor-button` / `update-email-editor-button` · style: `update-email-editor-button-style` | `label`, `href` → `descriptor.button.*` | survives as itself |
| **Menu** `menu` | `add-email-editor-menu` / `update-email-editor-menu` | entry list | comes back as links; the editable menu is gone |
| **Social** `social` | `add-email-editor-social-links` / `update-email-editor-social-links` | entry list | comes back as images with links; the editable block is gone |
| **Divider** `divider` | `add-email-editor-divider` · style: `update-email-editor-divider-style` | — | comes back as a styled line; the block is gone |
| **Spacer** `spacer` | `add-email-editor-spacer` · style: `update-email-editor-spacer-style` | — | survives as itself |
| **Table** `table` | `add-email-editor-table` / `update-email-editor-table` | rows of cells, each cell markup | comes back as plain markup; the editable table is gone |
| **Countdown**, **Contact card**, **Wowing video** | **no add tool** — the editor | add-on, handle in `moduleInternal.uid` | comes back as its rendered result; the add-on is gone |
| **Personalised email** | **no tool at all** | add-on | comes back rendered; the add-on is gone |

Import cost applies to `replace-email-editor-content-from-html` only. Editing through the block tools converts
nothing and costs nothing.

In the document every block is `mailup-bee-newsletter-modules-<kind>`; every add-on is
`…-modules-addon` and identified by `moduleInternal.uid` (`countdown-handle`, `vcard-handle`,
`wowing-handle`, `smartcopywriter-handle`, `personalized-email`).

## The pitfalls, per kind

- **Paragraph, text, heading, button** — the typography sits **in the markup itself** (wrapper
  `div`, `<p style=…>`, `<span style=…>`). A bare `<p>New text</p>` throws away size, line height
  and colour. Start from the markup you read and swap only the words. This includes a button's
  `label`.
- **Heading** — `level` is **structure, not size**: `h1` is the one headline, `h2` a section. How
  big it *looks* is in the markup. The field is stored under `descriptor.heading.title`, which the
  name belies.
- **Text vs paragraph** — the same thing to a reader. When you have the choice, take `paragraph`; it
  is what real newsletters mostly contain.
- **List** — `html` is the complete `<ul>`/`<ol>` markup, not just the items.
- **Image** — the URL has to be one of this account's. Order: `list-email-editor-images` (the account's
  library — it **lists, it does not search**: one page per call, `nextCursor` for the next), then
  `search-email-editor-stock-images` (Pexels, Pixabay) and the chosen photo through
  `upload-email-editor-image-from-url` with `sourceUrl` and `fileName`. **A provider URL never goes into a
  newsletter.** Own material through `open-email-editor-image-upload`.
- **Video** — without `thumbSrc` it is an empty box in the editor.
- **Icons** — not the same as social: any image with a label. `width`, `height` and `textPosition`
  are mandatory in the format and get copied from an existing entry; you neither know nor pass them.
- **Social** — **never guess a `src`.** The icon sets live in the editor's browser SDK and cannot be
  listed server-side. Call `list-email-editor-social-icons` first; it returns the images this newsletter
  already uses, most-used first.
- **Menu, social, icons, table** — **the list replaces the list.** Send every entry in the intended
  order; an empty list is rejected. Unstated properties (`target`, separator, spacing) are carried
  over from an existing entry.
- **Table** — a grid, not a flat list: **every row needs the same number of cells**, a short row is
  a hole and is rejected.
- **Divider, spacer** — finished as they are; their look is the styling level.
- **Countdown, contact card, wowing video** — arrive unconfigured and cannot be configured
  from here; the content is set in a dialog of the KlickTipp editor. There is no add tool: one would
  only have placed an empty shell that renders nothing. Point at the editor.
- **Personalised email** — and here the editor does **not** help: its insert menu does not carry
  this block, only automations place one. In a newsletter it cannot be created at all. Existing ones
  stay readable, movable and removable.

Four kinds exist in the editor but not here — **form, carousel, merge content and empty block**. No
tool, because no real specimen was found to derive a neutral initial state from. They stay with the
editor.
