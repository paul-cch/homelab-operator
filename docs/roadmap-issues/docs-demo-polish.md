# Polish docs and demo assets for first-time adopters

Labels: `good first issue`, `roadmap`, `docs`, `demo`

## Summary

Improve first-run docs and demo material so a new adopter can understand the
proof ladder, run the CLI, and see a passing source-only check quickly.

## Why

Homelab Operator is easiest to trust when the examples make the proof boundary
obvious. A compact demo path can show the value without exposing private
infrastructure or implying live verification.

## Proposed Scope

- Add or polish a short demo script using synthetic fixtures.
- Add screenshots, terminal transcript snippets, or asciinema-style notes only
  if they are fully synthetic.
- Tighten first-run docs around install, commands, expected output, and blockers.
- Add a checklist for reviewers evaluating a source-only PR.

## Acceptance Criteria

- A new user can run one documented source-only flow from a clean checkout.
- Demo output uses synthetic names and no private operational material.
- Docs distinguish repo proof from runtime or live-service proof.
- Existing validation commands still pass.

## Out Of Scope

- Demoing real deployments.
- Publishing private runbooks or logs.
- Changing package behavior unless needed for a documented demo command.
