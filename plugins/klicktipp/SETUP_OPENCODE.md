---
name: klicktipp-setup-opencode
description: Connect opencode to the KlickTipp MCP server and install the KlickTipp skills. Use when the user wants KlickTipp tools in opencode, when opencode's OAuth login against mcp.klicktipp.com fails, or when dynamic client registration is refused.
prerequisites: A KlickTipp account, opencode, git.
---

# Connect KlickTipp to opencode

opencode is not a plugin host for this plugin, but it has both halves natively: remote MCP servers
with OAuth, and Agent Skills from `SKILL.md` folders. So the setup is two steps — one entry in the
opencode config, and the skills copied into a folder opencode reads — and opencode can do both
itself when you paste the prompt below.

**The client is named, not registered.** KlickTipp has closed dynamic client registration, and
opencode falls back to it whenever no `clientId` is configured. So the entry carries the shared
public client `mcp-klicktipp-desktop`: no secret, PKCE, loopback callbacks. opencode's own
callback (`http://127.0.0.1:19876/mcp/oauth/callback`) is covered by it, so nothing has to be
registered for you.

## Set it up by prompt

Start opencode in any directory and paste this:

```text
Set up KlickTipp for opencode. Do exactly these steps and nothing else:

1. MCP server. In ~/.config/opencode/opencode.json (create it with
   "$schema": "https://opencode.ai/config.json" if it does not exist), add this entry under "mcp".
   Merge it into what is there — do not remove or change any other key:

   "klicktipp": {
     "type": "remote",
     "url": "https://mcp.klicktipp.com/mcp",
     "enabled": true,
     "oauth": { "clientId": "mcp-klicktipp-desktop", "scope": "api offline_access" }
   }

   Do not add a clientSecret and do not add an Authorization header.

2. Skills. Run:
   git clone --depth 1 https://github.com/klicktipp/agent-plugins.git /tmp/klicktipp-agent-plugins
   Then copy every folder in /tmp/klicktipp-agent-plugins/plugins/klicktipp/skills/ into
   ~/.config/opencode/skills/ (create it if needed). If a folder of the same name already exists
   there, stop and ask me before replacing it. Then delete /tmp/klicktipp-agent-plugins.

3. Show me the resulting "mcp" block and the list of skill folders you installed, and tell me to
   run `opencode mcp auth klicktipp` and restart opencode.
```

Then sign in — this step is yours, because a browser opens:

```bash
opencode mcp auth klicktipp
```

Sign in with the KlickTipp account and approve the access. The token is stored in
`~/.local/share/opencode/mcp-auth.json` and refreshed automatically. **Restart opencode**
afterwards: skills and MCP servers are read at start.

## Set it up by hand

The same two steps, without the agent. Add to `~/.config/opencode/opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "klicktipp": {
      "type": "remote",
      "url": "https://mcp.klicktipp.com/mcp",
      "enabled": true,
      "oauth": { "clientId": "mcp-klicktipp-desktop", "scope": "api offline_access" }
    }
  }
}
```

and copy the skills:

```bash
git clone --depth 1 https://github.com/klicktipp/agent-plugins.git /tmp/klicktipp-agent-plugins
mkdir -p ~/.config/opencode/skills
cp -R /tmp/klicktipp-agent-plugins/plugins/klicktipp/skills/* ~/.config/opencode/skills/
rm -rf /tmp/klicktipp-agent-plugins
```

For one project only, put the entry into that project's `opencode.json` and the skills into
`.opencode/skills/` instead. opencode also reads `~/.claude/skills/` — if the Claude Code plugin
is installed there already, the skills are found without copying.

## Check that it worked

```bash
opencode mcp list
```

should show `klicktipp` as connected. Then ask for something harmless and read-only:

> Show me my opt-in processes.

If that returns a list, the connection is live.

## When it does not work

**`Policy 'Trusted Hosts' rejected request to client-registration service`** — the entry has no
`clientId`, so opencode tried to register itself. Add the `oauth` block above.

**`Client nicht gefunden` / client not found** — the `clientId` is misspelt. It is
`mcp-klicktipp-desktop`.

**The browser shows an invalid redirect URI** — a `redirectUri` points somewhere other than
`127.0.0.1` or `localhost`. Remove it; only loopback callbacks are allowed.

**The tools are there but the skills are not** — opencode was not restarted, or a skill folder
landed one level too deep. Each skill must be `~/.config/opencode/skills/<name>/SKILL.md`, and
the folder name must equal the `name` in its frontmatter.

## Before writing anything

Everything under "Before writing anything" in [SETUP.md](SETUP.md) applies here unchanged.
opencode is another way in to the same account, and a tool that writes reaches a live customer
account whichever host called it.
