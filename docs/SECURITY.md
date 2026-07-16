# Security and privacy boundary

This kit is intentionally an overlay, not a backup of `~/.hermes`.

Excluded categories include live `.env` values, auth files, credential pools,
provider tokens, messaging IDs, sessions, memories, user profiles, histories,
cron state, databases, logs, caches, screenshots, browser text, telemetry IDs,
compiled binaries, virtual environments, dependencies, and build artifacts.

The config exporter redacts secret-like keys, messaging/account identifiers,
private-content fields, home-directory paths, common token formats, and private
keys. It is a defense-in-depth helper, not permission to publish without review.

Before updating the patch or config, rerun:

```bash
python3 scripts/scan-secrets.py .
git diff --check -- . ':(exclude)patches/*.patch'
rg -n -i 'BEGIN .*PRIVATE KEY|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{30,}|gh[pousr]_[0-9A-Za-z]{20,}|sk-(ant-)?[0-9A-Za-z_-]{16,}|xox[baprs]-[0-9A-Za-z-]{10,}' .
```

Also inspect new fixtures manually. Accessibility trees, window titles, URLs,
and screenshots may contain private content even when they contain no formal
credential.
