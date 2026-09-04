# KlickTipp

Write, configure and send KlickTipp email newsletters from your agent, and read
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
| `search-newsletters` | find newsletters of the account |
| `get-newsletter` | read one, with its content and configuration |
| `create-newsletter-draft` · `update-newsletter-draft` · `delete-newsletter-draft` | work on a draft |
| `configure-newsletter-delivery` | audience, sender and schedule |
| `send-newsletter-test` | test send, to yourself |
| `activate-newsletter` | hand the newsletter over for dispatch |
| `get-newsletter-delivery-status` | follow what happened after that |

**Opt-in**

| | |
|---|---|
| `search-opt-in-processes` | list the account's opt-in processes |
| `get-opt-in-process` | read the full configuration of one |
| `get-subscription-redirect-url` | resolve the pending or thank-you URL a subscriber is redirected to |

## Skill

`skills/email-erstellung` — writes HTML that the KlickTipp email editor's HTML
import turns back into editable drag-and-drop blocks instead of one
undividable wall of text. In German, like the editor itself.

## What it touches

Everything happens inside the KlickTipp account the login belongs to, or a
subaccount that account may support. Read tools run without a prompt; every
write tool is annotated so your agent asks first.

`activate-newsletter` **hands a newsletter over for dispatch to real recipients
and cannot be taken back.** It requires an explicit approval argument, so it can
never fire as a side effect of some other request.

`get-subscription-redirect-url` returns a URL that identifies a subscriber — it
carries subscriber ID, email address, list, subscriber key and referral link.
Treat its result as personal data.

## Support

support@klick-tipp.com ·
[Documentation](https://klicktipp.github.io/agent-plugins/) ·
[Privacy policy](https://www.klick-tipp.com/datenschutz) ·
[Terms](https://www.klick-tipp.com/agb)
