# Repo Map

Generated: 2026-06-07
Root: .
Branch: codex/validator-schema-privacy-map

## Entry Points
- `homelab-operator` console script -> `homelab_operator.cli:main`.
- CLI subcommands: `check-pr`, `receipt-template`, `check-receipt`, `check-claim`, `check-estate`, `check-privacy`, `doctor`, `init`.
- `.github/workflows/ci.yml` installs the package, runs pytest, exercises contract checks, and runs `homelab-operator doctor --root .`.
- `templates/github/pull_request_template.md`, `templates/github/workflows/homelab-operator-contract.yml`, and `templates/receipts/lane-receipt.md` are installed by `homelab-operator init`.
- `README.md` provides the quickstart, proof ladder, command overview, and public-safety boundary.

## Validation
- Canonical repo gate: `python -m pip install -e ".[dev]"`, `python -m pytest`, `homelab-operator doctor --root .`.
- Local validation on this checkout used `.venv/bin/python` because bare `python` is not available on PATH.
- Additional ship checks: `ruff check .`, individual contract commands, `python -m build`, and `twine check dist/*`.
- `homelab-operator check-privacy --root .` is included inside `doctor`.

## Key Paths
- `src/homelab_operator/` - Python package for CLI wiring, side-effect-free contract checks, and scaffold templates.
- `schemas/` - JSON Schemas for PR contracts, lane receipts, surface claims, and example estates.
- `docs/concepts/` - proof ladder, claim boundaries, and privacy model.
- `docs/workflows/` - source-change, deploy-handoff, watcher-automation, and blocked-with-evidence workflows.
- `templates/` - PR, GitHub Actions, and lane-receipt templates copied into target repositories.
- `examples/` - synthetic example estate, source-change receipt, and assistant-runtime surface claim.
- `tests/` - pytest suite and fixtures for good/bad PR bodies, receipts, claims, estate checks, privacy scan, init, and doctor.
- `.github/` - repository PR template and CI workflow.

## Symbols / Modules
- `homelab_operator.cli`
  - `main(argv)`, `build_parser()`, and command handlers for each CLI subcommand.
  - `iter_text_files(root)` and `cmd_check_privacy(args)` walk text files while skipping cache/build directories.
  - `cmd_doctor(args)` runs fixture-backed PR, receipt, claim, estate, and privacy checks.
- `homelab_operator.contracts`
  - Enums: `ExitState`, `ProofKind`, `SurfaceKind`.
  - Results: `ContractResult`, `ReceiptResult`, `EstateResult`.
  - PR helpers: `parse_sections`, `find_section`, `owned_path_lines`, `body_has_placeholders`, `evaluate_pr_body`.
  - Receipt helpers: `receipt_template`, `receipt_fields`, `evaluate_receipt`.
  - Surface and estate checks: `evaluate_surface_claim`, `evaluate_estate`.
  - Privacy check: `scan_privacy`.
- `homelab_operator.scaffold`
  - `INIT_FILES` maps install targets to the synthetic/public-safe templates written by `homelab-operator init`.
- `tests.test_contracts`
  - Exercises PR bodies, receipt fields, schema/runtime enum parity, surface claims, estate flow references, scaffold init, and doctor.
- `tests.test_privacy_scan`
  - Exercises private-address detection, documentation-address acceptance, credential assignment detection, private-key block detection, and safe policy prose.

## Notes
- This is a public OSS repository; keep examples synthetic and do not add private hostnames, IPs, domains, logs, runtime state, live config, secrets, or personal operating history.
- Source and docs changes should use `repo_only` proof unless a separate public example proves a deeper surface.
- Root is recorded as `.` so this persistent artifact remains portable and public-safe.
- Symbol inventory was captured with `rg`; the local `ast-grep scan --pattern ...` sample command was not compatible with the installed `ast-grep` CLI.
