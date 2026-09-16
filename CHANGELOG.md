# Changelog

One entry per released version. Both manifests — `.claude-plugin/plugin.json` and
`.codex-plugin/plugin.json` — carry the same version, and every version is a tag in this
repository.

The plugin is generated from the internal `agent-plugin` repository, and the version numbers are
that repository's tags: only its production build is published here, so a version that changed
nothing in the production plugin leaves no entry of its own.

## 0.8.11 — 2026-09-16

- **Corrected what production actually offers.** 0.8.3 and 0.8.10 listed the split-test tools and
  the contact, tag and field tools as if they were available; they are not released on production
  yet, and neither are the image tools nor the `email-signature-*` family. The tool table marks
  each of them, and the plugin description is back to what production does: newsletters, and
  reading the opt-in processes.
- `crm`: on production the opt-in processes are read, not written — `update-opt-in-process` and
  `delete-opt-in-process` are missing there too, so the skill points at the web interface for
  changing and deleting one instead of enumerating which writer is out this week.

## 0.8.10 — 2026-09-16

- **Every skill carries its own tool reference.** A `references/` folder per skill holds the tools
  that skill uses, the answer shapes they publish and the pitfalls they have — generated from the
  tool list rather than remembered. Tools not released on production are marked as such instead of
  by environment. (0.8.4 – 0.8.6)
- **New skill `crm`** — the contact data of the account: find, read, subscribe and unsubscribe
  contacts, set field values, manage manual tags and custom field definitions, and read the opt-in
  processes behind them. The published tool table and the plugin description follow. (0.8.6)
- Opt-in: changing and deleting a process is described, along with the redirect parameters, the
  confirmation email and the tracking pixel. (0.8.9, 0.8.10)
- `email`: the image folders and the two upload tools (the file with its form, the URL on its
  own), the page font versus the row frame, and the content check now reporting unconfigured
  add-ons. (0.8.7 – 0.8.10)
- `splittest`: the read tool, which also takes an arm's email ID, plus what a test run turned up.
  (0.8.8)
- Signatures are documented as the `email-signature-*` family with their placeholder rules, but
  they are **not released on production** — an "unknown tool" there is the pending release, not a
  defect. (0.8.5)

## 0.8.3 — 2026-09-14

- **Split tests.** `email-split-test-configure` makes a newsletter a split test and says how the
  winner is found; `email-split-test-variant-add`, `-update` and `-remove` manage the arms, with
  the subject line per arm. The new `splittest` skill explains what changes once a newsletter is
  one — a tool refusing with `split_test_not_supported` is almost never a defect, it is the wrong
  address. (0.7.x)
- **A newsletter's preheader** is documented, and name, subject and preheader are read out of the
  HTML before it is imported. (0.7.x)
- **New skill `dashboard`** — reads an account's numbers (reach, delivery, opens, clicks, bounces,
  unsubscribes of the last dispatches) and builds a readable dashboard from them. Read-only: it
  creates, changes and sends nothing. (0.8.0 – 0.8.2)
- **New skill `email-template-generator`** — the plain business emails that are not newsletters:
  cold outreach, support replies, follow-ups, declines. No HTML, no layout. (0.8.3)
- Upstream the plugin is built one per environment, installable by either host, and production is
  plainly `KlickTipp`. Nothing changes for this repository, which only ever ships production.
  (0.7.x)

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
- The Codex manifest follows: its listing text describes the block tools and names both skills,
  and CI now checks that the skills declaration does not drift between the two manifests.
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
