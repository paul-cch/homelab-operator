# Application Readiness Receipt

- Exit state: MERGE_READY
- Issue: None supplied
- Branch / worktree: `main`
- PR: not needed for initial public release
- Owned paths: repository-wide application packet
- Surface classification: repo source, GitHub coordination, release metadata
- Proof kind: github_coordination
- Claim proven: Homelab Operator is public, Apache-2.0 licensed, released as `v0.1.0`, and has passing CI.
- Claim not proven: no broad adoption, stars, forks, PyPI downloads, or external contributor activity yet.
- Repo gate: `python -m pytest`, `ruff check .`, package build, `twine check`
- Host/runtime handoff needed: no
- Host gate needed: no
- Runtime gate needed: no
- Live config gate needed: no
- Checks or commands run: local test/build/privacy gates and GitHub release/CI checks
- Blockers: none
- Next safe command: submit the OpenAI Codex for Open Source form using `docs/application/openai-codex-for-oss.md`

## Evidence

- Repository: `https://github.com/paul-cch/homelab-operator`
- Release: `https://github.com/paul-cch/homelab-operator/releases/tag/v0.1.0`
- Visibility: public
- License: Apache-2.0
- Role: primary maintainer

## Claim Proven

Homelab Operator is a public OSS repository with a recognized Apache-2.0
license, a pushed `main` branch, a `v0.1.0` GitHub release, package artifacts,
passing CI, tests, schemas, docs, templates, and a ready OpenAI Codex for OSS
application packet.

## Claim Not Proven

The project does not yet have broad adoption, stars, forks, PyPI downloads, or
external contributor activity. The application should present it as an early
project with clear ecosystem importance rather than as a widely adopted tool.

## Validation Evidence

- `python -m pytest`
- `ruff check .`
- `homelab-operator check-pr --body-file tests/fixtures/good_pr_body.md`
- `homelab-operator check-receipt --file tests/fixtures/good_receipt.md`
- `homelab-operator check-claim --json-file tests/fixtures/surface_claim.json`
- `python -m build`
- `python -m twine check dist/*`
- privacy scan for private Homelab identifiers and secret-bearing strings
- GitHub Actions CI success on `main`

## Next Safe Action

Submit the OpenAI Codex for Open Source form using
`docs/application/openai-codex-for-oss.md`.
