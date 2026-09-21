---
name: klicktipp-setup-langdock
description: Connect a Langdock workspace to the KlickTipp MCP server. Use when the user wants KlickTipp tools in Langdock, when a Langdock integration against mcp.klicktipp.com fails to authorise, or when dynamic client registration is refused.
prerequisites: A KlickTipp account, and permission to add integrations in the Langdock workspace.
---

# Connect KlickTipp to Langdock

Langdock reaches the same server as the plugin, `https://mcp.klicktipp.com/mcp`,
but it is not a plugin host: the connection is configured once per workspace as a
remote MCP integration, and the OAuth client is named explicitly rather than
registered on the fly.

**Register the client by hand, not dynamically.** KlickTipp has closed dynamic
client registration, so the "OAuth 2.0 (Dynamic Client Registration)" option
fails — not because something is misconfigured, but because there is nothing on
the other side to register with. The manual option is the supported route.

## Add the integration

In <https://app.langdock.com>: **Integrations → Add Integration → Start from
scratch → Connect remote MCP**.

| Field | Value |
|---|---|
| Server URL | `https://mcp.klicktipp.com/mcp` |
| Transport | `STREAMABLE_HTTP` |
| Authentication | OAuth 2.0 Manual (Authorization Code + PKCE) |
| Client ID | `mcp-klicktipp-langdock` |
| Client Secret | *leave empty* |
| Authorization URL | `https://auth.klicktipp.com/realms/klicktipp/protocol/openid-connect/auth` |
| Token URL | `https://auth.klicktipp.com/realms/klicktipp/protocol/openid-connect/token` |
| Scopes | `api offline_access` |
| Send resource parameter | on |

The empty secret is deliberate. This is a public client, and PKCE — not a shared
secret — is what secures the exchange. A form that insists on a secret is a sign
the wrong authentication mode is selected.

Then **Create and connect**, sign in with the KlickTipp account, and approve the
consent screen.

## Check that it worked

**Test connection** should load the tool list. Then pick the tools the workspace
should have and save.

If the list is empty or the test fails, the authorisation did not complete —
repeat it rather than changing the values above.

## When it does not work

**`redirect_uri_mismatch`** — Langdock's redirect URL is not on the Keycloak
client. Read the URL Langdock shows and have it added; it is not something the
integration form can fix.

**The token request fails** — turn *Send resource parameter* off and try again.
Some deployments reject the `resource` parameter rather than ignoring it.

**The form insists on a client secret** — the mode is wrong, or this Langdock
build cannot do public clients. Both are resolved on the Keycloak side, by
issuing a confidential client for this workspace.

## Before writing anything

Everything under "Before writing anything" in [SETUP.md](SETUP.md) applies here
unchanged. Langdock is another way in to the same account, and a tool that writes
reaches a live customer account whichever host called it.
