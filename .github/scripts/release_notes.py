#!/usr/bin/env python3
"""Print the CHANGELOG.md section of one version, for the release body.

    python3 .github/scripts/release_notes.py 0.5.0

A version without its own section is an error: the release would otherwise be
published with someone else's notes, or with none.
"""

import re
import sys
from pathlib import Path

CHANGELOG = Path(__file__).resolve().parents[2] / "CHANGELOG.md"


def section(text, version):
    # "## 0.5.0 — 2026-09-09" up to the next "## "
    pattern = rf"^## {re.escape(version)}(?:[^\n]*)?$\n(.*?)(?=^## |\Z)"
    m = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    return m.group(1).strip() if m else None


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: release_notes.py <version>")
    version = sys.argv[1]
    body = section(CHANGELOG.read_text(encoding="utf-8"), version)
    if not body:
        raise SystemExit(f"CHANGELOG.md has no '## {version}' section")
    print(body)


if __name__ == "__main__":
    main()
