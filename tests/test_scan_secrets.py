import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def run_scan_secrets(path: Path) -> tuple[int, str]:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "scan-secrets.py"), str(path)],
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout


def test_clean_file_has_no_findings(tmp_path: Path):
    clean = tmp_path / "clean.txt"
    clean.write_text("This file contains no credentials.\n")
    code, output = run_scan_secrets(clean)
    assert code == 0, f"Expected no findings, got:\n{output}"
    assert output == ""


def test_leaked_file_has_expected_findings(tmp_path: Path):
    # Construct strings that match the scanner regexes at runtime only.
    telegram_token = "1" * 10 + ":" + "A" * 35
    leaked = tmp_path / "leaked.txt"
    leaked.write_text(
        f"aws=AKIA{'A' * 16}\n"
        f"google=AIza{'a' * 36}\n"
        f"github=ghp_{'A' * 36}\n"
        f"anthropic=sk-{'A' * 36}\n"
        f"slack=xoxb-{'1' * 10}-{'A' * 24}\n"
        f"telegram={telegram_token}\n"
        "private=" + "-----BEGIN " + "PRIVATE KEY-----\n"
    )
    code, output = run_scan_secrets(leaked)
    assert code == 1, f"Expected findings, got exit code {code}"
    assert output.count(":") >= 6, f"Expected at least six findings:\n{output}"
