#!/usr/bin/env bash
set -euo pipefail

kit_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
target="${1:-}"

if [[ -z "$target" ]]; then
  echo "Usage: $0 /path/to/clean/hermes-agent" >&2
  exit 2
fi

git -C "$target" apply --check "$kit_dir/patches/hermes-customizations.patch"
echo "Patch applies cleanly to $target"
