"""Command-line interface for Homelab Operator."""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import sys
from pathlib import Path
from typing import Any

from .contracts import (
    ExitState,
    PrivacyConfigError,
    evaluate_estate,
    evaluate_pr_body,
    evaluate_receipt,
    evaluate_surface_claim,
    load_privacy_config,
    receipt_template,
    scan_privacy,
)
from .scaffold import INIT_FILES


SKIP_DIRS = {".git", ".venv", ".pytest_cache", ".ruff_cache", "build", "dist", "__pycache__"}
DEFAULT_PRIVACY_CONFIG = ".homelab-operator-privacy.toml"


def read_text(path: str | None) -> str:
    if path:
        return Path(path).read_text(encoding="utf-8")
    return sys.stdin.read()


def result_payload(result: Any, fields: tuple[str, ...] = ()) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "ok": result.ok,
        "errors": list(result.errors),
        "warnings": list(result.warnings),
    }
    for field in fields:
        value = getattr(result, field)
        if isinstance(value, tuple):
            payload[field] = list(value)
        elif isinstance(value, dict):
            payload[field] = dict(value)
        else:
            payload[field] = value
    return payload


def print_json(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, sort_keys=True))


def emit_result(args: argparse.Namespace, result: Any, ok_message: str, fields: tuple[str, ...] = ()) -> int:
    if args.json:
        print_json(result_payload(result, fields))
        return 0 if result.ok else 1

    for warning in result.warnings:
        print(f"WARNING {warning}", file=sys.stderr)
    if result.ok:
        print(ok_message)
        return 0
    for error in result.errors:
        print(f"ERROR {error}", file=sys.stderr)
    return 1


def cmd_check_pr(args: argparse.Namespace) -> int:
    result = evaluate_pr_body(read_text(args.body_file))
    if result.ok:
        if args.write_owned_paths and result.owned_paths:
            Path(args.write_owned_paths).write_text("\n".join(result.owned_paths) + "\n", encoding="utf-8")
    return emit_result(args, result, "PR_CONTRACT_OK", ("owned_paths",))


def cmd_receipt_template(args: argparse.Namespace) -> int:
    print(receipt_template(args.state), end="")
    return 0


def cmd_check_receipt(args: argparse.Namespace) -> int:
    result = evaluate_receipt(read_text(args.file))
    return emit_result(args, result, "RECEIPT_CONTRACT_OK", ("fields",))


def cmd_check_claim(args: argparse.Namespace) -> int:
    result = evaluate_surface_claim(read_text(args.json_file))
    return emit_result(args, result, "SURFACE_CLAIM_OK")


def cmd_check_estate(args: argparse.Namespace) -> int:
    result = evaluate_estate(read_text(args.file))
    return emit_result(args, result, "ESTATE_CONTRACT_OK", ("surfaces",))


def iter_text_files(root: Path) -> list[Path]:
    paths: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        paths.append(path)
    return sorted(paths)


def privacy_config_path(root: Path, config_file: str | None) -> Path | None:
    if config_file:
        path = Path(config_file)
        return path if path.is_absolute() else root / path
    default_path = root / DEFAULT_PRIVACY_CONFIG
    return default_path if default_path.exists() else None


def privacy_payload(root: Path, config_file: str | None = None) -> dict[str, Any]:
    errors: list[str] = []
    files_scanned = 0
    config_path = privacy_config_path(root, config_file)
    resolved_config_path = config_path.resolve() if config_path else None
    try:
        extra_rules = load_privacy_config(config_path) if config_path else ()
    except PrivacyConfigError as exc:
        return {
            "ok": False,
            "errors": [str(exc)],
            "warnings": [],
            "files_scanned": 0,
            "privacy_config": str(config_path),
            "custom_privacy_rules": 0,
        }

    for path in iter_text_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        files_scanned += 1
        rules = () if resolved_config_path and path.resolve() == resolved_config_path else extra_rules
        result = scan_privacy(text, rules)
        errors.extend(f"{path}: {error}" for error in result.errors)
    return {
        "ok": not errors,
        "errors": errors,
        "warnings": [],
        "files_scanned": files_scanned,
        "privacy_config": str(config_path) if config_path else None,
        "custom_privacy_rules": len(extra_rules),
    }


def cmd_check_privacy(args: argparse.Namespace) -> int:
    payload = privacy_payload(Path(args.root), args.privacy_config)
    if args.json:
        print_json(payload)
        return 0 if payload["ok"] else 1
    if not payload["ok"]:
        for error in payload["errors"]:
            print(f"ERROR {error}", file=sys.stderr)
        return 1
    print("PRIVACY_SCAN_OK")
    return 0


def doctor_payload(root: Path, config_file: str | None = None) -> dict[str, Any]:
    checks = [
        ("PR", root / "tests/fixtures/good_pr_body.md", evaluate_pr_body, "PR_CONTRACT_OK", ("owned_paths",)),
        ("receipt", root / "tests/fixtures/good_receipt.md", evaluate_receipt, "RECEIPT_CONTRACT_OK", ("fields",)),
        ("claim", root / "tests/fixtures/surface_claim.json", evaluate_surface_claim, "SURFACE_CLAIM_OK", ()),
        ("estate", root / "examples/minimal-homelab/estate.yaml", evaluate_estate, "ESTATE_CONTRACT_OK", ("surfaces",)),
    ]
    errors: list[str] = []
    warnings: list[str] = []
    check_payloads: list[dict[str, Any]] = []
    for label, path, evaluator, ok_message, fields in checks:
        if not path.exists():
            check_payload = {
                "name": label,
                "path": str(path),
                "ok": False,
                "errors": [f"{label} fixture missing: {path}"],
                "warnings": [],
                "ok_message": ok_message,
            }
            errors.extend(check_payload["errors"])
            check_payloads.append(check_payload)
            continue
        result = evaluator(path.read_text(encoding="utf-8"))
        check_payload = result_payload(result, fields)
        check_payload.update({"name": label, "path": str(path), "ok_message": ok_message})
        errors.extend(f"{path}: {error}" for error in result.errors)
        warnings.extend(f"{path}: {warning}" for warning in result.warnings)
        check_payloads.append(check_payload)

    privacy_check = privacy_payload(root, config_file)
    privacy_check.update({"name": "privacy", "ok_message": "PRIVACY_SCAN_OK"})
    check_payloads.append(privacy_check)
    errors.extend(str(error) for error in privacy_check["errors"])
    warnings.extend(str(warning) for warning in privacy_check["warnings"])

    return {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "checks": check_payloads,
    }


def cmd_doctor(args: argparse.Namespace) -> int:
    root = Path(args.root)
    payload = doctor_payload(root, args.privacy_config)
    if args.json:
        print_json(payload)
        return 0 if payload["ok"] else 1

    errors: list[str] = []
    for check in payload["checks"]:
        if check["ok"]:
            print(check["ok_message"])
        elif check["name"] == "privacy":
            for error in check["errors"]:
                print(f"ERROR {error}", file=sys.stderr)
            errors.append("privacy scan failed")
        else:
            path = check.get("path")
            if path and Path(str(path)).exists():
                errors.extend(f"{path}: {error}" for error in check["errors"])
            else:
                errors.extend(str(error) for error in check["errors"])

    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        return 1
    print("HOMELAB_OPERATOR_DOCTOR_OK")
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    target = Path(args.target)
    written: list[str] = []
    skipped: list[str] = []
    for relative, content in INIT_FILES.items():
        path = target / relative
        if path.exists() and not args.force:
            skipped.append(relative)
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        written.append(relative)
    for relative in written:
        print(f"WROTE {relative}")
    for relative in skipped:
        print(f"SKIPPED {relative}", file=sys.stderr)
    if skipped and not args.force:
        print("INIT_PARTIAL existing files skipped; rerun with --force to overwrite")
    else:
        print("INIT_OK")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="homelab-operator")
    parser.add_argument("--version", action="version", version=importlib.metadata.version("homelab-operator"))
    subparsers = parser.add_subparsers(dest="command", required=True)

    check_pr = subparsers.add_parser("check-pr", help="Validate an agent-authored PR body")
    check_pr.add_argument("--body-file", help="Markdown PR body. Defaults to stdin.")
    check_pr.add_argument("--write-owned-paths", help="Write extracted owned paths to a file.")
    check_pr.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    check_pr.set_defaults(func=cmd_check_pr)

    receipt = subparsers.add_parser("receipt-template", help="Print a lane receipt template")
    receipt.add_argument("--state", choices=[state.value for state in ExitState], default=ExitState.MERGE_READY.value)
    receipt.set_defaults(func=cmd_receipt_template)

    check_receipt = subparsers.add_parser("check-receipt", help="Validate a lane receipt")
    check_receipt.add_argument("--file", required=True, help="Markdown receipt file.")
    check_receipt.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    check_receipt.set_defaults(func=cmd_check_receipt)

    check_claim = subparsers.add_parser("check-claim", help="Validate a JSON surface claim")
    check_claim.add_argument("--json-file", required=True, help="JSON surface claim file.")
    check_claim.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    check_claim.set_defaults(func=cmd_check_claim)

    check_estate = subparsers.add_parser("check-estate", help="Validate a simple estate YAML file")
    check_estate.add_argument("--file", required=True, help="Estate YAML file.")
    check_estate.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    check_estate.set_defaults(func=cmd_check_estate)

    check_privacy = subparsers.add_parser("check-privacy", help="Scan text files for private operational material")
    check_privacy.add_argument("--root", default=".", help="Repository root to scan.")
    check_privacy.add_argument(
        "--privacy-config",
        help=f"Additional TOML privacy deny rules. Defaults to {DEFAULT_PRIVACY_CONFIG} under --root when present.",
    )
    check_privacy.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    check_privacy.set_defaults(func=cmd_check_privacy)

    doctor = subparsers.add_parser("doctor", help="Run the built-in project contract checks")
    doctor.add_argument("--root", default=".", help="Repository root to check.")
    doctor.add_argument(
        "--privacy-config",
        help=f"Additional TOML privacy deny rules. Defaults to {DEFAULT_PRIVACY_CONFIG} under --root when present.",
    )
    doctor.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    doctor.set_defaults(func=cmd_doctor)

    init = subparsers.add_parser("init", help="Install Homelab Operator templates into a repo")
    init.add_argument("--target", default=".", help="Target repository root.")
    init.add_argument("--force", action="store_true", help="Overwrite existing files.")
    init.set_defaults(func=cmd_init)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
