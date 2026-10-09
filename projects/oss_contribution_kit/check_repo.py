#!/usr/bin/env python3
"""Basic repository hygiene checker; heuristic only, not a security scanner."""
from pathlib import Path
import argparse, re

REQUIRED = ["README.md", "LICENSE"]
SECRET_PATTERNS = [
    re.compile(r"(?i)\b(api[_-]?key|secret|password)\s*[:=]\s*['\"][A-Za-z0-9_/\+=.-]{12,}['\"]"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{25,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9]{24,}\b"),
]
IGNORED_PARTS = {".git", ".venv", "venv", "node_modules", "__pycache__"}

def check_repo(root):
    root = Path(root)
    findings = []
    if not root.is_dir():
        return [f"ERROR: path is not a directory: {root}"]
    for name in REQUIRED:
        if not (root/name).exists():
            findings.append(f"WARNING: missing recommended file: {name}")
    for path in root.rglob("*"):
        if not path.is_file() or any(part in IGNORED_PARTS for part in path.parts):
            continue
        if path.stat().st_size > 1_000_000:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(content):
                findings.append(f"REVIEW: possible secret pattern in {path.relative_to(root)}")
                break
    if not findings:
        findings.append("OK: no configured hygiene findings")
    return findings

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default=".")
    args = parser.parse_args()
    findings = check_repo(args.path)
    for item in findings:
        print(item)
    return 1 if any(item.startswith("ERROR:") for item in findings) else 0

if __name__ == "__main__":
    raise SystemExit(main())
