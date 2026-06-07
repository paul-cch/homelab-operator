# Add GitHub Action examples for common proof lanes

Labels: `good first issue`, `roadmap`, `github-actions`, `docs`

## Summary

Add copyable GitHub Action examples for source-only validation, PR contract
checks, lane receipt checks, privacy scanning, and schema validation once the
schema CLI exists.

## Why

The project is most useful when maintainers can wire it into review quickly.
Small workflow examples would help adopters understand which checks prove repo
source state and which checks do not prove runtime or live-service state.

## Proposed Scope

- Add workflow snippets using synthetic file names and paths.
- Include examples for pull request checks and scheduled source-only checks.
- Explain expected command results without claiming live proof.
- Keep examples minimal enough to copy into another repository.

## Acceptance Criteria

- Each workflow snippet names its proof boundary.
- Commands align with the current CLI surface.
- The examples avoid real project names, private infrastructure, and logs.
- Any new example files are validated by tests or `doctor` where practical.

## Out Of Scope

- Creating actions that deploy, restart services, or read live config.
- Publishing marketplace actions.
- Creating GitHub issues or repository settings changes.
