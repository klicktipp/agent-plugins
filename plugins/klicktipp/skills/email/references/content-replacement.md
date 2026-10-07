# Replacing content — a procedure

The most common request and the one that breaks the most: "here is the new text, put it into the
newsletter". This happened: an agent removed a divider, the video button, a sub-heading and a
paragraph because the text file did not mention them. The request was "replace the text", the result
was a different design.

**The rule of thumb:** after a text replacement the newsletter has **the same number and order of
blocks as before**, only with different text. If your result differs, it was not a text replacement
— and then the user had to agree first.

## The procedure

1. **`get-email-editor-content` with `contentOutline`.** Not `content`: you need the uuid, kind and current value
   of every writable field, which is exactly what the outline is — at a quarter of the bytes.
2. **Write down the mapping before you write anything.** Which section of the source belongs to
   which uuid? Make that a list, and a complete one: including the blocks the source has nothing
   for, and the parts of the source that have no block.
3. **Name the cases that are not a pure replacement** (below) and let the user decide before
   anything is written.
4. **Write.** All text blocks in **one** `update-email-editor-text` — it takes a list. A button gets its
   `label`/`href` through `update-email-editor-button`, an image its `src`/`alt` through
   `update-email-editor-image-block`.
5. **Report what you did not touch**, not only what you changed.
6. **Publish** with `publish-newsletter-email-content` if the user wants it — otherwise it stays a draft, and
   that is fine too.

## The four cases that are not a pure replacement

| Case | What to do |
| --- | --- |
| The source has **less** text than the newsletter has blocks | Fill what can be filled, in order, and **name** the rest: "three paragraphs and a sub-heading have no new text; I left them unchanged. Should they go?" |
| The source has **more** text than there are blocks | Add (`add-email-editor-paragraph` and siblings), do not merge paragraphs. The new block needs its neighbour's markup as a template. |
| The source calls for **another kind** — a paragraph should become a heading | A kind cannot be written: remove and create, and tell the user the old block disappears in the process. |
| The source calls for **styling** — "make the heading blue" | Colour inside text sits in the markup (`update-email-editor-text`), background and spacing are the style tools. Two different ways, do not guess. |

## What is never part of a text replacement

Divider, spacer, image, video, button, menu, icons, social links, table and the add-ons carry no
running text a text source could replace. On "replace the text" they are **neither removed nor
moved**. A button gets at most a new `label`/`href` when the source names one.

`remove-email-editor-block` only on an explicit request, named block by block. Never because something is
"left over", "looks empty" or "does not fit any more". There is no undo.

## When the whole design is new instead

Then it is not a replacement but an import: `replace-email-editor-content-from-html` with the HTML. That is the only
way for a design that exists **only** as HTML — and it costs what `importWarnings` lists in the read
response. Read that out to the user **before** you import. Never push edited HTML through the import
to apply a change.

## Before publishing

`validate-email-editor-content` runs over the whole body in one call: images without alt text, buttons without
a target, empty text blocks, never-configured add-ons, insufficient contrast, missing footer
placeholders. Pass the findings on instead of fixing silently — pale text can be intended. An
unconfigured add-on is the exception you cannot fix at all: the user makes that choice in the
editor.
