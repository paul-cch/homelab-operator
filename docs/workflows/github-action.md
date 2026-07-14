# GitHub Action Workflow

Homelab Operator is usually adopted as a GitHub Actions workflow. The workflow
checks the real pull request body from `github.event.pull_request.body`, then
scans checked-out files for private operational material.

It complements CI fixture tests. Keep normal tests in CI so validator behavior
stays covered, and run this workflow as a separate PR gate so reviewers know
the submitted PR body carries the required contract.

## Install

Copy `templates/github/workflows/homelab-operator-contract.yml` into the target
repository as:

```text
.github/workflows/homelab-operator-contract.yml
```

The template installs Homelab Operator from the public `v1.0.0` tag. Update
`HOMELAB_OPERATOR_REF` deliberately when adopting a newer release.

## Copyable proof lanes

The [`examples/github-actions`](../../examples/github-actions/README.md)
directory has ready-to-copy workflows for:

- validating a checked-in lane receipt when receipt files change
- scanning repository text on pull requests and pushes to `main`
- running a scheduled or manual source-claim and privacy check

Each example uses only commands shipped in `v1.0.0`, requests read-only GitHub
permissions, and states its `repo_only` proof boundary in the workflow file.
Change the synthetic example path after copying a workflow into another
repository.

The scheduled example validates a checked-in source claim. It does not inspect
a host or runtime. A generic JSON Schema workflow remains deferred until the
schema-validation CLI command exists.

## Required PR Body

The Action expects the pull request body to keep these sections:

- `## Summary`
- `## Linked Issue` or `## Linked Issues`
- `## Owned Paths`
- `## Validation` or `## Verification`
- `## Claim Boundary`, `## Surface Classification`, or `## Host / Runtime Handoff`

Use `Refs #123` or `Part of #123` for partial work. Reserve closing keywords
such as `Closes #123` for work that actually finishes the issue.

## Gate Behavior

The workflow runs on `opened`, `edited`, `synchronize`, `reopened`, and
`ready_for_review` pull request events. An empty PR body fails because the
contract sections are missing.

The workflow uses read-only permissions and does not persist the GitHub token
in the checkout. It writes the PR body to `$RUNNER_TEMP/pr-body.md` through
JSON decoding so Markdown content is not interpreted by the shell.

When the installed Homelab Operator version supports annotation output, a
source-only PR gate can emit GitHub Actions annotations directly:

```yaml
- name: Validate PR body
  run: homelab-operator check-pr --body-file "$RUNNER_TEMP/pr-body.md" --github-annotations
- name: Scan checked-out files for private material
  run: homelab-operator check-privacy --root . --github-annotations
```

For systems that consume SARIF, emit a deterministic source-only result file
from the same synthetic checks:

```yaml
- name: Write PR contract SARIF
  run: homelab-operator check-pr --body-file "$RUNNER_TEMP/pr-body.md" --sarif > homelab-operator-pr.sarif
- name: Write privacy SARIF
  run: homelab-operator check-privacy --root . --sarif > homelab-operator-privacy.sarif
```

For branch protection, require the `Validate PR body and privacy` job alongside
the repository's normal CI job. Do not replace test, build, or lint gates with
this Action.

## Proof Boundary

Passing this Action proves only that the PR body is contract-shaped and that the
checked-out repository text did not match the built-in privacy patterns. It does
not prove host checkout state, runtime behavior, live config, external service
health, or deployment success.
