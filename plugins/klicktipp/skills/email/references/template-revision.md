# Revising a large editor template

Use this when the user has chosen a design but the supplied copy calls for many coordinated row
removals or structural changes. A simple text swap still follows `content-replacement.md`; a single
block removal still uses its block tool. This route is for a deliberate redesign of the existing
stored document, not for importing rendered HTML back into the editor.

1. Read `get-email-editor-content` with `content` and the current `contentRevision`. Read
   `contentOutline` if it helps map visible text to UUIDs. For conditional content, read
   `list-email-editor-display-conditions` as well; the outline alone does not show every binding.
   Inspect the actual template preview, including text embedded in images, links and footer.
2. Map each source section to a row or block. List what will be retained, changed and removed.
   Confirm the losses that the user's request did not already authorize. Prefer a shorter template
   when the selected one would require extensive demolition.
3. Check the live contract for `replace-email-editor-content-from-document`. Work from the stored
   document, preserving the valid root form (`page` wrapper or page itself), untouched UUIDs,
   styles, add-on data, links and display-condition structure. Remove only the named rows or blocks;
   edit only the mapped fields. Do not round-trip through HTML, which discards editor structure.
   If the document cannot be transformed reliably, stop before writing and explain the limitation.
4. Submit one complete document with the current revision. A replacement refusal or overwrite
   guard is a safety checkpoint, not a precise list of every changed field. Compare the planned
   document with the source before retrying with any replacement flag. Do not infer from a
   `created` list that every retained element survived unchanged.
5. Independently read back the stored `content` and compare retained UUIDs, row order, styles,
   links, footer and add-ons with the baseline. Read display conditions again and check their row
   bindings and segment logic. Check that the new copy is complete and no unwanted demo text or
   placeholder image remains. Treat a mismatch as unfinished work, even if the write succeeded.
6. Run `validate-email-editor-content` and show the actual `preview-email-editor` result. Validation
   does not certify the visible design. Publish only if the user requested publication or the next
   authorized newsletter step needs published content; then verify the published state separately.

Do not describe an HTML import warning or overwrite guard as an exact loss report for this document
change. Do not claim a product bug is fixed because the skill prevented one agent mistake.
