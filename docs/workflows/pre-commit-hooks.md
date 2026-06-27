# Pre-Commit Hooks

Homelab Operator publishes opt-in `pre-commit` hooks for local contract checks.
They are a contributor convenience, not a replacement for CI or PR review.

## Example Config

Add this to a consuming repository's `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/paul-cch/homelab-operator
    rev: main
    hooks:
      - id: homelab-operator-check-privacy
      - id: homelab-operator-doctor
```

Use a released tag instead of `main` once the hook metadata is available in a
release. Then run:

```bash
python -m pip install pre-commit
pre-commit run homelab-operator-check-privacy --all-files
pre-commit run homelab-operator-doctor --all-files
```

For contract fixture or generated-template work, a targeted local run can name
the files that should trigger the hook while the checker still scans from the
repository root:

```bash
pre-commit run homelab-operator-check-privacy --files \
  .github/pull_request_template.md \
  tests/fixtures/good_pr_body.md \
  examples/minimal-homelab/estate.yaml \
  templates/github/workflows/homelab-operator-contract.yml
```

## What The Hooks Scan

`homelab-operator-check-privacy` runs:

```bash
homelab-operator check-privacy --root .
```

It scans UTF-8 text files under the repository root, skipping `.git`, `.venv`,
`.pytest_cache`, `.ruff_cache`, `build`, `dist`, and `__pycache__`. It ignores
binary or non-UTF-8 files. The built-in patterns catch private IP addresses,
credential assignments, and private key blocks.

`homelab-operator-doctor` runs:

```bash
homelab-operator doctor --root .
```

It validates the bundled PR, receipt, claim, estate, and privacy fixtures. Use
it for this repository or repositories that carry the Homelab Operator fixture
layout. For a repository that only wants leak detection, enable the privacy hook
alone.

## Proof Boundary

Passing these hooks proves only repository-local source, docs, examples, and
fixture checks. It does not prove host checkout state, runtime export, live
config, external service health, deployment, release, or package publish state.
