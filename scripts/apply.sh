#!/usr/bin/env bash
set -euo pipefail

kit_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
target="${1:-$PWD}"
base="$(tr -d '[:space:]' < "$kit_dir/UPSTREAM_BASE")"
patch="$kit_dir/patches/hermes-customizations.patch"

git -C "$target" rev-parse --is-inside-work-tree >/dev/null

if [[ -n "$(git -C "$target" status --porcelain)" ]]; then
  echo "Refusing to apply onto a dirty Hermes checkout: $target" >&2
  exit 1
fi

head="$(git -C "$target" rev-parse HEAD)"
if [[ "$head" != "$base" ]]; then
  echo "Expected Hermes base $base, found $head." >&2
  echo "Check out the pinned base or rebase the patch deliberately." >&2
  exit 1
fi

git -C "$target" apply --check "$patch"
git -C "$target" apply "$patch"

echo "Applied Hermes customization overlay to $target"
