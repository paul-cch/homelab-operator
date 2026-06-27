# Adoption Demo

This is a synthetic walkthrough for a tiny agent-maintained operations repo. It
does not describe a real host, network, runtime, or service.

The demo shows the mistake Homelab Operator is built to catch: an agent validates
source files and then implies deployment proof.

## Flow

1. A bad PR body validates local source but omits the claim boundary.
2. A good PR body uses `repo_only` and states that host, runtime, live config,
   and external-service proof were not checked.
3. A receipt records the next safe handoff.
4. The project doctor checks the public examples.

## Commands

Run from the repository root:

```bash
homelab-operator check-pr --body-file tests/fixtures/bad_pr_body_missing_boundary.md || true
homelab-operator check-pr --body-file tests/fixtures/good_pr_body.md
homelab-operator receipt-template --state MERGE_READY
homelab-operator check-receipt --file examples/minimal-homelab/receipts/source-change.md
homelab-operator check-claim --json-file examples/assistant-runtime/surface-claim.json
homelab-operator check-estate --file examples/minimal-homelab/estate.yaml
homelab-operator doctor --root .
```

## Expected signal

The bad PR should fail because validation without a claim boundary is not
reviewable. The good path should end with:

```text
HOMELAB_OPERATOR_DOCTOR_OK
```

## Demo repo shape

A fuller demo repository can copy this structure:

```text
homelab-operator-demo-app/
  README.md
  AGENTS.md
  .github/
    pull_request_template.md
    workflows/
      homelab-operator-contract.yml
  estate.yaml
  app/
    service.py
    config.example.yaml
  examples/
    pr-bodies/
      01-bad-missing-boundary.md
      02-bad-overclaims-runtime.md
      03-good-repo-only.md
      04-good-handoff.md
    receipts/
      merge-ready.md
      host-runtime-handoff.md
      blocked-with-evidence.md
      clean-no-op.md
```

Keep every host, service, config value, and receipt synthetic.
