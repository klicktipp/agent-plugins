#!/usr/bin/env python3
"""Check the invariants `claude plugin validate` does not cover.

The Claude manifest and the Codex manifest describe one plugin for two
directories. Whatever drifts between them is published to one audience and not
the other, and nothing else in CI would notice.

    python3 .github/scripts/check_manifests.py
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PLUGIN = ROOT / "plugins" / "klicktipp"
SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
PROD_URL = "https://mcp.klicktipp.com/mcp"

problems = []


def fail(msg):
    problems.append(msg)


def load(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing {path.relative_to(ROOT)}")
    except json.JSONDecodeError as e:
        fail(f"{path.relative_to(ROOT)} is not valid JSON: {e}")
    return None


def main():
    claude = load(PLUGIN / ".claude-plugin" / "plugin.json")
    codex = load(PLUGIN / ".codex-plugin" / "plugin.json")
    market = load(ROOT / ".claude-plugin" / "marketplace.json")
    mcp = load(PLUGIN / ".mcp.json")
    if problems:
        return report()

    # the name is a permanent slug in both directories — a rename breaks every
    # existing install with plugin-not-found, so it is pinned here on purpose
    for label, m in (("claude", claude), ("codex", codex)):
        if m.get("name") != "klicktipp":
            fail(f"{label} manifest: name is '{m.get('name')}', must stay 'klicktipp'")
        if not SEMVER.match(str(m.get("version", ""))):
            fail(f"{label} manifest: version '{m.get('version')}' is not semver")
        for field in ("description", "author", "homepage", "repository", "license"):
            if not m.get(field):
                fail(f"{label} manifest: missing '{field}'")
        if m.get("mcpServers") != "./.mcp.json":
            fail(f"{label} manifest: mcpServers must point at ./.mcp.json")

    # both directories have to be shipped the same plugin
    for field in ("version", "description", "keywords", "homepage", "repository", "license"):
        if claude.get(field) != codex.get(field):
            fail(f"'{field}' differs between the Claude and the Codex manifest")

    if claude.get("displayName") != codex.get("interface", {}).get("displayName"):
        fail("displayName differs between the Claude manifest and the Codex interface block")

    # a public listing without these is rejected in review. The category lives
    # in the marketplace entry, not in plugin.json — `claude plugin validate`
    # warns that plugin.json ignores it.
    if claude.get("category"):
        fail("claude manifest: 'category' belongs in marketplace.json, not plugin.json")
    if not (market or {}).get("plugins", [{}])[0].get("category"):
        fail("marketplace.json: the plugin entry has no 'category'")
    for field in ("shortDescription", "longDescription", "developerName", "category",
                  "privacyPolicyURL", "termsOfServiceURL", "logo"):
        if not codex.get("interface", {}).get(field):
            fail(f"codex manifest: interface.{field} is missing")

    if not (ROOT / "LICENSE").exists():
        fail("no LICENSE file — the plugin directory requires one")

    # the published plugin must never point anywhere but production
    servers = (mcp or {}).get("mcpServers", {})
    if list(servers) != ["klicktipp"]:
        fail(f".mcp.json: expected exactly one server 'klicktipp', got {list(servers)}")
    for name, cfg in servers.items():
        if cfg.get("url") != PROD_URL:
            fail(f".mcp.json: server '{name}' points at {cfg.get('url')}, not {PROD_URL}")

    entries = (market or {}).get("plugins", [])
    if len(entries) != 1 or entries[0].get("name") != "klicktipp":
        fail("marketplace.json: expected exactly one plugin entry named 'klicktipp'")
    else:
        source = ROOT / entries[0].get("source", "")
        if not source.is_dir():
            fail(f"marketplace.json: source '{entries[0].get('source')}' is not a directory")

    for declared, path in (("skills", "skills"),):
        if claude.get(declared) and not (PLUGIN / path).is_dir():
            fail(f"claude manifest declares '{declared}' but {path}/ does not exist")
        if (PLUGIN / path).is_dir() and not claude.get(declared):
            fail(f"{path}/ exists but the claude manifest does not declare '{declared}'")

    return report()


def report():
    if problems:
        print("\n".join(f"  x {p}" for p in problems))
        sys.exit(f"\n{len(problems)} problem(s) in the published manifests.")
    print("ok - the Claude and Codex manifests agree and are complete.")


if __name__ == "__main__":
    main()
