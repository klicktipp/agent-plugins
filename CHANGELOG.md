# Changelog

One entry per released version. Both manifests — `.claude-plugin/plugin.json` and
`.codex-plugin/plugin.json` — carry the same version, and every version is a tag in this
repository.

The plugin is generated from the internal `agent-plugin` repository, and the version numbers are
that repository's tags: only its production build is published here, so a version that changed
nothing in the production plugin leaves no entry of its own.

## 0.10.1 — 2026-09-18

- **Two things that made the plugin directory reject the submission.** The `email` skill's
  `description` was 1198 characters against a limit of 1024 — it now keeps every trigger that is not
  covered elsewhere and drops the two that were. And the release archive held the plugin directory
  as a folder, so `.claude-plugin/plugin.json` sat one level down; it now holds the contents of that
  directory, with the manifest at the top level.

## 0.10.0 — 2026-09-18

- **Three ways into a newsletter body, and the skill says which one you are in.** The `email` skill
  described the HTML conversion as the only route, which is what sent a run through it and cost the
  dividers, the box and some images. The form the design is already in decides now: another email of
  the account is `email-content-copy`, a finished editor document is `email-content-document-import`,
  and only markup that exists nowhere else is worth a conversion. Both new routes replace the body in
  one call and convert nothing.
- **A body is not assembled from single block calls when it is new.** The skill said both things in
  two places for the same case; the slow reading took over ten minutes. Authoring now writes the
  document and stores it in one call, and the cost of the other road is named with the measured
  number rather than left as a preference.
- **The email skill loads a third of what it did** — 50k characters down to 31k. What only applies in
  one situation moved into `references/`: styling, adding blocks, the HTML case and authoring from
  nothing. Each site keeps a pointer that names the decision, so the choice of whether to go look
  stays in the skill.
- **A split test asks for its three settings** instead of filling them in as "defaults". Test size,
  duration and winner criterion settle what share of real recipients gets a test version — the one
  thing in that flow that is not a design decision. They are asked in one question, and an own choice
  is named as one.
- **A variant already carries its content revision**, so reading one just to learn its token is a
  round trip that can go.
- **Rules the tool descriptions had to give up now live in the skills** — among them: ask before
  removing a block, and ask for the subject rather than inventing it.

## 0.9.0 — 2026-09-17

- **Thirteen contact, tag and field tools go to production** — the four tag tools, the five
  contact tools, the four custom-field tools — arriving with the next production deployment.
- **And a list of what deliberately stays behind, each with its reason** rather than as one
  bucket: the two deletions, because deleting a field takes the value out of every contact of the
  account; `subscribe`, `unsubscribe` and `get-subscription-redirect-url`, because a subscription
  sends the confirmation mail, can start automations and changes who really gets post; and
  everything writing an opt-in process or its confirmation email, because that is the record of
  consent.
- `enrich-contact` is now **`update-contact`** — it never enriched, it wrote contact fields, and it
  now reads like `update-manual-tag` and `update-custom-field`.
- **A dispatch can be taken back.** `email-newsletter-cancel` exists, so `canBeCancelled` no longer
  names a state with no way out of it. It does not unsend what already left, it takes the same
  permission as handing a newsletter over, it is not on production yet — and the skill says to ask
  the person before calling it.
- **A missing unsubscribe link is a blocker, not a warning.** The publish refuses without the
  token, and nothing is sent unpublished, so the old wording sent an agent to tell people the
  dispatch would decide it. The skill names which footer placeholder blocks and which does not.

## 0.8.19 — 2026-09-17

- **The split-test tools are released.** They are in the production allowlist, so what was "not on
  production, release pending" is now "released, and there from the next production deployment on"
  — an "unknown tool" until then is the state of the deployment, not a defect. The skill also says
  what the release does *not* change: delivery configuration, test send and activation refuse a
  split test everywhere, because none of them can pick an arm.
- It also records the dead end in between, because someone will still meet it: the `splitTest`
  argument was published while the five tools were not, and a test created that way cannot be
  given its second arm from here at all — that newsletter is finished in the app.
- `email`: block alignment, and the editor's own font names rather than approximations of them.

## 0.8.16 — 2026-09-16

- **No tool adds a block only the editor can fill.** Countdown, contact card and Wowing video had
  add tools that could set an empty shell and nothing else — their content is chosen in a dialog
  of the KlickTipp editor, so what came out looked placed and rendered nothing at send time. Those
  three add tools are gone; the skills name the editor as the answer, and existing blocks of those
  kinds stay readable, movable and removable.
- **A tool called without an account works in the account the app would open** — the user's own
  where they have KlickTipp access, the one linked account where they have none, and a choice
  where there are several. The skills describe that, and the refusals a texter or a disconnected
  account gets, so the agent asks the person instead of guessing.
- **The six output schemas are published again.** A client that wants to validate an answer needs
  a machine-readable schema; deriving the shape from Markdown is not that. The references say so
  rather than claiming there is none, and stay the fuller source — a schema names fields, it does
  not explain them.
- `newsletter`: the tracking settings the screen has and the tools did not — the UTM campaign name
  through draft-update, link tracking and the KlickTipp header line through delivery-configure.
- `email`: the HTML import answer says what the conversion cost, and since the conversion is Bee's,
  only the report after it is binding.

## 0.8.14 — 2026-09-16

- **The test send takes any address now — and writes one.** It runs through the app's own test
  dialog, so the restriction to the account's own addresses is gone and the side effect is real:
  the recipient becomes a tagged contact, which can start an automation. The skill says so before
  the step rather than after it, and the published tool table follows.
- **Publish before testing.** A test send shows the published body, so an unpublished change is
  not what arrives; the skill reads the warning that says so instead of passing it over.
- `newsletter`: the sender lists are binding and the domain comes with them; and three things the
  server allows without prompting — excluding long-inactive contacts when an audience is set (with
  the limit said out loud, because tag conditions have no time axis), the imprint, and the
  transactional signature.
- `crm`: contact date fields are read the way the interface writes them — `16.09.2026`, not a
  second notation beside it. ISO 8601 still goes in on the write side, for a date that was
  computed rather than read.

## 0.8.12 — 2026-09-16

- Three add-on blocks are held back on production: **countdown**, **contact card** and
  **personalized email**. The first two add a block only the editor can finish; the personalized
  email has no fallback at all, because the editor does not offer it in its insert menu either, so
  on production it cannot be placed. The `email` skill says so where an agent actually stands when
  it reaches for one — in the tool table, in the list of add tools and in each block's own file.

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
