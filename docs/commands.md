# Command Reference

Most validation commands accept `--json` for machine-readable output. JSON mode
prints one object to stdout with `ok`, `errors`, and `warnings`; command-specific
fields are included when the checker exposes them.

## `check-pr`

Validate a Markdown pull request body.

```bash
homelab-operator check-pr --body-file PR.md
homelab-operator check-pr --body-file PR.md --json
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
```

JSON includes parsed receipt `fields`.

## `check-claim`

Validate a JSON surface claim.

```bash
homelab-operator check-claim --json-file surface-claim.json
homelab-operator check-claim --json-file surface-claim.json --json
```

## `check-estate`

Validate the simple YAML subset used by Homelab Operator example estates.

```bash
homelab-operator check-estate --file examples/minimal-homelab/estate.yaml
homelab-operator check-estate --file examples/minimal-homelab/estate.yaml --json
```

JSON includes estate `surfaces`.

## `check-privacy`

Scan text files for private operational material such as private IP addresses,
credential assignments, and private key blocks.

```bash
homelab-operator check-privacy --root .
homelab-operator check-privacy --root . --json
```

JSON includes `files_scanned`.

## `doctor`

Run the built-in project contract checks.

```bash
homelab-operator doctor --root .
homelab-operator doctor --root . --json
```

JSON includes nested `checks` for the built-in contract and privacy scans.

## `init`

Install Homelab Operator templates into another repository.

```bash
homelab-operator init --target /path/to/repo
```
