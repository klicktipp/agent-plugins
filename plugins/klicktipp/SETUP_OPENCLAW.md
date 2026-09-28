---
name: klicktipp-setup-openclaw
description: Connect OpenClaw to the KlickTipp MCP server and install the KlickTipp skills. Use when the user wants KlickTipp tools in OpenClaw, when OpenClaw's OAuth login against mcp.klicktipp.com fails, or when dynamic client registration is refused.
prerequisites: A KlickTipp account, OpenClaw, git.
---

# Connect KlickTipp to OpenClaw

OpenClaw has both halves natively: MCP servers under `mcp.servers` in `~/.openclaw/openclaw.json`,
with OAuth, and Agent Skills from `SKILL.md` folders. So the setup is one config entry and one
skills folder, and the OpenClaw agent can do both itself when you paste the prompt below.

**The client is a metadata URL, not an id.** KlickTipp has closed dynamic client registration,
and OpenClaw's MCP config has no field for a client id — it registers dynamically unless it is
given a client metadata document. KlickTipp publishes one for exactly this case:

```text
https://mcp.klicktipp.com/.well-known/oauth-client/desktop.json
```

Do not host your own copy: Keycloak trusts only KlickTipp's domains for this, and a document on
another domain is rejected with `Client nicht gefunden`. The document allows loopback callbacks
only, which covers OpenClaw's default `http://127.0.0.1:8989/oauth/callback`.

## Set it up by prompt

Paste this into a chat with your OpenClaw agent:

```text
Set up KlickTipp for OpenClaw. Do exactly these steps and nothing else:

1. MCP server. In ~/.openclaw/openclaw.json, add this server under "mcp" → "servers". Merge it
   into what is there — do not remove or change any other key:

   "klicktipp": {
     "url": "https://mcp.klicktipp.com/mcp",
     "transport": "streamable-http",
     "auth": "oauth",
     "oauth": {
       "scope": "api offline_access",
       "clientMetadataUrl": "https://mcp.klicktipp.com/.well-known/oauth-client/desktop.json"
     }
   }

   Do not set "identity" or "redirectUrl".

2. Skills. Run:
   git clone --depth 1 https://github.com/klicktipp/agent-plugins.git /tmp/klicktipp-agent-plugins
   Then copy every folder in /tmp/klicktipp-agent-plugins/plugins/klicktipp/skills/ into
   ~/.openclaw/skills/ (create it if needed). If a folder of the same name already exists there,
   stop and ask me before replacing it. Then delete /tmp/klicktipp-agent-plugins.

3. Run `openclaw mcp reload`. Show me the resulting server entry and the list of skill folders you
   installed, and tell me to run `openclaw mcp login klicktipp`.
```

Changing the config is a lasting change, so a restricted run asks you to approve it — with the
approval card or `/approve`, not with a "yes" in the chat.

Then sign in — this step is yours, because a browser opens:

```bash
openclaw mcp login klicktipp
```

Sign in with the KlickTipp account and approve the access. If the browser cannot reach the
callback (OpenClaw on another machine), finish with the code it shows:
`openclaw mcp login klicktipp --code <code>`.

Skills are picked up without a restart, but a running session keeps the set it started with —
start a new one.

## Set it up by hand

Add to `~/.openclaw/openclaw.json`:

```json
{
  "mcp": {
    "servers": {
      "klicktipp": {
        "url": "https://mcp.klicktipp.com/mcp",
        "transport": "streamable-http",
        "auth": "oauth",
        "oauth": {
          "scope": "api offline_access",
          "clientMetadataUrl": "https://mcp.klicktipp.com/.well-known/oauth-client/desktop.json"
        }
      }
    }
  }
}
```

and copy the skills:

```bash
git clone --depth 1 https://github.com/klicktipp/agent-plugins.git /tmp/klicktipp-agent-plugins
mkdir -p ~/.openclaw/skills
cp -R /tmp/klicktipp-agent-plugins/plugins/klicktipp/skills/* ~/.openclaw/skills/
rm -rf /tmp/klicktipp-agent-plugins
openclaw mcp reload
openclaw mcp login klicktipp
```

For one workspace only, copy the skills into that workspace's `skills/` folder instead — it takes
precedence over `~/.openclaw/skills/`.

## Check that it worked

```bash
openclaw mcp probe klicktipp
```

should connect. Then ask for something harmless and read-only:

> Show me my opt-in processes.

If that returns a list, the connection is live.

## When it does not work

**`Policy 'Trusted Hosts' rejected request to client-registration service`** — `clientMetadataUrl`
is missing, so OpenClaw tried to register itself. Add it.

**`Client nicht gefunden` / client not found** — `clientMetadataUrl` points at a copy of the
document, or is misspelt. It must be the URL above, on `mcp.klicktipp.com`.

**The browser shows an invalid redirect URI** — `identity` is `per-requester` or `redirectUrl`
points at a public URL. The KlickTipp client allows loopback callbacks only; remove both.

**The tools are there but the agent ignores the skills** — the session started before they were
copied. Start a new session; `openclaw skills list` shows what is loaded.

## Before writing anything

Everything under "Before writing anything" in [SETUP.md](SETUP.md) applies here unchanged.
OpenClaw is another way in to the same account, and a tool that writes reaches a live customer
account whichever host called it — including from a chat channel someone else can write into.
