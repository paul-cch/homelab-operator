# Agent Instructions

This is a public OSS repository. Keep all examples synthetic and privacy-safe.

## Boundaries

- Do not add private hostnames, IP addresses, domains, logs, runtime state, or
  live config.
- Do not claim host, runtime, live config, or external service proof unless a
  matching check exists in the public example.
- Prefer small, reviewable source changes with tests.

## Validation

Run:

```bash
python -m pip install -e ".[dev]"
python -m pytest
homelab-operator check-pr --body-file tests/fixtures/good_pr_body.md
```

Use `repo_only` proof for source and docs changes unless a separate public
example proves a deeper surface.
