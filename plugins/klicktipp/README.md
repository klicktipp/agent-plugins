# KlickTipp

Write, review and prepare KlickTipp email newsletters from your agent, and read
the opt-in processes of the account — over the hosted KlickTipp MCP server at
`https://mcp.klicktipp.com/mcp`.

The plugin carries no API key. The endpoint sits behind OAuth and you sign in
once, interactively, on first use. See [SETUP.md](SETUP.md).

## Install

**Claude Code**

```bash
claude plugin marketplace add klicktipp/agent-plugins
claude plugin install klicktipp@klicktipp
claude mcp login plugin:klicktipp:klicktipp
```

**Codex** — point your plugin configuration at this directory. The `interface`
block in `.codex-plugin/plugin.json` carries the display metadata Codex expects.

Both targets read the same `.mcp.json`.

## Tools

**Newsletters**

| | |
|---|---|
| `email-newsletter-search` | find newsletters, newest first, filtered by name and delivery state |
| `email-newsletter-get` | read one; projections add metadata, audience, content, delivery configuration and dispatch state |
| `email-newsletter-draft-create` | create a draft with its name and initial subject |
| `email-newsletter-draft-update` | name, internal note and audience of a draft |
| `email-newsletter-draft-delete` | discard a draft |
| `email-newsletter-delivery-configure` | sender name, sender address, reply address, signature |
| `email-newsletter-test-send` | test send to any address — the recipient becomes a tagged contact, which can start an automation |
| `email-newsletter-send` | prepare the real dispatch and return a confirmation URL |

**Content of one email**

| | |
|---|---|
| `email-get` | read the stored block document of a newsletter, block by block |
| `email-content-import` | bring in a design that only exists as HTML, once, bound to the revision you read |
| `email-content-check` | review the assembled email before it is published |
| `email-content-publish` | make the reviewed body the one a dispatch would send |
| `email-<block>-add` | add one block: paragraph, heading, text, button, image, list, divider, spacer, row, table, menu, social, icons, video, HTML, personalized email |
| `email-<block>-write` | change the content of an existing block of that kind |
| `email-<block>-style-write` | change the styling of a block, a column, a row or the page |
| `email-block-move`, `email-block-remove` | move a block within the document, or take it out |

Each block tool names the blocks it may touch by their `uuid`, so a change reaches
exactly one block and leaves the rest of the design untouched.

**Countdown, contact card and Wowing video have no add tool.** Their content is
chosen in a dialog of the KlickTipp editor, so a tool could only place an empty
shell that rendered nothing at send time. The editor is the answer for those
three; blocks of those kinds that already exist stay readable, movable and
removable.

**Split tests** — ⚠ not released on production yet; calling one there answers
"unknown tool", which is the pending release and not a defect

| | |
|---|---|
| `email-split-test-configure` | make a newsletter a split test, and set how the winner is found |
| `email-split-test-variant-add` | add a test arm, or copy an existing one |
| `email-split-test-variant-update` | change an arm, its subject line above all |
| `email-split-test-variant-remove` | take an arm out |

**Contacts, tags and fields** — ⚠ not released on production yet, same as the
split tests above

| | |
|---|---|
| `search-contacts` · `get-contact` | find contacts by tag, field value or subscription, and read one |
| `subscribe` · `unsubscribe` | take a contact into an opt-in process, or out of the account's mailings |
| `enrich-contact` | set field values on a contact that already exists |
| `search-tags` · `get-tag` · `create-manual-tag` · `update-manual-tag` · `delete-manual-tag` | the manual tags of the account |
| `assign-manual-tag` · `remove-manual-tag` | put a manual tag on a contact, or take it off |
| `search-custom-fields` · `get-custom-field` · `create-custom-field` · `update-custom-field` · `delete-custom-field` | the custom field definitions |

**Opt-in** — reading works on production; changing and deleting a process is the
web interface's job there

| | |
|---|---|
| `search-opt-in-processes` | list the account's opt-in processes |
| `get-opt-in-process` | read the full configuration of one |

There is no separate delivery-status tool: where a newsletter stands with its
dispatch is the `deliveryStatus` projection of `email-newsletter-get`. The
subject is written once, at creation; afterwards it is changed in the KlickTipp
editor and read through the `metadata` projection.

## What it touches

Everything happens inside the KlickTipp account the login belongs to, or a
subaccount that account may support. Read tools run without a prompt; every
write tool is annotated so your agent asks first.

**No tool sends a newsletter.** `email-newsletter-send` validates account,
permission, content, audience and sender, states who would receive it, and
returns a short-lived single-use confirmation URL. Only the logged-in person, by
opening that URL in KlickTipp and confirming there, hands the newsletter over —
and that step does reach real recipients and cannot be taken back. If a bound
value changes or the link expires, the confirmation is refused and a new one has
to be prepared.

Three writes have no undo, and the agent is expected to say so before it calls
them:

- `email-content-import` converts HTML only, and it is the entry for a
  design that exists as HTML and nowhere else -- not a way to change a newsletter.
  Social icons come back as linked images, tables as plain markup, video as a
  preview image, add-ons as their rendered output; web fonts, row background
  images and own head styles are dropped; **KlickTipp decisions and AI blocks are
  deleted beyond recovery.** The `content` projection of `email-newsletter-get`
  lists exactly what an import would cost for the newsletter at hand, as
  `importWarnings` — those belong in front of the user, not summarised away.
- The block tools convert nothing, so no block loses its styling or its
  editability, but `email-block-remove` cannot be undone either. They are the way
  to make a change that can be named, and the ones to prefer over an import on a
  newsletter that already carries a design.
- `email-content-publish` changes what real recipients would receive — and a test
  send shows the published body, so publishing comes before testing, not after.
- `email-newsletter-test-send` is no longer restricted to the account's own
  addresses, and it writes: whoever receives the test becomes a contact with a
  tag, which can trigger an automation. The agent is expected to say that before
  the step, not after.
- `email-newsletter-draft-delete` removes the draft with its email, audience
  conditions and system tags.

`get-subscription-redirect-url` returns a URL that identifies a subscriber — it
carries subscriber ID, email address, list, subscriber key and referral link.
Treat its result as personal data.

## Skills

`skills/email` — the content of one email: what each block is and which fields it
takes, how to assemble a finished, professional email from a starting point, and
how to change an existing one block by block instead of replacing it. It also
writes HTML that the editor's HTML import turns back into editable
drag-and-drop blocks rather than one undividable wall of text — the HTML
`email-content-import` expects.

`skills/newsletter` — the hull around that content: draft, audience, sender and
reply address, test send, and the dispatch confirmation.

`skills/splittest` — A/B tests: make a newsletter a split test, add and copy
test arms, set a subject line per arm, and read what changes once a newsletter
is one.

`skills/dashboard` — reads the numbers of an account — reach, delivery, opens,
clicks, bounces, unsubscribes of the last dispatches — and builds a dashboard
out of them. Read-only: it creates, changes and sends nothing.

`skills/crm` — the contact data of the account: find, read, subscribe and
unsubscribe contacts, set field values, manage manual tags and custom field
definitions, and read the opt-in processes behind them. On production only the
two opt-in reads are released so far; the skill says so rather than letting an
agent hunt for a defect.

`skills/email-template-generator` — writes the plain business emails that are
not newsletters: cold outreach, support replies, follow-ups, declines. No HTML,
no layout.

Each skill carries a `references/` folder with the tools it uses, their answer
shapes and their pitfalls. All of them are in German, like the editor itself.

**What is not on production yet** — the split tests, the contact and tag tools,
the image tools, the `email-signature-*` family, and the personalized email. All four are documented in
the skills that use them, each with the note that an "unknown tool" there is the
pending release and not a defect. What does work on production is picking an
existing signature through `signatureId` in
`email-newsletter-delivery-configure`.

## Support

support@klick-tipp.com ·
[Documentation](https://klicktipp.github.io/agent-plugins/) ·
[Privacy policy](https://www.klick-tipp.com/datenschutz) ·
[Terms](https://www.klick-tipp.com/agb)
