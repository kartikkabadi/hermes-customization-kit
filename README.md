# Hermes Computer-Use Customization Kit

[![CI](https://github.com/kartikkabadi/hermes-customization-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/kartikkabadi/hermes-customization-kit/actions/workflows/ci.yml)
[![GitHub release](https://img.shields.io/github/v/release/kartikkabadi/hermes-customization-kit)](https://github.com/kartikkabadi/hermes-customization-kit/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A compact, private overlay for Hermes Agent. It packages only the local changes
made on top of Nous Research's Hermes Agent—no upstream source mirror, runtime
state, credentials, histories, memories, logs, or compiled binaries.

The overlay focuses on deterministic macOS computer use through CuaDriver,
cache-aware context shaping and compaction, durable goal/permission continuity,
and the CLI/gateway behavior needed to support long-running work.

## Contents

- `patches/*.patch` — a numbered patch series containing the sanitized net
  source delta against the pinned upstream base. See `patches/README.md` for
  the feature breakdown.
- `local/config.sanitized.yaml` — non-secret behavioral settings exported from
  the working installation.
- `local/.env.local.example` — names of locally used environment variables,
  with no values.
- `local/hermes-launcher.example` — portable launcher matching the local
  command setup.
- `local/cua-driver.json.example` — non-secret CuaDriver capture preference.
- `scripts/apply.sh` — validates and applies the overlay to a clean Hermes
  checkout.
- `scripts/export-config.py` — repeatable config sanitizer.
- `docs/CUSTOMIZATIONS.md` — feature map and provenance.
- `docs/SECURITY.md` — what was excluded and how to rescan future exports.
- `docs/VERIFICATION.md` — reproducible validation results for this export.

## Quick start

```bash
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent
git checkout 6997dc81cd21dc88c6cb808a1fb3626b6ce71254
/path/to/hermes-customization-kit/scripts/apply.sh "$PWD"
```

Then follow [`docs/LOCAL_SETUP.md`](docs/LOCAL_SETUP.md) to install the
sanitized config and CuaDriver integration.

## Compatibility

The patch series is pinned to upstream commit
`6997dc81cd21dc88c6cb808a1fb3626b6ce71254` from 2026-07-14. Applying it to a
newer Hermes revision may require a deliberate rebase and regression test pass.

Hermes Agent is MIT-licensed by Nous Research. This kit retains that license
for the patch content derived from and modifying Hermes Agent.

See [NOTICE](NOTICE) for the full attribution.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for local validation steps and patch
update guidance.

## Security

This repository intentionally excludes credentials, histories, screenshots, and
private state. See [docs/SECURITY.md](docs/SECURITY.md) and
[SECURITY.md](SECURITY.md) for the privacy boundary and how to rescan exports.
