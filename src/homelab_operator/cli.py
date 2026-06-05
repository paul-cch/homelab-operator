"""Command-line interface for Homelab Operator."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .contracts import ExitState, evaluate_pr_body, evaluate_receipt, evaluate_surface_claim, receipt_template
from .scaffold import INIT_FILES


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
