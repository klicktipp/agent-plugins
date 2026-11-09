#!/usr/bin/env python3
"""Rebuild mocks/klicktipp/_tools.json from the published KlickTipp tool catalogue.

The production MCP server answers tools/list only behind OAuth, so the catalogue the
docs site ships is the source. Run this after a KlickTipp server release.

    python3 evals/refresh-tools.py [--no-output-schema]

claude plugin eval caps any single mock file at 1 MiB. With every output schema the
file sits around 890 KiB; --no-output-schema halves it, at the price of the agent mock
inventing response shapes again.
"""
import json, sys, urllib.request
from pathlib import Path

SRC = "https://developers.klicktipp.com/page-data/shared/api-docs-mcp-tools.json.json"
CAP = 1024 * 1024
OUT = Path(__file__).parent / "mocks" / "klicktipp" / "_tools.json"

with_output = "--no-output-schema" not in sys.argv[1:]
with urllib.request.urlopen(SRC, timeout=120) as r:
    catalogue = json.load(r)["store"]["mcp"]["tools"]

tools = []
for t in sorted(catalogue, key=lambda t: t["name"]):
    entry = {"name": t["name"], "description": t.get("description", "")}
    if t.get("title"):
        entry["title"] = t["title"]
    entry["inputSchema"] = t["inputSchema"]
    if with_output and t.get("outputSchema"):
        entry["outputSchema"] = t["outputSchema"]
    tools.append(entry)

blob = json.dumps({"tools": tools}, ensure_ascii=False, separators=(",", ":"))
size = len(blob.encode())
print(f"{len(tools)} tools, {size / 1024:.0f} KiB", file=sys.stderr)
if size >= CAP:
    print(
        f"over the 1 MiB cap claude plugin eval enforces per mock file — "
        f"re-run with --no-output-schema",
        file=sys.stderr,
    )
    sys.exit(1)
OUT.write_text(blob + "\n")
print(f"wrote {OUT}", file=sys.stderr)
