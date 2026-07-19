# Verification record

## Re-verification on 2026-07-19

- Patch series dry-run (`scripts/check.sh`): passed against
  `NousResearch/hermes-agent@6997dc81cd21dc88c6cb808a1fb3626b6ce71254`.
- Patch series apply (`scripts/apply.sh`): passed against the same clean
  checkout.
- Applied-tree comparison: the `0001-0004` series produces the same 47-file,
  8,965-insertion overlay as the previous single `patches/hermes-customizations.patch`.
- Kit validation:
  - `python3 -m pytest tests/ -q` — 18 passed.
  - `python3 scripts/scan-secrets.py .` — no findings.
  - `git diff --check -- . ':(exclude)patches/*.patch'` — clean.

## Original verification on 2026-07-16

Verified against upstream Hermes Agent commit
`6997dc81cd21dc88c6cb808a1fb3626b6ce71254`.

- Focused Hermes tests: 806 passed, 0 failed across 18 test files.
- Anonymized Safari accessibility fixture: all 10 filtering tests passed.
- Config export: all 554 key paths preserved; 28 sensitive or identity values
  replaced with placeholders.
- Strong credential signature scan: no findings.
- Tirith scan: no high-severity findings; one expected medium finding because
  the Hermes source patch legitimately discusses the system prompt.
- CuaDriver structural health check: `ok: true`.

The focused test command was:

```bash
scripts/run_tests.sh \
  tests/computer_use \
  tests/tools/test_computer_use.py \
  tests/tools/test_computer_use_capture_routing.py \
  tests/agent/test_context_compressor.py \
  tests/agent/test_context_files_mode.py \
  tests/agent/test_context_engine.py \
  tests/agent/test_prompt_builder.py \
  tests/agent/test_system_prompt.py \
  tests/run_agent/test_message_sequence_repair.py -q
```
