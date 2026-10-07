# Creating a block

You land here when a block is to be **added** to a draft that already stands. You do not build a
whole body this way (see "Filling a body" in `SKILL.md`), and to change an existing block you do not
need this file.

Two things surprise people here regularly: some blocks arrive empty and cannot be filled from here,
and a new block inherits its look from a neighbour you did not choose.

**Read the `warnings` of the write response and pass them on.** A block is stored even when it shows
nothing — that is deliberate, because it is a legitimate intermediate state on the way to a block a
human finishes in the editor. But it is stated, in the response: a video without `thumbSrc`, a list
without `<ul>`/`<ol>`, an unconfigured add-on. Never report "added" when the response tells you the
block stays empty — say what is still missing and where it gets set.

**Countdown, contact card and wowing video cannot be inserted.** Their content comes into
being in a dialog of the KlickTipp editor, and no tool here reaches it. There used to be add tools
for them; they placed an empty shell that showed nothing on dispatch, and that is exactly why they
are gone. If one of these blocks is wanted, the answer is the editor — name it, instead of
approximating a countdown out of text and an image and presenting it as one. Existing blocks of
these kinds stay readable, movable and removable.

**The personalised email can no longer be inserted either, as of 2026‑09‑18** — and here the reason
lies elsewhere: nothing is wrong with the block, the add-on behind it is paid and the work on it is
postponed. `email-personalized-email-add` and `email-personalized-email-write` were therefore
dropped; the write tool had also shipped with a reported defect (an update of the name alone was
rejected with "carries no prompt").

State the difference when someone asks: **the editor does not help here.** Its insert menu does not
carry this block — only automations place one. In a newsletter it cannot be created at all. Existing
blocks stay readable, movable and removable; their instruction is changed in the editor.

**Adding: the new block looks like a block of the same kind — but not necessarily like its
neighbour.** On creation the server copies the `style` object and the padding from the **first**
block of the same kind it finds: first in the same column, then in the same row, then anywhere in
the newsletter. *First*, not *nearest* — the insert position plays no part. What sits in the `html` —
wrapper, `<p style=…>`, font sizes — it does **not** copy; that is your part: take the `html` of the
neighbouring block of the same kind (preferably from the same row or the section the new block goes
into — not the preview line, not the footer) as a template and replace only the words. Invent
nothing: no values that are not in the document, no `font-family` from memory, no sizes you consider
suitable.

Two things remain:

1. If the newsletter has **no** block of that kind, there is nothing to read off — then the new block
   carries the values of its initial state, and your `html` comes without a template: plain markup
   (`<p>`, `<strong>`, `<a href>`), nothing invented. Say so instead of reporting a finished result.

   **Two exceptions: the text colour and the link colour.** Paragraph, heading, text, list and table
   then take the page's text colour (`update-email-editor-page-style`, `textColor`) instead of their initial
   state's; paragraph, text, list and table also its link colour (`linkColor`). Without that, a
   freshly created paragraph carried the `#555555` and the `#4768ef` of the foreign newsletter the
   initial state once came from, and the configured page colours had no effect — both reported
   exactly that way on staging.

   Two blocks are deliberately **not** included. The button: its label colour belongs to its frame,
   not to running text. The menu: its entries *are* links, so text and link colour are one look there
   — replacing one half leaves a menu that no longer matches itself. The heading carries no link
   colour of its own.

   The order therefore matters: **`update-email-editor-page-style` first, then create the blocks.** The
   colours are written into the block on creation, not inherited later — a page colour changed
   afterwards does not reach existing blocks, neither through the tools nor in the editor, because a
   block renders its own colours.
2. Several new blocks cost several calls: an add creates **one** block and returns the new revision
   the next one works with. Since every add brings its content along, that is one call per block —
   no second one to fill it.
3. **A run of adds makes a run of identical blocks.** As soon as the first new paragraph is in the
   column, *it* is the first of its kind for the second — and its spacing travels through the whole
   run. Ten paragraphs inserted this way all carry the same padding, while a designed draft varies
   its spacing from section to section. That is visible as a jump in the design, and has been in
   practice.
