# Privacy Model

Homelab Operator is designed for infrastructure repositories that may be
private, sensitive, or operationally revealing.

Public examples must be synthetic. Do not publish:

- hostnames, private domains, real IP addresses, or network ranges
- VM, container, cluster, or service inventories from a real estate
- secrets, token names, authorization headers, cookies, or `.env` content
- runtime logs, deployment markers, backups, or generated private reports
- personal schedules, messages, academic materials, or assistant memory payloads

Safe examples use names like `source`, `host`, `runtime`, `live-config`, and
`external-service`. They show the shape of the contract without revealing the
shape of a real system.

## Configurable Deny Patterns

Repositories can add synthetic, project-specific deny rules without editing
Python source. Put `.homelab-operator-privacy.toml` at the repository root, or
pass `--privacy-config` to `check-privacy` or `doctor`.

```toml
[privacy]

[[privacy.deny_patterns]]
id = "synthetic.project-code"
description = "Synthetic project marker"
pattern = 'SYNTHETIC-PROJECT'
```

Config rules only add checks. They cannot disable the built-in private address,
credential assignment, or private-key checks. Failure output names the matched
rule id and description, not the matched text, so secret-like values are not
printed back to the terminal. Configured patterns are literal substrings rather
than regular expressions, which keeps repository-loaded checks predictable in
local hooks and CI.

Keep public configs generic and synthetic. Do not publish real organization
policy names, internal project names, live service names, or private operating
details as examples.
