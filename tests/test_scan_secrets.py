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


def test_leaked_fixture_has_expected_findings():
    fixtures = ROOT / "tests" / "fixtures" / "scan_secrets"
    code, output = run_scan_secrets(fixtures)
    assert code == 1, f"Expected findings, got exit code {code}"
    assert "leaked.txt" in output
    assert output.count("leaked.txt") >= 6, f"Expected at least six findings:\n{output}"
