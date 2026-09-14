# Changelog

One entry per released version. Both manifests — `.claude-plugin/plugin.json` and
`.codex-plugin/plugin.json` — carry the same version, and every version is a tag in this
repository.

The plugin is generated from the internal `agent-plugin` repository, and the version numbers are
that repository's tags: only its production build is published here, so a version that changed
nothing in the production plugin leaves no entry of its own.

## 0.6.3 — 2026-09-11

- **The content of an email is edited block by block.** `email-newsletter-content-edit` is gone;
  in its place a tool per block kind — `email-paragraph-add`, `email-button-write`,
  `email-image-add`, `email-row-style-write`, `email-block-move`, `email-block-remove` and the
  rest — each addressing blocks by their `uuid`. Reading is `email-get`, importing HTML
  `email-content-import`, publishing `email-content-publish`, and `email-content-check` reviews
  the assembled email before it goes out. (0.6.0)
- **Two skills instead of one.** `email-erstellung` is split: `email` carries the content of one
  email — what each block is, which fields it takes, how to assemble a finished email from a
  starting point and how to change an existing one — and the new `newsletter` carries the hull
  around it: draft, audience, sender and reply address, test send, dispatch confirmation. (0.6.0,
  0.6.1)
- The `email` skill ships a design brief and a parts bin rather than more templates, with the
  per-kind styles documented per block, and it says what each block *is*, not only which fields it
  has. (0.6.0)
- The skill no longer makes the agent re-read after every write, and it says what fits into one
  call. (0.6.0)
- Fixes: no add-on blocks nobody asked for, the content check is performed rather than merely
  offered, the image library lists rather than searches, and the block-tool corrections reached
  the files the agent actually reads. (0.6.2, 0.6.3)

## 0.5.0 — 2026-09-09

- Every environment gets its own MCP server name upstream; production keeps the unsuffixed one, so
  the tool names in this plugin stay as they are.
- `email-erstellung`: changing the words of a text block keeps the block's **stored markup**. A
  block carries most of its look inside its own `html` — the wrapper, `<p style=…>`, `<span
  style=…>` — so a bare `<p>New text</p>` would throw away font size, line height and colours. The
  skill now takes the block's own `html` as the template and replaces the words only. (0.4.5,
  0.4.6)
- `email-erstellung`: corrected what `addModule` copies. The server takes the `style` object and
  the padding from the nearest block of the same kind, but not what sits inside the `html` — that
  part is the caller's, taken from a neighbouring block rather than invented. (0.4.4)

## 0.4.3 — 2026-09-08

- `email-erstellung`: the two structure operations are described, together with the way to build a
  newsletter out of them. (0.4.2, 0.4.3)

## 0.4.1 — 2026-09-08

- `email-erstellung`: states that the personalized email is written complete, and what it costs to
  add one.

## 0.4.0 — 2026-09-08

- DEV-10830: import once, edit afterwards — no full replacement any more.
- The skill ships a professional template to generate from, with its reference files.
- The two fields a video block takes are named.
- `replaceWarnings` is described as it behaves today.

## 0.3.1 — 2026-09-08

- `email-erstellung`: what a text replacement may and may not touch.

## 0.3.0 — 2026-09-07

- `email-erstellung`: the tools hand out the stored block document, not HTML — and the skill reads
  it that way. `content` is the editable draft with its revision, `publishedContent` the active
  dispatch template.

## 0.2.7 — 2026-09-07

- Fixes.

## 0.2.6 — 2026-08-31

- The skill is named `email-erstellung` — the plugin already says KlickTipp.

## 0.2.5 — 2026-08-31

- The plugin source is named `klicktipp` rather than `kt-app`.

## 0.2.4 — 2026-08-31

- Plugin, connector and skill are named after KlickTipp, not after the tooling.

## 0.2.3 — 2026-08-28

- The login instructions are split by install path.

## 0.2.2 — 2026-08-28

- The one-time MCP login is documented, with the prefixed server name.

## 0.2.0 — 2026-08-28

- Archives are named after the tag; the icon comes from the official logo. (0.2.0, 0.2.1)

## 0.1.0 — 2026-08-28

- First public release: the KlickTipp plugin for Claude Code and Codex, as a one-plugin
  marketplace, pointing at the production MCP server (`https://mcp.klicktipp.com/mcp`).
- Scope is newsletters and opt-in processes: drafts, drag-and-drop content, audience, sender, test
  sends and the dispatch confirmation, plus reading the account's opt-in processes.
- Ships the `email-erstellung` skill with its reference files, a `SETUP.md`, and the documentation
  page published through GitHub Pages. (0.1.0 – 0.1.2)
