# Changelog

## [0.1.0] - 2026-07-19

### Added

- Initial public release of the Hermes Customization Kit overlay.
- `LICENSE` (MIT) and `NOTICE` for upstream Nous Research attribution.
- `README.md`, `docs/`, and sanitized example configuration files.
- `scripts/apply.sh` and `scripts/check.sh` to apply/verify the patch series against a clean Hermes Agent checkout.
- `scripts/export-config.py` to sanitize private Hermes configuration for publication.
- `scripts/scan-secrets.py` to detect common credential signatures.
- GitHub Actions CI that compiles scripts, scans secrets, runs unit tests, and verifies the patch applies cleanly to the pinned upstream commit.
- Unit tests for `apply.sh`, `check.sh`, `scan-secrets.py`, and `export-config.py`.
