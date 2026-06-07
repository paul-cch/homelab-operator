# Social Post Variants

These are safe public variants for announcing Homelab Operator to narrow
audiences: AI coding agent users, homelab/self-hosted maintainers, DevOps and
CI people, GitHub Actions users, and OSS maintainers reviewing AI-authored PRs.

Replace the repo URL only if the canonical public URL changes. Do not add
private infrastructure details, live runtime claims, production claims, or
adoption claims.

Repository: `https://github.com/paul-cch/homelab-operator`

## General Short

I built Homelab Operator, a privacy-safe Python CLI for AI-assisted
infrastructure repos.

It checks PR claim boundaries, lane receipts, synthetic examples, and
`repo_only` proof so source checks are not mistaken for host, runtime,
live-config, or external-service proof.

Synthetic demo and docs: `https://github.com/paul-cch/homelab-operator`

## AI Coding Agent Users

If an AI coding agent opens an infrastructure PR, the review should say what
was actually proven.

Homelab Operator checks that PR bodies and lane receipts separate `repo_only`
source proof from host, runtime, live-config, deployment, and external-service
claims.

Synthetic demo: `https://github.com/paul-cch/homelab-operator`

## Homelab And Self-Hosted Maintainers

Homelab Operator is for maintainers who want public infrastructure examples
without leaking private operational details.

The repo uses synthetic examples and privacy-safe contract checks for PR
bodies, lane receipts, surface claims, and example estate files. The demo is
`repo_only`; it does not claim live host or runtime proof.

`https://github.com/paul-cch/homelab-operator`

## DevOps And CI

Tests prove code behavior. They do not prove that a PR description stayed honest
about deployment, runtime, live-config, or external-service evidence.

Homelab Operator adds a small contract layer for that review gap: `check-pr`,
`check-receipt`, `check-claim`, `check-privacy`, and `doctor`.

`https://github.com/paul-cch/homelab-operator`

## GitHub Actions Users

Homelab Operator includes a read-only GitHub Actions workflow template that
validates PR-body sections and scans checked-out text for private operational
material.

It is meant to sit beside normal tests/builds/linting, not replace them.

`https://github.com/paul-cch/homelab-operator`

## OSS Maintainers

For AI-authored PRs, I want reviewers to see the proof boundary before they
read the diff: source, host checkout, runtime export, live config, external
service, or handoff needed.

Homelab Operator is an early OSS toolkit for making that contract explicit in
PR bodies, receipts, and CI checks.

`https://github.com/paul-cch/homelab-operator`

## Show HN Draft

Title:

```text
Show HN: Homelab Operator - PR contract checks for AI-assisted infra repos
```

Body:

```text
I built a small Python CLI for maintainers using coding agents on infrastructure
repos. It validates PR claim boundaries, lane receipts, surface claims,
synthetic estate examples, and privacy patterns.

The demo is intentionally synthetic and repo-only: it shows an unsafe PR body
failing, a corrected PR body passing, a merge-ready receipt passing, and the
project doctor running. It does not claim host, runtime, live-config, or
external-service proof.

I would be especially interested in feedback from maintainers who review
AI-authored PRs or run GitHub Actions gates.
```

## Application Context

Homelab Operator is an early OSS toolkit for evidence-based AI-assisted
infrastructure maintenance. It provides a Python CLI, schemas, templates,
synthetic examples, and a GitHub Actions workflow that keep private operational
details out of public docs while making unproven host, runtime, live-config, and
external-service claims visible during review.

## 280-Character Variant

Homelab Operator is a privacy-safe Python CLI for AI-assisted infra repos. It
checks PR claim boundaries, lane receipts, synthetic examples, and `repo_only`
proof so source checks are not mistaken for host/runtime/live-config proof.

## Follow-Up Reply

The public demo is deliberately `repo_only`: unsafe PR body fails, corrected PR
body passes, receipt passes, and `doctor` reports bundled contract checks. It
does not claim deployment, runtime, live-config, external-service, or adoption
proof.

## Notes Before Posting

- Do not claim real deployment, runtime, live-config, or external-service proof.
- Do not imply adoption, contributor activity, production usage, or community
  endorsement.
- Link to the synthetic demo rather than describing private workflows or private
  infrastructure.
- Keep "homelab" as the project context, not as evidence of a published private
  estate.
- When posting to communities, read the rules first and avoid cross-posting the
  same copy to multiple places on the same day.
