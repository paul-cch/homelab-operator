# Make a Safe First PR

This path is for contributors who want a small, reviewable first pull request.
It keeps the work public, synthetic, and easy to validate.

## 1. Pick a Good First Issue

Choose an issue labelled `good first issue`. Prefer issues that already list
the expected files to touch, acceptance criteria, and validation commands.

Good first issues in this repo are usually one of these shapes:

| Issue shape | Expected files to touch |
| --- | --- |
| Docs polish | `docs/**`, `CONTRIBUTING.md`, or synthetic examples under `examples/**` |
| CLI help or docs sync | `src/homelab_operator/cli.py`, `docs/commands.md`, and focused tests |
| Validator behavior | `src/homelab_operator/contracts.py`, `schemas/**`, and focused tests |
| GitHub workflow examples | `templates/github/**`, `.github/**`, and docs for the example |
| Demo fixture cleanup | `examples/**`, `tests/fixtures/**`, and docs that reference them |

Avoid issues that require private infrastructure, live services, deployment
access, host runtime inspection, package publishing, secret handling, or account
permissions for a first PR.

## 2. Claim the Issue Lightly

Leave a short comment before starting:

```text
I would like to work on this. I expect to touch `docs/commands.md` and tests,
and I will keep the proof boundary at `repo_only`.
```

Claiming an issue is a coordination signal, not permanent ownership. If work
goes quiet, maintainers may invite someone else to pick it up. If the scope
starts needing host, runtime, live-config, publishing, or external-service proof,
pause and ask a maintainer before continuing.

## 3. Keep the Change Small

A strong first PR usually does one thing:

- adds one missing example
- tightens one doc path
- adds one focused test case
- documents one command or workflow
- fixes one validation message or schema mismatch

Do not bundle unrelated cleanup. If you discover a second problem, mention it in
the PR or open a follow-up issue.

## 4. Respect the Privacy Boundary

This is a public OSS repository. Do not add:

- private hostnames, IP addresses, network ranges, or domains
- real VM, container, service, cluster, or estate inventories
- secrets, token names, cookies, authorization headers, or `.env` content
- runtime logs, deploy markers, backups, screenshots, or generated private
  reports
- personal schedules, messages, academic material, or assistant memory payloads

Use synthetic names such as `source`, `host`, `runtime`, `live-config`, and
`external-service`. A first PR should normally prove only repository-local
behavior.

## 5. Run Validation

Install the development dependencies once:

```bash
python -m pip install -e ".[dev]"
```

For code, schema, or example changes, run:

```bash
python -m pytest
homelab-operator doctor --root .
```

For docs-only changes, run:

```bash
homelab-operator check-privacy --root .
git diff --check
```

If you cannot run a command, say which command was skipped and why.

## 6. Open the PR With a Claim Boundary

Use the pull request template. The important sections for a first PR are:

- `Owned Paths`: list the files or folders you intentionally changed
- `Validation`: paste the commands you ran and whether they passed
- `Claim Boundary`: state what your checks prove and what they do not prove

Most first PRs should use:

```text
Proof kind: repo_only
Claim proven: the changed source, docs, examples, or tests passed the listed local checks.
Claim not proven: no host checkout, runtime export, live config, deployment, package publish, or external service was checked.
Host/runtime/live-config handoff needed: no
```

Use `handoff` instead of `repo_only` only when the source change is ready but a
maintainer must verify another surface before the work can land.
