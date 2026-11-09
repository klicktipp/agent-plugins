#!/usr/bin/env python3
"""Generate each case's MCP mock from a shared world and a per-group tool list.

A mocked tool is visible to Claude during the run, and every mocked tool's schema goes
into the run's context. Serving all 181 tools the skills touch would cost ~110k tokens of
tool definitions per run, so each skill group mocks only its own tools. The fictional
account is shared, so the groups agree about ids, tags and counts.

Layout this reads:
    mocks/world.md              the fictional account, shared by every group
    mocks/klicktipp/_tools.json the production tools/list, shared (not written here)
    <group>/tools.txt           one tool name per line
    <group>/abort_when.md       the conditions that end a run, one per '- ' line

and writes <group>/<case>/mocks/klicktipp/_server.md for every case in the group.

    python3 evals/build-mocks.py [--check]

--check exits 1 when a file on disk differs from what would be written, for CI.
"""
import json, sys
from pathlib import Path

root = Path(__file__).parent
check = "--check" in sys.argv[1:]
known = {t["name"] for t in json.loads((root / "mocks" / "klicktipp" / "_tools.json").read_text())["tools"]}
world = (root / "mocks" / "world.md").read_text().strip()

stale, written, groups = [], 0, 0
for tools_file in sorted(root.glob("*/tools.txt")):
    group = tools_file.parent
    tools = [t.strip() for t in tools_file.read_text().split() if t.strip()]
    unknown = [t for t in tools if t not in known]
    if unknown:
        sys.exit(f"{tools_file}: not production tools: {', '.join(unknown)}")
    abort = (group / "abort_when.md").read_text().strip()
    header = "---\ntype: agent\ntools:\n" + "".join(f"  - {t}\n" for t in tools)
    header += "abort_when: |\n" + "".join(f"  {l}\n" for l in abort.splitlines()) + "---\n\n"
    body = header + world + "\n"
    groups += 1
    for case in sorted(p.parent for p in group.glob("*/prompt.md")):
        out = case / "mocks" / "klicktipp" / "_server.md"
        if out.exists() and out.read_text() == body:
            continue
        if check:
            stale.append(str(out.relative_to(root)))
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(body)
        written += 1

if check and stale:
    sys.exit("out of date, re-run build-mocks.py:\n  " + "\n  ".join(stale))
print(f"{groups} group(s), {written} mock(s) written", file=sys.stderr)
