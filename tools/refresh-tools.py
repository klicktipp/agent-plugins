#!/usr/bin/env python3
"""Rebuild the eval suite's mocks/klicktipp/_tools.json from the published catalogue.

The production MCP server answers tools/list only behind OAuth, so the catalogue the
docs site ships is the source. Run this after a KlickTipp server release, then
`python3 tools/build-mocks.py`.

    python3 tools/refresh-tools.py [--with-output-schema]

Only the tools the groups actually mock are written — the union of every
<group>/tools.txt — because a tool no group mocks is never served. The plugin
directory inspects every file it ships and refuses what it cannot read in full, so
the file stays small: output schemas are left out unless --with-output-schema is
given, at the price of the agent mock inventing response shapes again.

This script lives outside the plugin folder on purpose: the plugin directory accepts
Markdown, text, JSON, YAML and a few image formats there, and no executable scripts.
"""
import json, sys, urllib.request
from pathlib import Path

SRC = "https://developers.klicktipp.com/page-data/shared/api-docs-mcp-tools.json.json"
CAP = 512 * 1024
EVALS = Path(__file__).resolve().parent.parent / "plugins" / "klicktipp" / "evals"
OUT = EVALS / "mocks" / "klicktipp" / "_tools.json"

with_output = "--with-output-schema" in sys.argv[1:]
used = set()
for tools_file in sorted(EVALS.glob("*/tools.txt")):
    used |= {t.strip() for t in tools_file.read_text().split() if t.strip()}
with urllib.request.urlopen(SRC, timeout=120) as r:
    catalogue = json.load(r)["store"]["mcp"]["tools"]

tools = []
for t in sorted(catalogue, key=lambda t: t["name"]):
    if t["name"] not in used:
        continue
    entry = {"name": t["name"], "description": t.get("description", "")}
    if t.get("title"):
        entry["title"] = t["title"]
    entry["inputSchema"] = t["inputSchema"]
    if with_output and t.get("outputSchema"):
        entry["outputSchema"] = t["outputSchema"]
    tools.append(entry)

missing = used - {t["name"] for t in tools}
if missing:
    sys.exit("tools.txt names no longer in the catalogue: " + ", ".join(sorted(missing)))

blob = json.dumps({"tools": tools}, ensure_ascii=False, separators=(",", ":"))
size = len(blob.encode())
print(f"{len(tools)} tools, {size / 1024:.0f} KiB", file=sys.stderr)
if size >= CAP:
    print(
        f"over the {CAP // 1024} KiB this suite keeps the file under — "
        f"re-run without --with-output-schema",
        file=sys.stderr,
    )
    sys.exit(1)
OUT.write_text(blob + "\n")
print(f"wrote {OUT}", file=sys.stderr)
