# Security

The detailed privacy and security boundary is documented in
[docs/SECURITY.md](docs/SECURITY.md).

## Reporting a vulnerability

Please open a private security advisory through GitHub or contact the maintainers
directly. Do not open public issues for security-sensitive findings.

## Sanitization reminders

- Never commit `.env` files, credentials, or private state.
- Run `python3 scripts/scan-secrets.py .` before publishing config updates.
- Inspect new fixtures and screenshots manually; accessibility trees and window
titles can contain private content even when no formal credential is present.
