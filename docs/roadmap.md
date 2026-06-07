# Public Roadmap

Homelab Operator has a stable v1.0.0 contract surface. The next public work is
about making that surface easier to adopt in ordinary repositories: clearer CLI
entry points, friendlier CI output, small integration examples, and polished
synthetic demos.

This roadmap is intentionally repo-only. It does not claim host, runtime,
live-config, or external-service proof.

## Principles

- Keep examples synthetic and privacy-safe.
- Make every feature state which proof surface it validates.
- Prefer small CLI and CI improvements that are easy to review.
- Keep first contributor tasks scoped enough for one focused pull request.

## Near Term

- Add a CLI command for validating files against the bundled JSON Schemas.
- Add SARIF output for contract and privacy scans.
- Provide a pre-commit hook path for local contract checks.
- Allow configurable privacy scan patterns without weakening the defaults.
- Expand GitHub Action examples for common source-only and handoff checks.

## Next

- Parse richer synthetic estate files while preserving the current simple
  examples.
- Emit CI annotations that point directly to failing contract sections.
- Polish docs and demo assets so a new adopter can understand the proof ladder
  in a few minutes.

## Issue Drafts

- [Add a CLI command for JSON Schema validation](roadmap-issues/json-schema-cli-validation.md)
  ([#6](https://github.com/paul-cch/homelab-operator/issues/6))
- [Emit SARIF output for contract and privacy checks](roadmap-issues/sarif-output.md)
  ([#9](https://github.com/paul-cch/homelab-operator/issues/9))
- [Add a pre-commit hook for local contract checks](roadmap-issues/pre-commit-hook.md)
  ([#7](https://github.com/paul-cch/homelab-operator/issues/7))
- [Support configurable privacy scan patterns](roadmap-issues/configurable-privacy-patterns.md)
  ([#3](https://github.com/paul-cch/homelab-operator/issues/3))
- [Add GitHub Action examples for common proof lanes](roadmap-issues/github-action-examples.md)
  ([#5](https://github.com/paul-cch/homelab-operator/issues/5))
- [Expand synthetic estate parsing](roadmap-issues/richer-estate-parsing.md)
  ([#8](https://github.com/paul-cch/homelab-operator/issues/8))
- [Add CI annotations for contract failures](roadmap-issues/ci-annotations.md)
  ([#2](https://github.com/paul-cch/homelab-operator/issues/2))
- [Polish docs and demo assets for first-time adopters](roadmap-issues/docs-demo-polish.md)
  ([#4](https://github.com/paul-cch/homelab-operator/issues/4))
