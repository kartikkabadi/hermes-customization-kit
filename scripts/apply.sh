#!/usr/bin/env bash
set -euo pipefail

shopt -s nullglob

kit_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
target="${1:-$PWD}"
base_file="$kit_dir/UPSTREAM_BASE"

if [[ ! -f "$base_file" ]]; then
  echo "Missing upstream base file: $base_file" >&2
  exit 1
fi

base="$(tr -d '[:space:]' < "$base_file")"
if [[ -z "$base" ]]; then
  echo "UPSTREAM_BASE is empty: $base_file" >&2
  exit 1
fi

if [[ ! -d "$target" ]]; then
  echo "Target directory does not exist: $target" >&2
  exit 1
fi

if ! git -C "$target" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Target is not a git repository: $target" >&2
  exit 1
fi

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

patches=("$kit_dir"/patches/*.patch)
if [[ ${#patches[@]} -eq 0 ]]; then
  echo "No patch files found in $kit_dir/patches/" >&2
  exit 1
fi

for patch in "${patches[@]}"; do
  git -C "$target" apply --check "$patch"
done

for patch in "${patches[@]}"; do
  git -C "$target" apply "$patch"
done

echo "Applied Hermes customization overlay to $target"
