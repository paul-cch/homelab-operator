# Homelab Operator

[![CI](https://github.com/paul-cch/homelab-operator/actions/workflows/ci.yml/badge.svg)](https://github.com/paul-cch/homelab-operator/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](pyproject.toml)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)

Homelab Operator is a privacy-safe contract checker for AI-assisted
infrastructure PRs.

It helps maintainers review agent-authored work without blurring claim
boundaries: a local source check can prove repo coherence, but it cannot prove
host checkout, runtime export, live config, or external service health. The CLI
validates PR bodies, lane receipts, JSON surface claims, synthetic estate
examples, and privacy scans so every handoff says what was and was not verified.

## Try It In 2 Minutes

Run the synthetic `repo_only` demo from a clean checkout:

```bash
git clone https://github.com/paul-cch/homelab-operator.git
cd homelab-operator
python3 -m pip install -e ".[dev]"
homelab-operator check-pr --body-file examples/demo/unsafe-pr-body.md || true
homelab-operator check-pr --body-file examples/demo/corrected-pr-body.md
homelab-operator doctor --root .
```

You should see the unsafe PR fail for a missing claim boundary, the corrected
`repo_only` PR pass, and the project doctor end with
`HOMELAB_OPERATOR_DOCTOR_OK`.

## What Reviewers Get

- a shared proof ladder for repo source, GitHub coordination, host checkout,
  runtime export, live config, and external service checks
- PR and receipt contracts that put "claim proven" and "claim not proven" into
  the review surface
- privacy-safe examples that are synthetic by default
- JSON output for CI and agent handoffs

## Proof Demo

Before: this PR body overclaims runtime proof from a local source check. With no
claim boundary, `check-pr` fails:

```bash
cat > /tmp/pr.md <<'EOF'
## Summary
Patch the dashboard and confirm the service is healthy in production.
## Linked Issue
Closes #42
## Owned Paths
- `README.md`
## Validation
- `python -m pytest` passed.
EOF

homelab-operator check-pr --body-file /tmp/pr.md
# ERROR PR body must state the source/host/runtime/live-config claim boundary
```

After: bound the claim to the proof that actually ran, and it passes:

```bash
cat > /tmp/pr.md <<'EOF'
## Summary
Clarify the dashboard documentation.
## Linked Issue
Refs #42
## Owned Paths
- `README.md`
## Validation
- `python -m pytest` passed.
## Claim Boundary
Proof kind: repo_only.
Claim proven: local documentation and tests are coherent.
Claim not proven: no host checkout, runtime export, live config, or external service was checked.
EOF

homelab-operator check-pr --body-file /tmp/pr.md
# PR_CONTRACT_OK
```

## Why this exists

Coding agents are increasingly good at editing infrastructure repos. They are
much less reliable at naming the exact surface they proved. A local test can
prove source coherence; it cannot prove a host pulled the change, a runtime was
exported, or a live service is healthy.

Homelab Operator gives maintainers a reusable proof vocabulary and CI checks so
agent-authored work stays reviewable. The project is intentionally boring:
templates, schemas, receipts, and a small Python CLI that makes agents say what
they changed, what they verified, what they did not verify, and the next safe
handoff.

## More Local Checks

After installing from the try path, these commands exercise the rest of the
contract surface:

```bash
homelab-operator check-pr --body-file tests/fixtures/good_pr_body.md
homelab-operator check-pr --body-file tests/fixtures/good_pr_body.md --json
homelab-operator receipt-template --state MERGE_READY
homelab-operator check-receipt --file tests/fixtures/good_receipt.md
homelab-operator check-claim --json-file tests/fixtures/surface_claim.json
homelab-operator check-estate --file examples/minimal-homelab/estate.yaml
homelab-operator doctor --root .
```

Expected plain-text checks include:

```text
PR_CONTRACT_OK
RECEIPT_CONTRACT_OK
SURFACE_CLAIM_OK
ESTATE_CONTRACT_OK
HOMELAB_OPERATOR_DOCTOR_OK
```

## Proof ladder

| Surface | What it can prove | What it cannot prove |
| --- | --- | --- |
| Repo source | Code, docs, and tests are coherent locally | Host deploy or runtime behavior |
| GitHub issue / PR | Reviewable coordination, owned paths, CI state | Live deployment unless live evidence is attached |
| Host checkout | Target host has intended source and host gate passed | Runtime export unless export checks ran |
| Runtime export | Running/exported behavior on the target runtime | Source continuity without deploy marker evidence |
| Live config | Redacted config shape or freshness | Source deployment; secret values must stay private |
| External service | A specific integration check passed | Broader estate health |

## Contract checks

`homelab-operator check-pr` validates that a pull request body includes:

- `## Summary`
- `## Linked Issue` or `## Linked Issues`
- `## Owned Paths`
- `## Validation` or `## Verification`
- a claim boundary section, such as `## Claim Boundary`

It also catches common unsafe patterns:

- empty placeholder bullets
- `Closes #` without an issue number
- partial work using closing keywords
- validation sections without commands, results, or explicit blockers
- PRs that omit the source/host/runtime/live-config boundary

## Commands

| Command | Purpose |
| --- | --- |
| `homelab-operator check-pr` | Validate a Markdown PR body. |
| `homelab-operator receipt-template` | Print a lane receipt template for an exit state. |
| `homelab-operator check-receipt` | Validate a Markdown lane receipt. |
| `homelab-operator check-claim` | Validate a JSON surface claim. |
| `homelab-operator check-estate` | Validate a simple example estate file. |
| `homelab-operator check-privacy` | Scan text files for private operational material. |
| `homelab-operator doctor` | Run the built-in project contract checks. |
| `homelab-operator init` | Install templates into another repository. |

Most validation commands also accept `--json` for machine-readable CI or agent
handoff output.

## Install into another repo

```bash
homelab-operator init --target /path/to/repo
```

This writes:

- `AGENTS.md`
- `.github/pull_request_template.md`
- `.github/workflows/homelab-operator-contract.yml`
- `docs/homelab-operator/lane-receipt.md`

Existing files are skipped unless `--force` is passed.

## Documentation

- [Demo walkthrough](docs/demo.md)
- [Shareable demo asset](docs/assets/demo-terminal.svg)
- [Proof ladder](docs/concepts/proof-ladder.md)
- [Command reference](docs/commands.md)
- [Claim boundaries](docs/concepts/claim-boundaries.md)
- [Privacy model](docs/concepts/privacy.md)
- [GitHub Action workflow](docs/workflows/github-action.md)
- [Pre-commit hooks](docs/workflows/pre-commit-hooks.md)
- [Source change workflow](docs/workflows/source-change.md)
- [Deploy handoff workflow](docs/workflows/deploy-handoff.md)
- [Watcher automation workflow](docs/workflows/watcher-automation.md)
- [Blocked with evidence workflow](docs/workflows/blocked-with-evidence.md)
- [Dogfooding workflow](docs/workflows/dogfooding.md)
- [Contributing guide](CONTRIBUTING.md)
- [Safe first PR guide](docs/contributing/first-pr.md)
- [Distribution notes](docs/distribution.md)
- [PyPI readiness](docs/release/pypi-readiness.md)
- [Public roadmap](docs/roadmap.md)
- [Essay: Source tests are not runtime proof](docs/essays/source-tests-are-not-runtime-proof.md)
- [OpenAI Codex for OSS application packet](docs/application/openai-codex-for-oss.md)
- [Launch copy](docs/application/launch-copy.md)
- [Narrow launch plan](docs/application/launch-plan.md)
- [Social posts](docs/application/social-posts.md)
- [Repository topics](docs/application/repo-topics.md)

## Public examples only

The examples in this repository are synthetic. They use fake hosts, fake
surfaces, fake receipts, and fake service names. Do not publish private
topology, secrets, logs, runtime state, live config, or personal operating
history in examples.

## Status

Released as `v1.0.0`. The stable command surface includes:

- working PR contract checks
- lane receipt templates and validators
- JSON surface-claim checks
- simple estate checks
- privacy scanning
- project doctor checks
- JSON Schemas
- synthetic example estates
- GitHub Actions integration
- docs for source-only, handoff, no-op, and blocked lanes
