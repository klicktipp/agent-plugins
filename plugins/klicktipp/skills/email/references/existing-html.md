# Editing existing HTML, and writing HTML for the import

You land here when finished email HTML is at hand — from an agency, another tool, a file — and it is
to be changed or imported. For a newsletter that already exists as a document this is the wrong way;
`replace-email-editor-content-from-email` or `replace-email-editor-content-from-document` get there without loss.

When email HTML already exists, the task is a content change, not a redesign. Change only what was
requested in terms of content. The rest of the document stays identical character for character.

What is content and may be changed:

- Texts, headings, list items, table cells, a visible preview line inside the document. (The email's
  **pre-header field** is not in the document — it is set through `update-newsletter-draft`,
  field `preheader`.)
- Button labels and link targets, `href`, `alt` texts, image URLs.
- KlickTipp variables and system links.

What is design and stays untouched:

- Structure and order of rows, columns and blocks; column count and widths.
- All classes, including the `block-[n]` numbering, and all attributes such as `width`, `align`,
  `cellpadding`.
- Inline styles, colours, fonts, font sizes, line heights, padding, spacing, borders.
- Spacers, dividers, wrapper tables — even apparently superfluous ones.

While editing, also:

- No tidying up on the side: no reformatting of the code, no reordering of attributes, no
  harmonising of styles, no removal of "unnecessary" nesting, no renumbering of blocks.
- If the existing HTML breaks a rule of this skill — an `http` image URL, a background image, a
  `menu_block` — do not rebuild it on your own authority but name it in one sentence after the code
  block. The exception is errors that necessarily break the import or storage: a missing `DOCTYPE`, a
  missing `<meta charset="UTF-8">`, missing mandatory footer variables, and invalid HTML such as an
  unclosed or crossed tag. Correct those and name the correction.
- If the new content needs more room than the layout allows, adjust the text, not the layout. If that
  does not work sensibly, name the conflict and ask for the layout change you should make.
- Change design only when explicitly asked — "make the button green", "two columns instead of one",
  "more space above the heading". Then make exactly that change and nothing beyond it.
- If it is unclear whether an instruction means content or design, treat it as content and ask the
  design question.

If no existing HTML is at hand, you design freely by the rules below.

## Contents

- Writing import HTML
- What the import does, reports and costs

## Writing import HTML

As soon as you produce HTML that goes through `replace-email-editor-content-from-html` — editing existing email HTML or
making foreign HTML importable — **read `references/html-authoring.md` first**. That is where the
mandatory rules live: the scaffold, the twelve-column grid, the editor's block classes, what is
permitted in CSS and images, the KlickTipp variables, the mandatory footer, valid HTML, and the
quality check before output.

They are neither optional nor summarisable: HTML that breaks them is either not imported at all or
imported as a lump that can no longer be edited. Do not rely on knowing them — they are five screens
long, and the difference is in the details.

For changes through the block tools they do **not** apply: nothing is converted there.

## What the import does, reports and costs

**What `importWarnings` says in a read response.** It is the cost list **of an HTML import** onto this
particular newsletter — and only that. It does not apply to editing: nothing is converted there, so no
block loses styling or editability. Read it out to the user **before** you import, never as a comment
on a change. Empty means a conversion would cost nothing here.

**An import over existing content is rejected on the first call** — deliberately. The response counts
how many rows and blocks the newsletter has and of what kinds, and changes nothing. Only a second
call with `replaceExistingContent: true` converts. Show the user that list and let them decide: an
import over a designed newsletter takes every block, its layout and the identity of every block with
it, and there is no way back. An empty draft needs no confirmation.

**The import does not publish.** It stores the draft; the dispatch content only changes through
`publish-newsletter-email-content`. The response says exactly that in `nextAction` — read it instead of
reporting "done" after the import.

**What an HTML import costs** (`replace-email-editor-content-from-html`). An import takes rendered HTML and never the
document; per block it comes back as: a divider as a styled line, a menu as links, social links and
icons as images with links, a table as plain markup, a video as a preview image with a link, custom
HTML, carousel, merge content and add-ons (countdown, contact card, wowing video, signature)
as their rendered result; web fonts, row background images and custom head styles are dropped.

**After the import the result's `warnings` say what this one conversion actually cost** — not as a
forecast but counted on both sides. Always included: the layout has been rebuilt, rows, columns and
spacing are the editor's afterwards, and there are spacers in it nobody sent. Plus one line with
numbers each for dividers, lists, tables, images and videos that did not come back as their own
block, together with the tool to restore them. A table whose cells run together as `cell Acell B` is
exactly there. Pass those lines on; an "import worked" without them is the report that lets the user
discover the loss in the editor.

**Do not promise beforehand what will become of an HTML.** The conversion is done by an external
service; what becomes of a table or a divider is not decided by KlickTipp, and it can change without
anything being shipped here. The list above is therefore an expectation, not a contract — what is
binding is always the report **after** the import. Phrase it accordingly: "in our experience
something like that does not survive the conversion" before the call, and the measured lines after.

The import leaves **name, subject and pre-header untouched** — it writes only the document. A
`<title>` in the imported HTML lands nowhere, and a hidden pre-header line is discarded by the
converter. Name, subject and pre-header are set by the skill `newsletter` through its own tools.

And decisions as well as AI blocks are **gone** after an import: they are not in the HTML, and no
approach of yours can preserve them — say so explicitly before you import. In the document they are
very much there, and editing leaves them untouched: that is the reason never to change a designed
newsletter through HTML.

**The list is a lower bound, not a complete enumeration.** Not included but demonstrated: spacing,
borders, rounding and inline colours are not preserved, padding shifts further with every pass, and
the layout is normalised — column count, additional spacer blocks and a changed content width have
all occurred. Pass that sentence on too: a list that sounds complete is worse than none.
