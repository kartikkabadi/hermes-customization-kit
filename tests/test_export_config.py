import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def load_export_config():
    spec = importlib.util.spec_from_file_location(
        "export_config", str(ROOT / "scripts" / "export-config.py")
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def sanitizer():
    return load_export_config()


class TestSanitize:
    def test_api_key_redacted(self, sanitizer):
        assert sanitizer.sanitize({"api_key": "sk-live"}, Path.home()) == {
            "api_key": "<set-via-environment>"
        }

    def test_secret_suffix_redacted(self, sanitizer):
        assert sanitizer.sanitize({"bedrock_secret": "abc"}, Path.home()) == {
            "bedrock_secret": "<set-via-environment>"
        }

    def test_identity_scalar_redacted(self, sanitizer):
        assert sanitizer.sanitize({"user_id": "u-123"}, Path.home()) == {
            "user_id": "<set-locally>"
        }

    def test_identity_list_emptied(self, sanitizer):
        assert sanitizer.sanitize({"allowed_chats": [1, 2, 3]}, Path.home()) == {
            "allowed_chats": []
        }

    def test_private_content_scalar_redacted(self, sanitizer):
        assert sanitizer.sanitize({"ref_audio": "/tmp/voice.wav"}, Path.home()) == {
            "ref_audio": "<set-locally>"
        }

    def test_private_content_dict_emptied(self, sanitizer):
        assert sanitizer.sanitize({"template_vars": {"foo": "bar"}}, Path.home()) == {
            "template_vars": {}
        }

    def test_home_path_replaced(self, sanitizer, monkeypatch):
        home = Path("/home/user")
        assert sanitizer.sanitize(str(home / "config.yaml"), home) == "${HOME}/config.yaml"

    def test_token_pattern_redacted(self, sanitizer):
        raw = "aws=AKIA0123456789ABCDEF"
        assert sanitizer.sanitize(raw, Path.home()) == "<redacted>"

    def test_private_key_redacted(self, sanitizer):
        raw = "-----BEGIN PRIVATE KEY-----\nabc\n-----END PRIVATE KEY-----"
        assert sanitizer.sanitize(raw, Path.home()) == "<redacted>"

    def test_custom_provider_name_and_base_url_redacted(self, sanitizer):
        data = {
            "custom_providers": [
                {
                    "name": "My Private Endpoint",
                    "base_url": "https://private.example.com/v1",
                    "api_key": "sk-secret",
                    "model": "public/model",
                }
            ]
        }
        result = sanitizer.sanitize(data, Path.home())
        provider = result["custom_providers"][0]
        assert provider["name"] == "<set-locally>"
        assert provider["base_url"] == "<set-locally>"
        assert provider["api_key"] == "<set-via-environment>"
        assert provider["model"] == "public/model"

    def test_custom_provider_preserves_already_redacted(self, sanitizer):
        data = {
            "custom_providers": [
                {
                    "name": "<set-locally>",
                    "base_url": "<set-locally>",
                    "api_key": "<set-via-environment>",
                }
            ]
        }
        assert sanitizer.sanitize(data, Path.home()) == data
