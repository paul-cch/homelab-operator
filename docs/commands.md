# Command Reference

## `check-pr`

Validate a Markdown pull request body.

```bash
homelab-operator check-pr --body-file PR.md
```

## `receipt-template`

Print a lane receipt template for an exit state.

```bash
homelab-operator receipt-template --state MERGE_READY
```

## `check-receipt`

Validate a Markdown lane receipt.

```bash
homelab-operator check-receipt --file receipt.md
```

## `check-claim`

Validate a JSON surface claim.

```bash
homelab-operator check-claim --json-file surface-claim.json
```

## `check-estate`

Validate the simple YAML subset used by Homelab Operator example estates.

```bash
homelab-operator check-estate --file examples/minimal-homelab/estate.yaml
```

## `check-privacy`

Scan text files for private operational material such as private IP addresses,
credential assignments, and private key blocks.

```bash
homelab-operator check-privacy --root .
```

## `doctor`

Run the built-in project contract checks.

```bash
homelab-operator doctor --root .
```

## `init`

Install Homelab Operator templates into another repository.

```bash
homelab-operator init --target /path/to/repo
```
