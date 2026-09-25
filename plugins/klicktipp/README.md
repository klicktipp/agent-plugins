# KlickTipp

Write, review and prepare KlickTipp email newsletters from your agent, and manage
the opt-in processes of the account with their confirmation email — over the hosted KlickTipp MCP server at
`https://mcp.klicktipp.com/mcp`.

The plugin carries no API key. The endpoint sits behind OAuth and you sign in
once, interactively, on first use. See [SETUP.md](SETUP.md), or
[SETUP_LANGDOCK.md](SETUP_LANGDOCK.md) to reach the same server from a Langdock
workspace.

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
| `search-newsletters` | find newsletters, newest first, filtered by name and delivery state |
| `get-newsletter` | read one; projections add metadata, audience, content, delivery configuration and dispatch state |
| `create-newsletter-draft` | create a draft with its name and initial subject |
| `update-newsletter-draft` | name, internal note and audience of a draft |
| `delete-newsletter-draft` | discard a draft |
| `configure-newsletter-delivery` | sender name, sender address, reply address, signature |
| `send-newsletter-test` | test send to any address — the recipient becomes a tagged contact, which can start an automation |
| `prepare-newsletter-dispatch` | prepare the real dispatch and return a confirmation URL |
| `cancel-newsletter-dispatch` | take a running dispatch back — it does not unsend what already left |

**Content of one email**

| | |
|---|---|
| `get-email-editor-content` | read the stored block document of a newsletter, block by block |
| `preview-email-editor` | render the current draft and show it, unpublished changes included — the answer to "show me the preview" |
| `replace-email-editor-content-from-html` | bring in a design that only exists as HTML, once, bound to the revision you read |
| `replace-email-editor-content-from-email` | take the body of another email of the account over unchanged, in one call |
| `replace-email-editor-content-from-document` | store a finished editor document as the body — nothing is converted, so nothing is lost |
| `validate-email-editor-content` | review the assembled email before it is published |
| `publish-newsletter-email-content` | make the reviewed body the one a dispatch would send |
| `email-<block>-add` | add one block: paragraph, heading, text, button, image, list, divider, spacer, row, table, menu, social, icons, video, HTML |
| `email-<block>-write` | change the content of an existing block of that kind |
| `email-<block>-style-write` | change the styling of a block, a column, a row or the page |
| `move-email-editor-block`, `remove-email-editor-block` | move a block within the document, or take it out |
| `search-email-editor-templates` · `preview-email-editor-template` · `replace-email-editor-content-from-template` | find a design of the account's catalogue, look at one whole, and put it on an email |
| `get-email-editor-display-condition-capabilities` | what a display condition may say in this account |
| `update-email-editor-display-condition` · `configure-email-editor-row-display-condition` | write a named display condition, and bind a row to it |
| `list-email-editor-display-conditions` | which display conditions an email carries, and which rows each governs |

Each block tool names the blocks it may touch by their `uuid`, so a change reaches
exactly one block and leaves the rest of the design untouched.

**Countdown, contact card and Wowing video have no add tool.** Their content is
chosen in a dialog of the KlickTipp editor, so a tool could only place an empty
shell that rendered nothing at send time. The editor is the answer for those
three; blocks of those kinds that already exist stay readable, movable and
removable.

**Split tests** — on production. Delivery configuration, test send and
activation refuse a split test everywhere, because none of them can pick an arm

| | |
|---|---|
| `configure-newsletter-split-test` | make a newsletter a split test, and set how the winner is found |
| `add-newsletter-split-test-variant` | add a test arm, or copy an existing one |
| `update-newsletter-split-test-variant` | change an arm, its subject line above all |
| `remove-newsletter-split-test-variant` | take an arm out |

**Contacts, tags and fields** — on production

| | |
|---|---|
| `search-contacts` · `get-contact` | find contacts by tag, field value or subscription, and read one |
| `upsert-subscribed-contact` | add one contact by hand, subscribed at once and with its field values — the Add Contact screen |
| `update-contact-values` | write field values on a contact that already exists |
| `search-tags` · `get-tag` · `create-manual-tag` · `update-manual-tag` | the manual tags of the account |
| `tag-contact` · `untag-contact` | put a manual tag on a contact, or take it off |
| `search-custom-fields` · `get-custom-field` · `create-custom-field` · `update-custom-field` | the custom field definitions |

| `delete-manual-tag` · `delete-custom-field` | remove one; deleting a field takes its value out of every contact of the account, and neither can be undone |

**Opt-in** — the processes and their confirmation email. That email is the
record of consent, so the skill changes it only when exactly that was asked.

| | |
|---|---|
| `search-opt-in-processes` | list the account's opt-in processes |
| `get-opt-in-process` | read the full configuration of one |
| `create-opt-in-process` | create one, optionally as a copy; its confirmation email comes with it |
| `update-opt-in-process` | change its settings — mode, redirect pages, labels, the change-email role |
| `delete-opt-in-process` | remove one, with its confirmation email; the contacts stay subscribed |
| `get-opt-in-confirmation-email` · `update-opt-in-confirmation-email` | the sender side of the confirmation email: subject, sender, reply-to, CC/BCC, domain |
| `get-opt-in-confirmation-email-content` · `update-opt-in-confirmation-email-content` | its text, HTML and plain |
| `preview-opt-in-confirmation-email` | look at the stored email before a contact gets it |
| `send-opt-in-confirmation-email-test` | send it to one address — which becomes a tagged contact |

There is no separate delivery-status tool: where a newsletter stands with its
dispatch is the `deliveryStatus` projection of `get-newsletter`. The
subject is written once, at creation; afterwards it is changed in the KlickTipp
editor and read through the `metadata` projection.

## What it touches

Everything happens inside the KlickTipp account the login belongs to, or a
subaccount that account may support. Read tools run without a prompt; every
write tool is annotated so your agent asks first.

**No tool sends a newsletter.** `prepare-newsletter-dispatch` validates account,
permission, content, audience and sender, states who would receive it, and
returns a short-lived single-use confirmation URL. Only the logged-in person, by
opening that URL in KlickTipp and confirming there, hands the newsletter over —
and that step does reach real recipients and cannot be taken back. If a bound
value changes or the link expires, the confirmation is refused and a new one has
to be prepared.

Three writes have no undo, and the agent is expected to say so before it calls
them:

- `replace-email-editor-content-from-html` converts HTML only, and it is the entry for a
  design that exists as HTML and nowhere else -- not a way to change a newsletter.
  Social icons come back as linked images, tables as plain markup, video as a
  preview image, add-ons as their rendered output; web fonts, row background
  images and own head styles are dropped; **KlickTipp decisions and AI blocks are
  deleted beyond recovery.** The `content` projection of `get-newsletter`
  lists exactly what an import would cost for the newsletter at hand, as
  `importWarnings` — those belong in front of the user, not summarised away.
- The block tools convert nothing, so no block loses its styling or its
  editability, but `remove-email-editor-block` cannot be undone either. They are the way
  to make a change that can be named, and the ones to prefer over an import on a
  newsletter that already carries a design.
- `publish-newsletter-email-content` changes what real recipients would receive — and a test
  send shows the published body, so publishing comes before testing, not after.
- `send-newsletter-test` is no longer restricted to the account's own
  addresses, and it writes: whoever receives the test becomes a contact with a
  tag, which can trigger an automation. The agent is expected to say that before
  the step, not after.
- `delete-newsletter-draft` removes the draft with its email, audience
  conditions and system tags.

`get-opt-in-process-redirect-url` returns a URL that identifies a subscriber — it
carries subscriber ID, email address, list, subscriber key and referral link.
Treat its result as personal data.

## Skills

`skills/email` — the content of one email: what each block is and which fields it
takes, how to assemble a finished, professional email from a starting point, and
how to change an existing one block by block instead of replacing it. It also
writes HTML that the editor's HTML import turns back into editable
drag-and-drop blocks rather than one undividable wall of text — the HTML
`replace-email-editor-content-from-html` expects.

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
definitions, and create and change the opt-in processes behind them together
with their confirmation email.

`skills/email-template-generator` — writes the plain business emails that are
not newsletters: cold outreach, support replies, follow-ups, declines. No HTML,
no layout.

Each skill carries a `references/` folder with the tools it uses, their answer
shapes and their pitfalls. All of them are in German, like the editor itself.

**What the skills describe is what the server serves.** A tool that is not in
them does not exist here, and neither does the capability behind it: there is no
tool that writes an email signature — an existing one is picked through
`signatureId` in `configure-newsletter-delivery`.

The personalized email block is a case of its own: the add-on behind it is paid
for separately and the work on it is deferred, and the editor offers the block
only inside an automation — so a newsletter cannot get one at all. Blocks that already exist
stay readable, movable and removable.

## Support

support@klick-tipp.com ·
[MCP server](https://developers.klicktipp.com/guides/mcp-server) ·
[Plugins](https://developers.klicktipp.com/guides/mcp-server-plugins) ·
[Privacy policy](https://www.klick-tipp.com/datenschutz) ·
[Terms](https://www.klick-tipp.com/agb)
