import os
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def make_fake_hermes_repo(path: Path) -> str:
    path.mkdir(parents=True, exist_ok=True)
    (path / "foo.txt").write_text("old\n")
    subprocess.run(["git", "init", "-q"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=path, check=True)
    subprocess.run(["git", "add", "."], cwd=path, check=True)
    subprocess.run(["git", "commit", "-m", "init", "-q"], cwd=path, check=True)
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=path, capture_output=True, text=True, check=True
    )
    return result.stdout.strip()


def make_fake_kit(tmp_path: Path, hermes_base: str) -> Path:
    kit = tmp_path / "kit"
    kit.mkdir()
    (kit / "UPSTREAM_BASE").write_text(hermes_base + "\n")
    patches = kit / "patches"
    patches.mkdir()
    (patches / "hermes-customizations.patch").write_text(
        "diff --git a/foo.txt b/foo.txt\n"
        "index 1234567..89abcde 100644\n"
        "--- a/foo.txt\n"
        "+++ b/foo.txt\n"
        "@@ -1 +1 @@\n"
        "-old\n"
        "+new\n"
    )
    scripts = kit / "scripts"
    scripts.mkdir()
    for name in ("apply.sh", "check.sh"):
        source = ROOT / "scripts" / name
        (scripts / name).write_text(source.read_text())
        (scripts / name).chmod(0o755)
    return kit


class TestApply:
    def test_applies_cleanly(self, tmp_path: Path):
        hermes = tmp_path / "hermes"
        base = make_fake_hermes_repo(hermes)
        kit = make_fake_kit(tmp_path, base)

        result = subprocess.run(
            ["bash", str(kit / "scripts" / "apply.sh"), str(hermes)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr
        assert (hermes / "foo.txt").read_text() == "new\n"

    def test_refuses_dirty_checkout(self, tmp_path: Path):
        hermes = tmp_path / "hermes"
        base = make_fake_hermes_repo(hermes)
        kit = make_fake_kit(tmp_path, base)
        (hermes / "foo.txt").write_text("dirty\n")

        result = subprocess.run(
            ["bash", str(kit / "scripts" / "apply.sh"), str(hermes)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1
        assert "dirty" in result.stderr

    def test_refuses_wrong_base(self, tmp_path: Path):
        hermes = tmp_path / "hermes"
        base = make_fake_hermes_repo(hermes)
        # add another commit so HEAD no longer matches base
        (hermes / "foo.txt").write_text("second\n")
        subprocess.run(["git", "add", "."], cwd=hermes, check=True)
        subprocess.run(["git", "commit", "-m", "second", "-q"], cwd=hermes, check=True)
        kit = make_fake_kit(tmp_path, base)

        result = subprocess.run(
            ["bash", str(kit / "scripts" / "apply.sh"), str(hermes)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1
        assert "Expected Hermes base" in result.stderr


class TestCheck:
    def test_check_success(self, tmp_path: Path):
        hermes = tmp_path / "hermes"
        base = make_fake_hermes_repo(hermes)
        kit = make_fake_kit(tmp_path, base)

        result = subprocess.run(
            ["bash", str(kit / "scripts" / "check.sh"), str(hermes)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr
        assert "applies cleanly" in result.stdout

    def test_check_missing_target(self, tmp_path: Path):
        kit = make_fake_kit(tmp_path, "a" * 40)
        result = subprocess.run(
            ["bash", str(kit / "scripts" / "check.sh"), str(tmp_path / "missing")],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 2
        assert "does not exist" in result.stderr
