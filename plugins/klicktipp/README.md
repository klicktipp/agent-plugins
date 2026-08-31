# KlickTipp

Work with the product data of a KlickTipp account from your agent — contacts,
tags, custom fields, opt-in processes, signatures and email newsletters — over
the hosted KlickTipp MCP server at `https://mcp.klicktipp.com/mcp`.

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

- **Contacts** — `search-contacts`, `get-contact`, `subscribe`, `unsubscribe`, `enrich-contact`
- **Tags** — search/get/create/update/delete manual tags, assign and remove them
- **Custom fields** — search/get/create/update/delete field definitions
- **Newsletters** — search, get, create/update draft, configure delivery, test send, `activate-newsletter`, delivery status, delete draft
- **Opt-in** — `search-opt-in-processes`, `get-opt-in-process`, `get-subscription-redirect-url`
- **Signatures** — `search-signatures`, `get-signature`

Read tools run without a prompt. Every write tool is annotated so your agent asks
first, and the three that reach a real person — `subscribe`, `unsubscribe` and
`activate-newsletter` — additionally require an explicit approval argument, so
they can never fire as a side effect of some other request.

## What it touches

Everything happens inside the KlickTipp account the login belongs to, or a
subaccount that account may support. `activate-newsletter` **hands a newsletter
over for dispatch to real recipients and cannot be taken back.**

`get-subscription-redirect-url` returns a URL that identifies a subscriber (it
carries subscriber ID, email address, list, subscriber key and referral link) —
treat its result as personal data.

## Support

support@klick-tipp.com · [Privacy policy](https://www.klick-tipp.com/datenschutz)
· [Terms](https://www.klick-tipp.com/agb)
