"""Command-line interface for Homelab Operator."""

from __future__ import annotations

import argparse
import importlib.metadata
import sys
from pathlib import Path

from .contracts import (
    ExitState,
    evaluate_estate,
    evaluate_pr_body,
    evaluate_receipt,
    evaluate_surface_claim,
    receipt_template,
    scan_privacy,
)
from .scaffold import INIT_FILES


SKIP_DIRS = {".git", ".venv", ".pytest_cache", ".ruff_cache", "build", "dist", "__pycache__"}


def read_text(path: str | None) -> str:
    if path:
        return Path(path).read_text(encoding="utf-8")
    return sys.stdin.read()


def cmd_check_pr(args: argparse.Namespace) -> int:
    result = evaluate_pr_body(read_text(args.body_file))
    for warning in result.warnings:
        print(f"WARNING {warning}", file=sys.stderr)
    if result.ok:
        print("PR_CONTRACT_OK")
        if args.write_owned_paths and result.owned_paths:
            Path(args.write_owned_paths).write_text("\n".join(result.owned_paths) + "\n", encoding="utf-8")
        return 0
    for error in result.errors:
        print(f"ERROR {error}", file=sys.stderr)
    return 1


def cmd_receipt_template(args: argparse.Namespace) -> int:
    print(receipt_template(args.state), end="")
    return 0


def cmd_check_receipt(args: argparse.Namespace) -> int:
    result = evaluate_receipt(read_text(args.file))
    for warning in result.warnings:
        print(f"WARNING {warning}", file=sys.stderr)
    if result.ok:
        print("RECEIPT_CONTRACT_OK")
        return 0
    for error in result.errors:
        print(f"ERROR {error}", file=sys.stderr)
    return 1


def cmd_check_claim(args: argparse.Namespace) -> int:
    result = evaluate_surface_claim(read_text(args.json_file))
    if result.ok:
        print("SURFACE_CLAIM_OK")
        return 0
    for error in result.errors:
        print(f"ERROR {error}", file=sys.stderr)
    return 1


def cmd_check_estate(args: argparse.Namespace) -> int:
    result = evaluate_estate(read_text(args.file))
    for warning in result.warnings:
        print(f"WARNING {warning}", file=sys.stderr)
    if result.ok:
        print("ESTATE_CONTRACT_OK")
        return 0
    for error in result.errors:
        print(f"ERROR {error}", file=sys.stderr)
    return 1


def iter_text_files(root: Path) -> list[Path]:
    paths: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        paths.append(path)
    return sorted(paths)


def cmd_check_privacy(args: argparse.Namespace) -> int:
    root = Path(args.root)
    failures: list[str] = []
    for path in iter_text_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        result = scan_privacy(text)
        failures.extend(f"{path}: {error}" for error in result.errors)
    if failures:
        for failure in failures:
            print(f"ERROR {failure}", file=sys.stderr)
        return 1
    print("PRIVACY_SCAN_OK")
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    root = Path(args.root)
    checks = [
        ("PR", root / "tests/fixtures/good_pr_body.md", evaluate_pr_body, "PR_CONTRACT_OK"),
        ("receipt", root / "tests/fixtures/good_receipt.md", evaluate_receipt, "RECEIPT_CONTRACT_OK"),
        ("claim", root / "tests/fixtures/surface_claim.json", evaluate_surface_claim, "SURFACE_CLAIM_OK"),
        ("estate", root / "examples/minimal-homelab/estate.yaml", evaluate_estate, "ESTATE_CONTRACT_OK"),
    ]
    errors: list[str] = []
    for label, path, evaluator, ok_message in checks:
        if not path.exists():
            errors.append(f"{label} fixture missing: {path}")
            continue
        result = evaluator(path.read_text(encoding="utf-8"))
        if result.ok:
            print(ok_message)
        else:
            errors.extend(f"{path}: {error}" for error in result.errors)

    privacy_args = argparse.Namespace(root=str(root))
    privacy_code = cmd_check_privacy(privacy_args)
    if privacy_code:
        errors.append("privacy scan failed")

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
    check_pr.set_defaults(func=cmd_check_pr)

    receipt = subparsers.add_parser("receipt-template", help="Print a lane receipt template")
    receipt.add_argument("--state", choices=[state.value for state in ExitState], default=ExitState.MERGE_READY.value)
    receipt.set_defaults(func=cmd_receipt_template)

    check_receipt = subparsers.add_parser("check-receipt", help="Validate a lane receipt")
    check_receipt.add_argument("--file", required=True, help="Markdown receipt file.")
    check_receipt.set_defaults(func=cmd_check_receipt)

    check_claim = subparsers.add_parser("check-claim", help="Validate a JSON surface claim")
    check_claim.add_argument("--json-file", required=True, help="JSON surface claim file.")
    check_claim.set_defaults(func=cmd_check_claim)

    check_estate = subparsers.add_parser("check-estate", help="Validate a simple estate YAML file")
    check_estate.add_argument("--file", required=True, help="Estate YAML file.")
    check_estate.set_defaults(func=cmd_check_estate)

    check_privacy = subparsers.add_parser("check-privacy", help="Scan text files for private operational material")
    check_privacy.add_argument("--root", default=".", help="Repository root to scan.")
    check_privacy.set_defaults(func=cmd_check_privacy)

    doctor = subparsers.add_parser("doctor", help="Run the built-in project contract checks")
    doctor.add_argument("--root", default=".", help="Repository root to check.")
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
