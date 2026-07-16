# Local setup

## Apply the source overlay

Use `scripts/apply.sh` with a clean Hermes Agent checkout pinned to the commit in
`UPSTREAM_BASE`. The script refuses a dirty checkout or a mismatched revision.

## Restore behavioral configuration

Review `local/config.sanitized.yaml`, replace placeholders locally, and copy it
to `~/.hermes/config.yaml`. Put credentials only in `~/.hermes/.env` or a
supported secret provider. `local/.env.local.example` is a variable-name
checklist, not a file to fill and commit.

## Restore commands and CuaDriver

Copy `local/hermes-launcher.example` to `~/.local/bin/hermes`, make it
executable, and ensure `~/.local/bin` is on `PATH`. Install CuaDriver separately;
the audited setup used version `0.7.1` and linked its skill from
`~/.cua-driver/skills/cua-driver` into Hermes.

Verify the native integration without extracting private app text:

```bash
hermes --version
cua-driver --version
cua-driver doctor --json
```

Then run the focused Hermes tests from the patched checkout:

```bash
scripts/run_tests.sh tests/computer_use tests/tools/test_computer_use.py -q
scripts/run_tests.sh tests/agent/test_context_compressor.py -q
```
