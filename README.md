# Homelab Operator

Homelab Operator is a contract layer for AI-assisted infrastructure maintenance.
It helps coding agents and human maintainers keep source changes, GitHub
coordination, host checkout state, runtime exports, live mutable config, and
external service proof separate.

The project is intentionally boring: templates, schemas, receipts, and a small
Python CLI that makes agents say what they changed, what they verified, what
they did not verify, and the next safe handoff.

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
agent-authored work stays reviewable.

## Quickstart

```bash
python -m pip install -e ".[dev]"
homelab-operator check-pr --body-file tests/fixtures/good_pr_body.md
homelab-operator check-pr --body-file tests/fixtures/good_pr_body.md --json
homelab-operator receipt-template --state MERGE_READY
homelab-operator check-receipt --file tests/fixtures/good_receipt.md
homelab-operator check-claim --json-file tests/fixtures/surface_claim.json
homelab-operator check-estate --file examples/minimal-homelab/estate.yaml
homelab-operator doctor --root .
```

Expected result:

```text
PR_CONTRACT_OK
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
- [Proof ladder](docs/concepts/proof-ladder.md)
- [Command reference](docs/commands.md)
- [Claim boundaries](docs/concepts/claim-boundaries.md)
- [Privacy model](docs/concepts/privacy.md)
- [GitHub Action workflow](docs/workflows/github-action.md)
- [Source change workflow](docs/workflows/source-change.md)
- [Deploy handoff workflow](docs/workflows/deploy-handoff.md)
- [Watcher automation workflow](docs/workflows/watcher-automation.md)
- [Blocked with evidence workflow](docs/workflows/blocked-with-evidence.md)
- [Dogfooding workflow](docs/workflows/dogfooding.md)
- [Distribution notes](docs/distribution.md)
- [Public roadmap](docs/roadmap.md)
- [OpenAI Codex for OSS application packet](docs/application/openai-codex-for-oss.md)
- [Launch copy and repository topics](docs/application/launch-copy.md)

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
