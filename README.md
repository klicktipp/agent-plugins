# KlickTipp agent plugins

The official KlickTipp plugin marketplace for AI coding agents. One plugin,
[`plugins/klicktipp`](plugins/klicktipp): it writes, reviews and prepares
KlickTipp email newsletters from your agent, and reads the opt-in processes of
the account, over the hosted KlickTipp MCP server.

```bash
claude plugin marketplace add klicktipp/agent-plugins
claude plugin install klicktipp@klicktipp
claude mcp login plugin:klicktipp:klicktipp
```

No API key lives in this repository. The MCP endpoint
(`https://mcp.klicktipp.com/mcp`) sits behind OAuth and you sign in once,
interactively — see [SETUP.md](plugins/klicktipp/SETUP.md).

**Documentation: <https://klicktipp.github.io/agent-plugins/>**

| | |
|---|---|
| Plugin | `klicktipp` |
| Endpoint | `https://mcp.klicktipp.com/mcp` |
| Tools | newsletters (draft, drag-and-drop content, audience, sender, test send, dispatch confirmation) and opt-in processes |
| Skill | `email-erstellung` — HTML the KlickTipp email editor can import as editable blocks |
| Agents | Claude Code and the Claude directory (`.claude-plugin/`), Codex and ChatGPT (`.codex-plugin/`) |
| Requires | a KlickTipp account |

## Layout

```
.claude-plugin/marketplace.json     the marketplace this repository is
docs/                               the documentation site, published as GitHub Pages
CHANGELOG.md                        one entry per released version, and the release notes
plugins/klicktipp/
├── .claude-plugin/plugin.json      manifest for Claude
├── .codex-plugin/plugin.json       manifest for Codex/ChatGPT, kept at the same version
├── .mcp.json                       the MCP server — both manifests read this one file
├── assets/logo.svg
├── skills/email-erstellung/        shipped with the plugin
├── SETUP.md                        walks the agent through the one-time OAuth login
└── README.md
```

Both manifests are validated on every push by
[`.github/workflows/validate.yml`](.github/workflows/validate.yml): `claude
plugin validate` plus the invariants it does not cover — that the two manifests
stay at the same version and carry the fields a public listing needs, and that
the published plugin points nowhere but production.

## Releasing

A pushed version tag publishes the release — nothing else to do:

```bash
git tag 0.5.1 && git push origin 0.5.1
```

[`.github/workflows/release.yml`](.github/workflows/release.yml) checks that the
tag equals the version in both manifests, revalidates the plugin, takes the
release notes from the tag's [`CHANGELOG.md`](CHANGELOG.md) section, and attaches
`klicktipp-<tag>.zip` — the plugin directory itself, so it unpacks to
`klicktipp/`. A tag without a changelog section, or one that disagrees with the
manifests, fails the run and publishes nothing.

## Where this comes from

This repository is a **published mirror**. The plugin is generated from
KlickTipp's internal `agent-plugin` repository, which is the source of truth and
also builds the staging and local variants used internally. Changes are made
there and mirrored here; a pull request against this repository can therefore not
be merged directly — open an issue instead, or write to support@klick-tipp.com.

## Licence

Proprietary — see [LICENSE](LICENSE). Use of the KlickTipp service through this
plugin is governed by the KlickTipp
[terms](https://www.klick-tipp.com/agb) and
[privacy policy](https://www.klick-tipp.com/datenschutz).
