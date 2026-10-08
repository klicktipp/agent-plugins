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

Langdock takes at most 60 tools per integration, and the server offers more. Pick
the ones for the work the workspace does — for newsletters, the `*-newsletter*`
and `*-email-editor-*` tools — rather than the first sixty.

## Load the skills

The tools alone do not know KlickTipp's rules — that the editor stores blocks, not
HTML, or that no tool sends a newsletter. That knowledge is in the skills, and
Langdock takes them natively: **Skills → Add Skill → upload**, one ZIP per skill
with `SKILL.md` at its top.

Every release publishes them ready to upload, one per skill — no git, no build.
These links always point at the latest release:

| Skill | Download |
|---|---|
| `contacts` | [klicktipp-skill-contacts.zip](https://github.com/klicktipp/agent-plugins/releases/latest/download/klicktipp-skill-contacts.zip) |
| `custom-fields` | [klicktipp-skill-custom-fields.zip](https://github.com/klicktipp/agent-plugins/releases/latest/download/klicktipp-skill-custom-fields.zip) |
| `dashboard` | [klicktipp-skill-dashboard.zip](https://github.com/klicktipp/agent-plugins/releases/latest/download/klicktipp-skill-dashboard.zip) |
| `dns-setup` | [klicktipp-skill-dns-setup.zip](https://github.com/klicktipp/agent-plugins/releases/latest/download/klicktipp-skill-dns-setup.zip) |
| `email` | [klicktipp-skill-email.zip](https://github.com/klicktipp/agent-plugins/releases/latest/download/klicktipp-skill-email.zip) |
| `email-template-generator` | [klicktipp-skill-email-template-generator.zip](https://github.com/klicktipp/agent-plugins/releases/latest/download/klicktipp-skill-email-template-generator.zip) |
| `newsletter` | [klicktipp-skill-newsletter.zip](https://github.com/klicktipp/agent-plugins/releases/latest/download/klicktipp-skill-newsletter.zip) |
| `opt-in` | [klicktipp-skill-opt-in.zip](https://github.com/klicktipp/agent-plugins/releases/latest/download/klicktipp-skill-opt-in.zip) |
| `splittest` | [klicktipp-skill-splittest.zip](https://github.com/klicktipp/agent-plugins/releases/latest/download/klicktipp-skill-splittest.zip) |
| `tags` | [klicktipp-skill-tags.zip](https://github.com/klicktipp/agent-plugins/releases/latest/download/klicktipp-skill-tags.zip) |

Upload each ZIP as it is, and in the skill's **Integrations** field
attach the KlickTipp integration from above — its tools then come with the skill whenever the skill is
active in a chat.

## Set up an agent by prompt

The integration is the one step no prompt can take: only an admin adds it, in the
form above. Everything after it can be asked for. Open **Agents → Create agent**
and give the Agent Builder this:

```text
Create an agent "KlickTipp". It works in the user's KlickTipp account through the
KlickTipp integration. Attach the KlickTipp integration and the skills contacts,
custom-fields, dashboard, dns-setup, email, email-template-generator, newsletter, opt-in,
splittest and tags.
Instructions: Read the matching skill before the first KlickTipp tool call of a
task. Never send a newsletter yourself: prepare-newsletter-dispatch returns a
confirmation link, hand it to the user with subject, audience, recipient estimate,
sender and time. Before any write without undo, say what it costs and ask.
```

The builder can only attach what is already connected in the workspace, so the
integration and the skills have to exist first.

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
