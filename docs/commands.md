# Command Reference

Most validation commands accept `--json` for machine-readable output. JSON mode
prints one object to stdout with `ok`, `errors`, and `warnings`; command-specific
fields are included when the checker exposes them.

Validation commands also accept `--github-annotations` for CI. When a command
fails, the flag emits GitHub Actions `::error ...::...` lines with a file, line,
stable rule title, and concise message while preserving the normal exit code.

## `check-pr`

Validate a Markdown pull request body.

```bash
homelab-operator check-pr --body-file PR.md
homelab-operator check-pr --body-file PR.md --json
homelab-operator check-pr --body-file PR.md --github-annotations
```

JSON includes `owned_paths`.

## `receipt-template`

Print a lane receipt template for an exit state.

```bash
homelab-operator receipt-template --state MERGE_READY
```

## `check-receipt`

Validate a Markdown lane receipt.

```bash
homelab-operator check-receipt --file receipt.md
homelab-operator check-receipt --file receipt.md --json
homelab-operator check-receipt --file receipt.md --github-annotations
```

JSON includes parsed receipt `fields`.

## `check-claim`

Validate a JSON surface claim.

```bash
homelab-operator check-claim --json-file surface-claim.json
homelab-operator check-claim --json-file surface-claim.json --json
homelab-operator check-claim --json-file surface-claim.json --github-annotations
```

## `check-estate`

Validate the simple YAML subset used by Homelab Operator example estates.

```bash
homelab-operator check-estate --file examples/minimal-homelab/estate.yaml
homelab-operator check-estate --file examples/minimal-homelab/estate.yaml --json
homelab-operator check-estate --file examples/minimal-homelab/estate.yaml --github-annotations
```

JSON includes estate `surfaces`.

## `check-privacy`

Scan text files for private operational material such as private IP addresses,
credential assignments, and private key blocks.

```bash
homelab-operator check-privacy --root .
homelab-operator check-privacy --root . --json
homelab-operator check-privacy --root . --github-annotations
homelab-operator check-privacy --root . --privacy-config privacy-rules.toml
```

By default, `check-privacy` loads `.homelab-operator-privacy.toml` from
`--root` when that file exists. Use `--privacy-config` to point at another TOML
file. Built-in high-risk checks always run, even when extra rules are loaded.

Additional deny rules use this synthetic shape:

```toml
[privacy]

[[privacy.deny_patterns]]
id = "synthetic.project-code"
description = "Synthetic project marker"
pattern = 'SYNTHETIC-PROJECT'
```

`id` must be a short lowercase identifier containing letters, digits, `.`, `_`,
or `-`. `description` is shown in failures. `pattern` is a literal substring,
not a regular expression. Match output reports rule ids and descriptions, not
captured values. GitHub annotations use the same non-leaking messages.
Malformed config fails before scanning and does not echo the configured pattern.
The config file itself is scanned with built-in rules only, so literal custom
patterns do not fail just because they appear in their own rule definition.

JSON includes `files_scanned`, `privacy_config`, and `custom_privacy_rules`.

## `doctor`

Run the built-in project contract checks.

```bash
homelab-operator doctor --root .
homelab-operator doctor --root . --json
homelab-operator doctor --root . --github-annotations
homelab-operator doctor --root . --privacy-config privacy-rules.toml
```

JSON includes nested `checks` for the built-in contract and privacy scans.

## `init`

Install Homelab Operator templates into another repository.

```bash
homelab-operator init --target /path/to/repo
```
