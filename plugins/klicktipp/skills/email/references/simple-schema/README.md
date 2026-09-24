# The editor SDK's simple schema, verbatim

The upstream JSON Schema files of the **simple schema**, copied unchanged so an agent can read what
the format actually allows instead of inferring it from examples. The source and the licence below
name the vendor because the licence requires it; everywhere else this is the editor's schema.

| | |
| --- | --- |
| Source | <https://github.com/BeefreeSDK/beefree-sdk-simple-schema> |
| Commit | `355d8efc0cc558ee04d1cc1535c10e084a3a1989` (2026-01-15) |
| Licence | Apache License 2.0 — see `LICENSE` |
| Changes | none; the files are byte-for-byte the upstream ones |

## What is in here

`simple_unified.schema.json` is the whole family in one file and the one to read when a single
lookup is wanted. The rest are the individual pieces: `simple_template`, `simple_row`,
`simple_column`, and one per block — `simple_title`, `simple_paragraph`, `simple_list`,
`simple_html`, `simple_image`, `simple_button`, `simple_menu`, `simple_icons`, `simple_divider`.
`definitions.schema.json` holds the constraints they share (padding, border radius, border width).
`example_valid_request.json` is a complete, valid document — usually faster than the schema when
the question is "what does one of these look like".

## Read `../simple-schema-catalog.md` first

This is the **input** form for generating a design, not the form a KlickTipp email is stored in,
and the two disagree on purpose: ten block types against nineteen kinds, properties on the module
against content inside `descriptor`, constrained integers against CSS strings, no ids against a
uuid on every row, column and module. Validating a stored document against these files will refuse
most real newsletters. The catalogue next to this folder lists the traps.

## Why they are worth having anyway

Two reasons, and neither is validation of stored documents.

The first is that they are the only authoritative statement of what a block may contain. They
already earned their place once: the icon schema names `image`, `width`, `height` and
`textPosition` as **mandatory per icon**, which is why `update-email-editor-icons` builds an entry by
copying one the block already has and replacing only the named leaves — an entry assembled from
scratch would go out without them, and the editor would open the block empty.

The second is that this is the shape a generation path would speak if KlickTipp ever grows one
beside the HTML import. The HTML import costs fidelity by converting; a design handed over in this
form would not.
