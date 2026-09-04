---
name: klicktipp-setup
description: Sign the user in to the KlickTipp MCP server after the KlickTipp plugin has been installed. Use when a KlickTipp tool call fails with an authentication or 401 error, when the user asks how to connect or log in to KlickTipp, or right after the plugin is installed and no KlickTipp tool has ever succeeded in this project.
prerequisites: A KlickTipp account.
---

# Connect the KlickTipp plugin

This plugin ships one MCP server, `klicktipp`, pointing at
`https://mcp.klicktipp.com/mcp`. It carries no API key: the endpoint sits behind
OAuth, and the user signs in once per machine. Nothing else has to be
configured — there is no setting, token or URL to fill in.

## What "not signed in yet" looks like

Until the connection is authorised, every attempt sends an `initialize` without a
token and the server answers `401` with a `WWW-Authenticate` header. The tool
list may come up empty and tool calls fail with an authentication error. **This
is the expected run-up to the login, not a defect** — do not start debugging the
endpoint, and do not offer to add the server a second time by hand.

## Sign in

The server of an installed plugin is its own connection with its own prefixed
name. Use the full name — a login for a hand-added server called `klicktipp` does
not count here, because credentials are stored per identity:

```bash
claude mcp login plugin:klicktipp:klicktipp
```

The short name alone is rejected with `No MCP server named "klicktipp"`. Inside
Claude Code, `/mcp` offers the same login; the connection is listed under exactly
that prefixed name.

A browser window opens, the user signs in with their KlickTipp credentials and
approves the access. After that the token is stored and refreshed automatically —
this is a one-time step per machine.

## Check that it worked

Ask for something harmless and read-only, and confirm the account is the one the
user expects:

> Show me my opt-in processes.

If that returns a list, the connection is live. If it still fails with `401`,
the login did not complete — repeat it rather than changing the configuration.

## Known limitation: the Claude desktop app

Adding this plugin **in the Claude desktop app** currently cannot complete the
OAuth handshake against the KlickTipp server; the authorise request ends in
`HTTP 400`. This is an upstream issue in how the desktop app registers itself as
an OAuth client, not something this plugin or the KlickTipp side can configure
around.

Two routes work today:

1. Install the plugin in the terminal and sign in there, as above.
2. Add the MCP server by hand, without the plugin. Every tool is then available,
   including in the desktop app — a locally registered MCP server is used by the
   app, a plugin server is not:

```bash
claude mcp add --scope user --transport http klicktipp https://mcp.klicktipp.com/mcp
claude mcp login klicktipp
```

If both routes are active at once, the same tools appear twice in the
`mcp__klicktipp__*` namespace. Remove one of the two sources:

```bash
claude mcp remove klicktipp --scope user
```

## Before writing anything

Tools that write reach a live customer account.

**No tool sends a newsletter.** `email-newsletter-send` only prepares the
dispatch and returns a short-lived single-use confirmation URL. Hand that URL to
the user along with what confirming it will do — subject, who receives it (mode
`all_contacts` means every active contact of the account), the recipient
estimate, sender and moment. Opening and confirming it is theirs to do, and that
step cannot be taken back.

Three writes have no undo. Say what they cost before calling them:

- `email-newsletter-content-replace` — read the newsletter first and pass its
  `replaceWarnings` to the user verbatim enough to be understood. KlickTipp
  decisions and AI blocks are deleted beyond recovery.
- `email-newsletter-content-publish` — changes what real recipients would
  receive.
- `email-newsletter-draft-delete` — only for a draft the user explicitly asked
  to delete.

`get-subscription-redirect-url` returns a URL that identifies a subscriber
(subscriber ID, email address, list, subscriber key, referral link). Treat its
result as personal data: use it, do not repeat it back in full unless the user
asked for the URL itself.
