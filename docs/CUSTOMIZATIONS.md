# Customization map

The patch series captures the net result of 24 local commits on top of Hermes Agent
commit `6997dc81cd21dc88c6cb808a1fb3626b6ce71254`. Before privacy sanitization,
the delta covered 58 files with 12,531 insertions and 389 deletions. The final
overlay contains 57 files with 12,096 insertions and 389 deletions.

## Computer use and CuaDriver

- Structured CuaDriver payload extraction with backward-compatible action
  shapes.
- Configurable accessibility-tree depth, element budgets, and app-specific
  queries.
- Passive-role and unlabeled-ghost filtering.
- Browser page actions plus Safari Apple Events diagnostics.
- Accessibility-only capture, screenshot fallback, pixel-bound rescaling, and
  sparse-browser hints.
- Deterministic background targeting, menu-bar surface classification, window
  title redaction, permission handling, transport recovery, duplicate-loop
  prevention, and input ownership.

## Context and compaction

- Cache-aware context working sets and sparse project-context loading.
- Configurable context compression and historical tool-receipt collapsing.
- Message-sequence repair, context accounting, and continuity across long
  computer-use runs.

## Agent and runtime integration

- Goal-bound durable permission leases.
- Stronger approvals, tool guardrails, tool search, and execution semantics.
- Supporting CLI, gateway, Telegram, TUI, and configuration behavior.
- Focused behavioral tests for the modified paths.

## Sanitization adjustment

One captured Safari fixture contained a screenshot and another contained live X
notification text. The screenshot fixture was removed from the overlay because
it was unused. The accessibility fixture was structurally anonymized while
preserving roles, frames, parent relationships, and test behavior.

## Local source commits

The unpublished intermediate commit subjects are preserved here for provenance:

1. Promote CuaDriver text-part payloads to structured content.
2. Wire capture limits and queries through per-app config.
3. Drop passive accessibility roles and ghost elements.
4. Surface browser page-tool hints for sparse trees.
5. Retry screenshot-missing cases through CLI-to-file capture.
6. Skip screenshots in accessibility-only mode.
7. Preserve legacy action payload shapes.
8. Rescale bounds to screenshot pixel space.
9. Add browser page actions and Apple Events prerequisites.
10. Improve Safari Apple Events diagnostics.
11. Harden autonomous computer use and context continuity.
12. Merge the then-current upstream main branch.
13. Compile cache-aware context working sets.
14. Scope named-app window inventory.
15. Redact window titles before inference.
16. Configure sparse project context.
17. Harden background app launch permissions.
18. Make background targeting deterministic.
19. Classify menu-bar app surfaces.
20. Collapse historical tool-protocol receipts.
21. Bind durable permission leases to goals.
22. Recover repeated driver transport closure.
23. Stop duplicate perception loops.
24. Enforce background input ownership.
