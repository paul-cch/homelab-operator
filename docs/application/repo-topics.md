# GitHub Description And Topics

Use this exact description and topic set for the public GitHub repository
metadata. Parent coordination should perform the actual GitHub metadata write.

## Recommended GitHub Description

Privacy-safe contract checker for AI-assisted infrastructure PRs: validate
claim boundaries, lane receipts, and repo-only proof.

## Recommended GitHub Topics

- `homelab`
- `infrastructure-as-code`
- `devops`
- `ai-agents`
- `agent-safety`
- `maintainer-tools`
- `python`
- `cli`
- `github-actions`
- `contract-checks`
- `claim-boundaries`
- `privacy`

Comma-separated copy target:

```text
homelab, infrastructure-as-code, devops, ai-agents, agent-safety, maintainer-tools, python, cli, github-actions, contract-checks, claim-boundaries, privacy
```

## Optional Topics

- `receipts`
- `repo-only`
- `automation-safety`
- `developer-tools`

## Positioning Notes

- Use `contract-checks`, `agent-safety`, and `privacy` to make the project
  discoverable outside homelab circles.
- Use `devops` and `infrastructure-as-code` for the broader maintainer audience,
  while keeping the description tied to PR contracts rather than deployment
  automation.
- Keep `homelab` because the examples and maintainer workflow are grounded in
  small infrastructure repositories.
- Avoid topics that imply live monitoring, deployment, secrets management,
  runtime observability, or production infrastructure proof. The public repo
  demonstrates source-side contracts and synthetic examples.
