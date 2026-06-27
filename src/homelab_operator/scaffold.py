"""Scaffold files installed by `homelab-operator init`."""

from __future__ import annotations

INIT_FILES = {
    "AGENTS.md": """# Agent Instructions

This repository uses Homelab Operator contracts for agent-authored changes.

## Boundaries

- Classify whether work touches repo source, GitHub coordination, host checkout,
  runtime export, live config, or an external service.
- Do not claim a deeper surface than you actually verified.
- Keep examples and receipts free of secrets, private topology, and raw logs.

## Validation

Run the project gate and end non-trivial work with a lane receipt.
""",
    ".github/pull_request_template.md": """## Summary

-

## Linked Issue

Refs #

## Owned Paths

- `path/to/file`

## Validation

- `command` result

## Claim Boundary

Proof kind:

Claim proven:

Claim not proven:

Host/runtime/live-config handoff needed:
""",
    ".github/workflows/homelab-operator-contract.yml": """name: Homelab Operator Contract

on:
  pull_request:
    types: [opened, edited, synchronize, reopened]

jobs:
  pr-contract:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: read
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: python -m pip install git+https://github.com/paul-cch/homelab-operator.git
      - name: Write PR body
        env:
          PR_BODY: ${{ github.event.pull_request.body }}
        run: printf '%s' "$PR_BODY" > /tmp/pr-body.md
      - run: homelab-operator check-pr --body-file /tmp/pr-body.md --github-annotations
      - run: homelab-operator check-privacy --root . --github-annotations
""",
    "docs/homelab-operator/lane-receipt.md": """## Agent Lane Receipt

- Exit state:
- Issue:
- Branch / worktree:
- PR:
- Owned paths:
- Surface classification:
- Proof kind:
- Claim proven:
- Claim not proven:
- Repo gate:
- Host/runtime handoff needed:
- Host gate needed:
- Runtime gate needed:
- Live config gate needed:
- Checks or commands run:
- Blockers:
- Next safe command:
""",
}
