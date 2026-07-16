# Source-Only PR Reviewer Checklist

Use this checklist when reviewing a pull request that claims `repo_only` proof.
A source-only PR should prove only that local source, docs, schema, or test
changes are coherent. It should not imply host checkout, runtime export, live
config, deployment, or external service verification.

## Before Approving

### Claim Boundary

- [ ] PR body includes a `## Claim Boundary` section.
- [ ] Proof kind is `repo_only`.
- [ ] PR body states what was **not** proven (host, runtime, live config, external
      service).
- [ ] PR body does not use runtime or live-service language ("deployed",
      "running", "live", "production", "environment verified") without explicitly
      scoping it to a different surface.

### Owned Paths

- [ ] PR body lists at least one owned path under `## Owned Paths`.
- [ ] Owned paths match the files actually changed in the diff.
- [ ] No paths outside `docs/`, `examples/`, `src/`, `tests/`, `schemas/`, or
      `templates/` unless the PR explains why.

### Validation

- [ ] PR body includes a `## Validation` section with at least one command and
      its result.
- [ ] `homelab-operator check-pr --body-file <pr-body>` passes (`PR_CONTRACT_OK`).
- [ ] `homelab-operator doctor --root .` passes (`HOMELAB_OPERATOR_DOCTOR_OK`).
- [ ] `homelab-operator check-privacy --root .` passes (`PRIVACY_SCAN_OK`).
- [ ] `python -m pytest` passes (all tests green).

### Privacy

- [ ] No private hostnames, IP addresses, domains, or network ranges.
- [ ] No real VM, container, service, cluster, or estate inventories.
- [ ] No secrets, tokens, credentials, cookies, or `.env` content.
- [ ] No runtime logs, deploy markers, backups, or operational screenshots.
- [ ] All synthetic names use: `source`, `host`, `runtime`, `live-config`,
      `external-service`, or similarly generic labels.

### Demo and Fixture Content

- [ ] Any new example under `examples/` uses only synthetic data.
- [ ] Any new fixture under `tests/fixtures/` uses only synthetic data.
- [ ] Screenshots or terminal transcript snippets (if any) are fully synthetic
      and labelled as such.

## Common Reasons to Request Changes

- PR body uses `repo_only` but the diff touches live config, secrets, or
  runtime state.
- Owned paths in the PR body do not match the actual diff.
- Validation section lists commands but does not show whether they passed.
- `homelab-operator check-pr` fails on the PR body itself.
- Privacy scan finds private material in newly added files.
- Demo transcript contains real hostnames, addresses, or operational output.

## What a Source-Only PR Does Not Need

- Host checkout evidence.
- Runtime export or inspection output.
- Live config redaction proof.
- Deployment or release confirmation.
- External service health checks.

If the PR description implies any of the above, ask the contributor to either
remove the claim or change the proof kind to `handoff` and name the surface
that still needs verification.
