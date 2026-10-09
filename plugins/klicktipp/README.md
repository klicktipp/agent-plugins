# KlickTipp

Write, review and prepare KlickTipp email newsletters from your agent, build
and change its automations, manage the opt-in processes of the account with
their confirmation email, and read its statistics — over the hosted KlickTipp MCP server at
`https://mcp.klicktipp.com/mcp`.

The plugin carries no API key. The endpoint sits behind OAuth and you sign in
once, interactively, on first use. See [SETUP.md](SETUP.md). The same server and
skills work without the plugin in [opencode](SETUP_OPENCODE.md),
[OpenClaw](SETUP_OPENCLAW.md) and [Langdock](SETUP_LANGDOCK.md) — each guide carries
a prompt that has the host set both up itself.

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
| `send-newsletter-test` | test send to any address — the recipient becomes a tagged contact, which can start an automation; for a split test, one variant per call |
| `prepare-newsletter-dispatch` | prepare the real dispatch and return a confirmation URL |
| `cancel-newsletter-dispatch` | take a running dispatch back — it does not unsend what already left |

**Signatures and sender domains**

| | |
|---|---|
| `search-signatures` · `get-signature` | the signatures a newsletter can carry, and one with its text, sender profile, tags and business card |
| `create-signature` | create one, or copy an existing one |
| `update-signature` | name, internal note, labels and digital business card |
| `replace-signature-content` | replace its text — it is appended at send time, so every future send that carries it changes |
| `configure-signature-delivery` | its tags and sender profile |
| `list-sender-domains` · `get-sender-domain` | the account's sender domains and their verification state |
| `get-sender-domain-dns-setup` | the DNS records a domain needs, and what was measured last |
| `create-sender-domain` | register a domain — unverified until its DNS records are in place |
| `request-sender-domain-dns-check` | ask for a fresh DNS check once the records are set |

No KlickTipp tool writes DNS. The `dns-setup` skill guides provider changes or uses a connected provider integration with the user's approval.

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
| `search-email-editor-placeholders` | the placeholders one email can carry, with the IDs of the account's own — look them up instead of guessing |
| `get-email-editor-rich-text-content` · `replace-email-editor-rich-text-content` | read and replace the whole body of an email from the previous HTML editor — no publish step, the next send carries it |
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

**Statistics** — read-only. Every counter is a lifetime total, not restricted to a period;
only the tag statistics answer per period

| | |
|---|---|
| `get-account-statistics` | the account's dashboard in one call: the last ten sends, today's fastest-growing tags, daily subscriptions, unsubscriptions and bounces, mail providers, bounces by kind |
| `get-campaign-statistics` | what one email or SMS newsletter or autoresponder achieved, with its rates and every tracked link |
| `get-newsletter-split-test-statistics` | what a split test found out, per arm — and the winner only once the test is decided |
| `get-tag-statistics` | how many contacts got up to ten tags, per hour, day, month or year |
| `get-automation-statistics` · `get-automation-waiting-contact-counts` | how an automation is doing, and where its contacts wait right now |
| `get-automation-email-statistics` · `get-automation-sms-statistics` | what one email or SMS of an automation achieved |

An automation's ID comes from `search-automations`, an email's or SMS's from `search-emails` or `search-automation-editor-references`.

**Account settings**

| | |
|---|---|
| `get-account-settings` | the account's settings screen: feature switches, preview tag, email blacklist — only what the account may change, credentials only as set or not |
| `update-account-settings` | change named settings only; one bad value refuses the whole call, and credentials cannot be set here |

**Automations** — the graph, its actions, the Masterclass templates and the
messages an automation sends. Every write needs an inactive automation and its
current revision; activating is confirmed by a person in KlickTipp

| | |
|---|---|
| `search-automations` · `get-automation` · `validate-automation` | find an automation, read its graph with action IDs and revision, and check it |
| `create-automation-draft` · `update-automation-draft` | create an inactive draft with its start action, optionally as a copy, and change its name, notes and labels |
| `add-automation-<kind>-action` · `update-automation-<kind>-action` | one pair per action type: email, SMS, notifications, wait, decision, goal, tag, untag, set field, go-to, exit, restart, start and stop another automation, split test, outbound, name and gender detection, unsubscribe; the start action is configured with `update-automation-start-action` |
| `move-automation-action` · `copy-automation-action` · `delete-automation-action` | rearrange the graph; a copied action shares its message, a deleted one leaves its email in place |
| `get-automation-editor-capabilities` · `search-automation-editor-references` | which settings and condition operators an action takes, and the IDs of the tags, fields, messages and automations it names |
| `estimate-automation-audience` | estimate the initial audience of an automation, in batches |
| `prepare-automation-activation` | validate and return the activation dialog — it activates nothing |
| `stop-automation` · `move-automation-contacts` | stop a running automation, or move waiting contacts to another action — both reach contacts already in it |
| `search-automation-templates` · `get-automation-template` · `import-automation-template` | the Business Automation Masterclass catalogue and shared template links: find one, see what it brings, import it paused |
| `get-automation-email` · `create-…` · `update-…` · `delete-automation-email-draft` · `copy-automation-email` | the emails of an automation; the same without copying for notification emails, the content is written with the email tools above |
| `get-automation-sms` · `create-…` · `update-…` · `delete-automation-sms-draft` · `replace-automation-sms-content` · `copy-automation-sms` | the SMS of an automation; the same without copying for notification SMS |
| `send-automation-email-test` · `send-notification-email-test` · `send-automation-sms-test` · `send-notification-sms-test` | test sends — an unknown address becomes a tagged contact, an SMS test costs SMS credit |
| `send-email-for-gmail-placement-preview` · `get-email-gmail-placement-preview-result` | the Gmail inbox placement check of an email, and its result |

Deleting an automation or an automation draft, the Facebook-audience and
FullContact actions, and the personalized preview and spam check of an
automation email are not available here; they stay in KlickTipp.

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

These writes have no undo, and the agent is expected to say so before it calls
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
- `replace-signature-content` replaces the whole text of a signature. A signature
  is appended when a mail is sent, so the change reaches every future send that
  carries it, not only the newsletter at hand.

**No tool activates an automation.** `prepare-automation-activation` validates
it and returns the activation dialog; a person starts it there. Building and
importing reach nobody — a draft is inactive and an imported automation is
paused — but both leave their objects in the account. `stop-automation` and
`move-automation-contacts` act on contacts already in a running automation and
cannot be undone; the agent is expected to say what will happen and ask first.

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

`skills/dns-setup` — sending-domain DNS records, provider-specific setup and
verification, including the optional assisted mailserver route where available.

`skills/splittest` — A/B tests: make a newsletter a split test, add and copy
test arms, set a subject line per arm, and read what changes once a newsletter
is one.

`skills/dashboard` — reads the numbers of an account — the account overview with
its daily activity, top tags and recent newsletters, the rates of one send, tag
counts and tags over time, saved reports — keeps the unit, window and denominator
of each figure visible, and builds a dashboard out of them only when asked.
Read-only: it creates, changes and sends nothing.

`skills/automation` — build and change automations: the order of the steps,
which action type does what and which settings it needs, goals instead of
waits, dated campaigns anchored on a date field, and importing a Masterclass
template or a shared template link.

`skills/contacts` — find, read, add, subscribe and unsubscribe contacts, set
their field values, and read and change the account's settings, its blocklist
included. A pending double opt-in stays pending: nothing here confirms it for
the recipient.

`skills/tags` — find, create, rename and delete manual tags, put them on and
take them off contacts, and tell which addresses a tag really applies to.

`skills/custom-fields` — custom field definitions: type, one value per
subscription or per contact, the placeholder that renders a field in content.

`skills/opt-in` — create and change the opt-in processes behind the contacts
together with their confirmation email, its redirect pages, and what an
existing consent covers.

`skills/email-template-generator` — writes the plain business emails that are
not newsletters: cold outreach, support replies, follow-ups, declines. No HTML,
no layout.

The tool-focused skills carry `references/` folders with the tools they use,
their answer shapes and their pitfalls. `dns-setup` covers provider guidance
directly. `email`, `newsletter`, `splittest` and `dns-setup` are in English; the
others are in German, like the editor itself.

**What the skills describe is what the server serves.** A tool that is not in
them does not exist here, and neither does the capability behind it: there is,
for example, no KlickTipp tool that writes DNS records — `dns-setup` can use a
separately connected provider integration, or guide the owner through their DNS provider.

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
