# Narrow Launch Plan

This plan targets maintainers who already feel the review problem: AI-assisted
infrastructure changes can sound more proven than they are. Keep every launch
claim tied to the public repository, synthetic examples, and `repo_only` proof.

Do not add private hostnames, IP addresses, domains, logs, runtime state, live
config, secrets, adoption claims, production claims, or external-service proof.

## Launch Goal

Reach a small set of practical audiences and get useful maintainer feedback on
the contract model:

- AI coding agent users who want safer PR handoffs.
- Homelab and self-hosted maintainers who publish infra docs carefully.
- DevOps and CI people who care about review gates.
- GitHub Actions users who want a copyable PR-body/privacy check.
- OSS maintainers reviewing AI-authored PRs.

The call to action is not "trust this in production." The call to action is:
try the synthetic demo, inspect the GitHub Actions template, and critique the
claim-boundary vocabulary.

## Core Pitch

Homelab Operator is a privacy-safe Python CLI and template pack for
AI-assisted infrastructure repos. It validates PR claim boundaries, lane
receipts, surface claims, synthetic estate examples, and privacy patterns so
source-only work is not presented as host, runtime, live-config, external
service, or end-to-end proof.

Use these public anchors:

- Repository: `https://github.com/paul-cch/homelab-operator`
- Demo: `docs/demo.md`
- GitHub Actions workflow: `docs/workflows/github-action.md`
- Claim-boundary concept: `docs/concepts/claim-boundaries.md`
- Social copy: `docs/application/social-posts.md`

## Audience Angles

| Audience | Problem to name | Angle | Concrete CTA |
| --- | --- | --- | --- |
| AI coding agent users | Agent PRs can overstate what a local check proved. | Make the PR body say exactly what was proven and what was not. | Run `check-pr` on a draft PR body and compare the failing/passing demo examples. |
| Homelab/self-hosted maintainers | Public infra examples can leak real operational details. | Keep examples synthetic while still documenting useful review contracts. | Read the privacy model and run `check-privacy` on public docs. |
| DevOps/CI people | Review gates usually test code, not claim quality. | Add a lightweight contract gate alongside normal test/build/lint CI. | Inspect the workflow template and the `doctor` output. |
| GitHub Actions users | PR-body checks are easy to skip or implement unsafely. | Use a read-only workflow that validates PR sections and scans checked-out text. | Copy the template into a test repository and keep normal CI required too. |
| OSS maintainers | AI-authored PRs need reviewable proof boundaries. | Separate source proof from deployment, runtime, live-config, and external-service claims. | Try the PR-body section vocabulary on one low-risk PR. |

## Channels

- GitHub repository surfaces: release notes, pinned issue, or discussion thread
  if the repo already uses that surface. Keep it factual and link the demo.
- X, Bluesky, or Mastodon: one short post with the synthetic demo link, then
  replies only when people ask concrete questions.
- LinkedIn: maintainer-focused explanation for AI-assisted infra review and
  CI governance.
- Hacker News: one "Show HN" post only after the demo link and README are easy
  to scan. Lead with the tool and the limitation, not the backstory.
- Reddit: one relevant community at a time, only where project posts are
  allowed. Prefer `r/selfhosted`, `r/homelab`, `r/devops`, or a GitHub Actions
  community when the post is framed as a useful review pattern.
- Dev.to or a personal blog: a short walk-through showing the unsafe PR body,
  corrected `repo_only` PR body, receipt, and `doctor` output.
- Existing maintainer communities: share only where Paul already participates
  or where project feedback is explicitly welcome. Do not cold-post into
  private teams or unrelated communities.

## One-Week Cadence

Day 0: Prep the launch pack. Re-run the repo demo, `doctor`, and privacy scan.
Pick three channels maximum for the first two days. Confirm all links point to
public synthetic examples.

Day 1: Publish the short general post on one microblogging channel and the
maintainer-focused post on LinkedIn. Respond to questions with links to the
demo, not private context.

Day 2: Share the CI/GitHub Actions angle. Point at the workflow template and
state clearly that it complements normal CI rather than replacing tests.

Day 3: Share the homelab/self-hosted angle in one rules-compatible community.
Ask for feedback on the privacy model and synthetic examples.

Day 4: Publish the longer walk-through or "Show HN" post. Include the
limitation up front: the demo proves source-side contract checks only.

Day 5: Share the OSS maintainer angle. Ask reviewers what claim-boundary
language would make AI-authored PRs easier to accept or reject.

Day 6: Triage feedback. Open or update public roadmap issues only for concrete
product gaps. Do not convert likes, replies, or private messages into adoption
claims.

Day 7: Post a factual follow-up if there is public feedback to summarize. Link
merged docs or issues, thank reviewers, and name the next `repo_only` milestone.
If there is no meaningful feedback, skip the recap and keep improving the docs.

## Reuse-Safe Post Variants

General:

> Homelab Operator is a privacy-safe Python CLI for AI-assisted infrastructure
> repos. It checks PR claim boundaries, lane receipts, synthetic examples, and
> `repo_only` proof so source checks are not mistaken for host, runtime, or
> live-config proof.

AI coding agent users:

> If an agent opens an infra PR, the review should say what was actually
> proven. Homelab Operator checks that PR bodies and receipts separate
> `repo_only` source proof from deployment, runtime, live-config, and external
> service claims.

Homelab/self-hosted maintainers:

> I made Homelab Operator for maintainers who want public infra examples without
> leaking private operational details. The repo uses synthetic examples and a
> privacy scan while still showing a useful PR/receipt contract.

DevOps/CI:

> Tests prove code behavior. They do not prove that a PR description stayed
> honest about deployment or runtime evidence. Homelab Operator adds a small PR
> contract gate for that review layer.

GitHub Actions:

> Homelab Operator includes a read-only GitHub Actions workflow template that
> validates PR-body sections and scans checked-out text for private operational
> material. It is meant to sit beside normal CI.

OSS maintainers:

> For AI-authored PRs, I want reviewers to see the proof boundary before they
> read the diff: source, host, runtime, live config, external service, or
> handoff needed. Homelab Operator is an early OSS toolkit for that contract.

## Reply Rules

- If asked whether it is production-proven, say the public demo is `repo_only`
  and synthetic.
- If asked for examples, link `docs/demo.md` and the example files.
- If asked how to adopt it, link the GitHub Actions workflow and say to keep
  existing tests/build/lint gates.
- If asked about private homelab details, decline and return to the public
  contract model.
- If feedback identifies a gap, open a roadmap issue instead of promising a
  live deployment or external integration.
