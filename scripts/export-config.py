#!/usr/bin/env python3
"""Export Hermes configuration while removing credentials and local identity."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

import yaml


SECRET_PARTS = {
    "api_key", "access_token", "auth_token", "bot_token", "client_secret",
    "credential", "password", "password_hash", "private_key", "secret",
    "session_key", "token",
}
IDENTITY_KEYS = {
    "allowed_channels", "allowed_chats", "allowed_rooms", "allowed_users",
    "client_id", "dm_role_auth_guild", "free_response_channels",
    "home_channel", "project_id", "user_id",
}
PRIVATE_CONTENT_KEYS = {
    "ambient_path", "persona_prompt_file", "ref_audio", "ref_text",
    "template_vars",
}
TOKEN_PATTERNS = (
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bAIza[0-9A-Za-z_-]{30,}\b"),
    re.compile(r"\bgh[pousr]_[0-9A-Za-z]{20,}\b"),
    re.compile(r"\bsk-(?:ant-)?[0-9A-Za-z_-]{16,}\b"),
    re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{10,}\b"),
    re.compile(r"\b\d{8,10}:[0-9A-Za-z_-]{30,}\b"),
)


def normalized(key: str) -> str:
    return key.lower().replace("-", "_")


def is_secret_key(name: str) -> bool:
    return name in SECRET_PARTS or any(
        name.endswith(f"_{part}") for part in SECRET_PARTS
    )


def _sanitize_provider(provider: Any, home: Path) -> Any:
    """Redact user-specific provider metadata while preserving public model metadata."""
    if not isinstance(provider, dict):
        return sanitize(provider, home)
    sanitized = sanitize(provider, home)
    for key in ("name", "base_url"):
        if key in sanitized and sanitized[key] not in {
            "<set-locally>", "<set-via-environment>", "<redacted>",
        }:
            sanitized[key] = "<set-locally>"
    return sanitized


def sanitize(value: Any, home: Path, key: str = "") -> Any:
    name = normalized(key)
    if is_secret_key(name):
        return "<set-via-environment>"
    if name in IDENTITY_KEYS:
        return [] if isinstance(value, list) else "<set-locally>"
    if name in PRIVATE_CONTENT_KEYS:
        return {} if isinstance(value, dict) else "<set-locally>"
    if name == "custom_providers" and isinstance(value, list):
        return [_sanitize_provider(item, home) for item in value]
    if isinstance(value, dict):
        return {k: sanitize(v, home, str(k)) for k, v in value.items()}
    if isinstance(value, list):
        return [sanitize(item, home) for item in value]
    if isinstance(value, str):
        clean = value.replace(str(home), "${HOME}")
        if any(pattern.search(clean) for pattern in TOKEN_PATTERNS):
            return "<redacted>"
        if "-----BEGIN " in clean and "PRIVATE KEY-----" in clean:
            return "<redacted>"
        return clean
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()

    raw = yaml.safe_load(args.source.read_text())
    clean = sanitize(raw, Path.home())
    header = (
        "# Sanitized from a working Hermes installation.\n"
        "# Replace placeholders locally; never commit live auth or .env files.\n"
    )
    args.destination.parent.mkdir(parents=True, exist_ok=True)
    args.destination.write_text(
        header + yaml.safe_dump(clean, sort_keys=False, allow_unicode=True)
    )


if __name__ == "__main__":
    main()
