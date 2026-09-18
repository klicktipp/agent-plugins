# The simple schema — and why it is not the stored document

The editor SDK publishes a second, much smaller document family called the **simple schema**. It is
the *input* form for generating a design (an AI-oriented description of a template), not the form
an email is stored in.

**Do not validate a stored document against it.** They disagree on purpose, and the disagreements
are exactly the traps:

| | simple schema (generation input) | stored document (what an email holds) |
| --- | --- | --- |
| root | `template` with `rows`, `settings`, `metadata` | `page` with `body`, `rows` — or the page itself, unwrapped |
| module identity | a short `type` such as `button`, `heading` | a prefixed type, kind appended (see `blocks/`) |
| module inventory | **10** types, see `typeOfModules` below | **19** kinds plus the add-ons |
| content | properties on the module | inside the module's `descriptor` |
| numbers | constrained (`padding` 0–60, `borderRadius` 0–60, `borderWidth` 0–30) | CSS strings such as `"10px"`, unconstrained |
| ids | none | `uuid` per row, column and module |

The most consequential difference is the inventory. The simple schema's `typeOfModules` knows
`button`, `divider`, `heading`, `html`, `icons`, `image`, `list`, `menu`, `paragraph`, `title` —
and therefore **not** `social`, `table`, `form`, `carousel`, `merge-content`, `spacer`, `empty`,
`video` or `addon`. A reader that treats it as the list of what an email can contain will refuse or
misname most real newsletters. `blocks/` next to this file is the inventory that
matches stored documents.

Note also that `heading` and `title` both exist there, while a stored document uses `heading` for
the block and carries the level inside the descriptor.

## What is in this folder

| File | Content |
| --- | --- |
| `document-skeleton.json` | key skeleton of a **stored** document, both shapes explained |
| `blocks/` | one file per stored module kind: its product term, its tools, its fields, and what a round trip costs it |
| `bee-simple-schema/` | the upstream schema files, verbatim and Apache-2.0 licensed: the unified schema, one per block, the shared `definitions.schema.json` and a complete valid example. See its README |

## The rest of the upstream catalog

The family is mirrored in full next to this file, so nothing has to be fetched to read a
constraint:

- Layout — `simple_template.schema.json`, `simple_row.schema.json`, `simple_column.schema.json`
- Blocks — `simple_button.schema.json`, `simple_divider.schema.json`, `simple_html.schema.json`,
  `simple_icons.schema.json`, `simple_image.schema.json`, `simple_list.schema.json`,
  `simple_menu.schema.json`, `simple_paragraph.schema.json`, `simple_title.schema.json`
- Shared — `definitions.schema.json`, which every one of them references, plus
  `simple_unified.schema.json` with the whole family in one file and `example_valid_request.json`

Only `form_validation_schema.json`, the row metadata and the comment schemas are not here; they
exist upstream as documentation pages and are worth fetching if a task really needs them.

Mirrors go stale: treat the copy here as a snapshot for orientation and re-fetch upstream before
relying on a constraint. The stored-document rules in `SKILL.md` do not depend on it — they were
derived from real stored documents and from the platform's own constants.
