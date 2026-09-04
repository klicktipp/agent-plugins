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
| `email-newsletter-content-replace` | replace the drag-and-drop body, bound to the revision you read |
| `email-newsletter-content-publish` | make the reviewed body the one a dispatch would send |
| `email-newsletter-delivery-configure` | sender name, sender address, reply address, signature |
| `email-newsletter-test-send` | test send to the account's own or a verified sender address |
| `email-newsletter-send` | prepare the real dispatch and return a confirmation URL |

**Opt-in**

| | |
|---|---|
| `search-opt-in-processes` | list the account's opt-in processes |
| `get-opt-in-process` | read the full configuration of one |
| `get-subscription-redirect-url` | resolve the pending or thank-you URL a subscriber is redirected to |

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

- `email-newsletter-content-replace` converts HTML only. Social icons come back
  as linked images, tables as plain markup, video as a preview image, add-ons as
  their rendered output; web fonts, row background images and own head styles are
  dropped; **KlickTipp decisions and AI blocks are deleted beyond recovery.** The
  `content` projection of `email-newsletter-get` lists exactly what a replacement
  would cost for the newsletter at hand, as `replaceWarnings` — those belong in
  front of the user, not summarised away.
- `email-newsletter-content-publish` changes what real recipients would receive.
- `email-newsletter-draft-delete` removes the draft with its email, audience
  conditions and system tags.

`get-subscription-redirect-url` returns a URL that identifies a subscriber — it
carries subscriber ID, email address, list, subscriber key and referral link.
Treat its result as personal data.

## Skill

`skills/email-erstellung` — writes HTML that the KlickTipp email editor's HTML
import turns back into editable drag-and-drop blocks instead of one undividable
wall of text. That is the HTML `email-newsletter-content-replace` expects. In
German, like the editor itself.

## Support

support@klick-tipp.com ·
[Documentation](https://klicktipp.github.io/agent-plugins/) ·
[Privacy policy](https://www.klick-tipp.com/datenschutz) ·
[Terms](https://www.klick-tipp.com/agb)
