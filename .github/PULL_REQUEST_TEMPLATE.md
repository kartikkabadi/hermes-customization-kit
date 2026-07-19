## Summary

Briefly describe the change and why it is needed.

## Checklist

- [ ] `python3 -m pytest tests/ -v` passes.
- [ ] `python3 scripts/scan-secrets.py .` reports no findings.
- [ ] `git diff --check -- . ':(exclude)patches/*.patch'` is clean.
- [ ] Documentation updated if the change is user-facing.
- [ ] `local/config.sanitized.yaml` was regenerated if `export-config.py` changed.
