# Start Here For Agents

Homelab Operator helps an AI coding agent say exactly what it proved before a
human reviews or ships infrastructure work.

Use it when an agent changes source, templates, runbooks, GitHub workflows, or
deployment handoff docs and the PR needs to separate repo proof from host,
runtime, live config, or external-service proof.

## Install

Install the published CLI with `pipx` when it is available from PyPI:

```bash
pipx install homelab-operator
```

Today, install directly from GitHub:

```bash
pipx install git+https://github.com/paul-cch/homelab-operator.git
```

Then add the templates to a repository:

```bash
homelab-operator init --target /path/to/repo
```

## First PR checklist

Before opening or updating a PR, make sure the body names:

- summary
- linked issue
- owned paths
- validation commands and results
- claim boundary
- what was not proven
- next safe handoff

Then validate it:

```bash
homelab-operator check-pr --body-file PR.md
```

## Choose the right proof kind

Use `repo_only` when local files, tests, schemas, and docs were checked but no
host, runtime, live config, or external service was verified.

Use a handoff receipt when the source is ready but another actor still needs to
check a host checkout, runtime export, live config, or external service.

Use a blocked receipt when work cannot safely continue and the blocker is named
with evidence.

## Privacy rule

Keep examples synthetic. Do not put private hostnames, IP addresses, domains,
logs, runtime state, live config, secrets, or personal operating history in
public docs, PR bodies, or receipts.

## Next docs

- [Prompt recipes](prompt-recipes.md)
- [Proof ladder](../concepts/proof-ladder.md)
- [Claim boundaries](../concepts/claim-boundaries.md)
- [Source change workflow](../workflows/source-change.md)
- [Deploy handoff workflow](../workflows/deploy-handoff.md)
