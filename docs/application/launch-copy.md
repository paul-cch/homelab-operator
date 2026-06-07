# Launch Copy

Use this file as the public copy source for the repository description,
application forms, launch posts, and maintainer notes. Keep claims tied to
synthetic examples and `repo_only` proof unless a separate public check proves a
deeper surface.

## Repository Description

Privacy-safe contract checks for AI-assisted infrastructure repos: validate PR
claim boundaries, lane receipts, synthetic estate examples, and `repo_only`
proof before source work is mistaken for runtime proof.

## Short Project Summary

Homelab Operator is a small Python CLI and template pack for maintainers using
AI agents on infrastructure repositories. It checks whether pull requests,
receipts, surface claims, and example estates clearly separate source proof from
host, runtime, live-config, and external-service claims.

The public repo uses synthetic examples only. Its demo shows an unsafe PR body
failing, a corrected `repo_only` PR body passing, a merge-ready receipt passing,
and `homelab-operator doctor --root .` reporting the bundled contract checks.

## Application Copy

Homelab Operator helps maintainers keep AI-assisted infrastructure changes
evidence-based. It validates PR claim boundaries, lane receipts, JSON surface
claims, and synthetic estate examples so source-only work is not presented as
host, runtime, live-config, external-service, or end-to-end proof.

The project is intentionally privacy-safe: public examples use synthetic names
and do not publish real hostnames, addresses, logs, runtime state, live config,
or secrets. The main evidence for this launch pack is `repo_only` proof from the
demo files and local contract checks.

## Demo Anchor

Point reviewers to:

- `docs/demo.md` for the synthetic walk-through.
- `examples/demo/unsafe-pr-body.md` for the failing claim-boundary example.
- `examples/demo/corrected-pr-body.md` for the passing `repo_only` PR example.
- `examples/demo/merge-ready-receipt.md` for the passing receipt.
- `docs/concepts/claim-boundaries.md` for the proof vocabulary.

## Maintainer Notes

- Lead with "privacy-safe repo-only contract checker", not broad automation or
  deployment claims.
- Say the tool checks the language and structure of source-side agent work. Do
  not imply that it proves a real host, runtime, live config, or external
  service unless that public proof exists.
- Keep examples synthetic. Do not paste private infrastructure names, IP
  addresses, domains, logs, runtime exports, live config, or secret-shaped
  strings into public launch material.
- Use concrete validation language: `check-pr`, `check-receipt`, `check-claim`,
  `check-estate`, `check-privacy`, and `doctor`.
- Be honest about maturity. Position it as an early OSS toolkit with clear
  contracts and reusable examples, not as a widely adopted standard.
- When discussing Codex or other agents, frame the project as a guardrail for
  maintainer review: it makes unproven claims visible before they become
  operational assumptions.
