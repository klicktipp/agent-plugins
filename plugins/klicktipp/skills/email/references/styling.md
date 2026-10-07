# Styling

You land here when colours, spacing, borders, widths, alignment or type need to change. For a pure
text change you do not need this file — `update-email-editor-text` handles that and leaves the styling
alone.

**Styling works, in named values, never in CSS.** Four levels for everything every block has (page,
row, column, block), and three tools for what **only one kind** has: the height of a spacer, the
line and width of a divider, the look of a button. A kind-bound tool on another kind is rejected — a
heading has no height. Together they set colours, padding, borders, alignment, widths, corner radii
and per-device visibility. A colour is `#RRGGBB`, `#RGB` or `transparent`, a spacing an integer
number of pixels 0–400, a width 320–1440, a border `1px solid #000000`. A CSS declaration is
rejected — it could carry `background-image: url(...)` into the email. Every tool writes only what
you name; everything else stays. Style writes are **absolute**: "make the background white" needs no
read, "eight pixels more padding" does — that is what `styleOutline` is for.

**In `styleOutline` a block carries two cards.** `style` is the outer spacing and alignment every
block has; `kindStyle` is what only this kind has — a spacer's height, a divider's line, a button's
whole look. Kept apart because both carry a `paddingTop` and it is not the same spacing: once around
the button, once inside it. `kindStyle` is `null` for every kind without its own style tool. An
empty card means "nothing is set here", not "nothing works here": the editor applies its defaults at
render time, not into the document.

State plainly what still does **not** work, rather than working around it: the column widths of an
existing row (a row's columns are equally wide; an uneven split comes from the editor), removing a
row, and the **width of an image or video** — that sits in the document as two coupled values plus a
class token, and setting one of them alone pulls editor and rendering apart; the editor is the way
there. The typography of a text block does not belong here either: it sits in that block's own
markup, so in `update-email-editor-text` — offering it in two places would mean two answers to one question.

**Which field a block kind has, which tool writes it and what to watch out for is in
`references/blocks.md`, one row per kind.**
