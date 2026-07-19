# Contributing to Hermes Customization Kit

Thanks for helping improve this overlay.

## Quick checks before submitting

1. Install dependencies and run the test suite:
   ```bash
   pip install -r requirements-dev.txt
   python3 -m pytest tests/ -v
   ```
2. Run the secret scanner:
   ```bash
   python3 scripts/scan-secrets.py .
   ```
3. Check for whitespace errors:
   ```bash
   git diff --check -- . ':(exclude)patches/*.patch'
   ```
4. If you changed `scripts/export-config.py`, regenerate `local/config.sanitized.yaml` from a private source and verify it contains no live credentials or identity metadata.

## Patch changes

- The patch series in `patches/*.patch` is pinned to the upstream commit in `UPSTREAM_BASE`.
- If you update the patches, update `UPSTREAM_BASE`, `docs/VERIFICATION.md`, `patches/README.md`, and the `Compatibility` section in `README.md`.
- Keep the patch files free of screenshots, private paths, and credentials.

## Pull requests

- Keep each PR focused on a single concern.
- Add tests for script changes.
- Reference the relevant upstream Hermes Agent issue or commit when applicable.

## Code of Conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
