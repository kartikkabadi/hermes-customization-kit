#!/usr/bin/env python3
"""Fail on strong credential signatures or private-key material."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


PATTERNS = {
    "AWS access key": re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    "Google API key": re.compile(r"\bAIza[0-9A-Za-z_-]{30,}\b"),
    "GitHub token": re.compile(r"\bgh[pousr]_[0-9A-Za-z]{20,}\b"),
    "OpenAI/Anthropic key": re.compile(r"\bsk-(?:ant-)?[0-9A-Za-z_-]{16,}\b"),
    "Slack token": re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{10,}\b"),
    "Telegram bot token": re.compile(r"\b\d{8,10}:[0-9A-Za-z_-]{30,}\b"),
    "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", type=Path, default=Path.cwd())
    args = parser.parse_args()
    findings: list[tuple[Path, int, str]] = []

    if args.path.is_file():
        paths = [args.path]
    else:
        paths = [p for p in args.path.rglob("*") if p.is_file() and ".git" not in p.parts]

    for path in paths:
        try:
            text = path.read_text()
        except (UnicodeDecodeError, OSError):
            continue
        for line_number, line in enumerate(text.splitlines(), 1):
            for label, pattern in PATTERNS.items():
                if pattern.search(line):
                    findings.append((path, line_number, label))

    for path, line_number, label in findings:
        print(f"{path}:{line_number}: {label}")
    raise SystemExit(1 if findings else 0)


if __name__ == "__main__":
    main()
