from __future__ import annotations

import json
from pathlib import Path

from homelab_operator.cli import main


FIXTURES = Path(__file__).parent / "fixtures"


def run_json(capsys, args: list[str]) -> tuple[int, dict[str, object]]:
    code = main(args)
    captured = capsys.readouterr()

    assert captured.err == ""
    return code, json.loads(captured.out)


def test_check_pr_json_includes_owned_paths(capsys) -> None:
    code, payload = run_json(capsys, ["check-pr", "--body-file", str(FIXTURES / "good_pr_body.md"), "--json"])

    assert code == 0
    assert payload["ok"] is True
    assert payload["errors"] == []
    assert payload["warnings"] == []
    assert "src/homelab_operator/contracts.py" in payload["owned_paths"]


def test_check_pr_text_output_is_unchanged_by_default(capsys) -> None:
    code = main(["check-pr", "--body-file", str(FIXTURES / "good_pr_body.md")])
    captured = capsys.readouterr()

    assert code == 0
    assert captured.out == "PR_CONTRACT_OK\n"
    assert captured.err == ""


def test_check_receipt_json_includes_fields(capsys) -> None:
    code, payload = run_json(capsys, ["check-receipt", "--file", str(FIXTURES / "good_receipt.md"), "--json"])

    assert code == 0
    assert payload["ok"] is True
    assert payload["fields"]["Proof kind"] == "repo_only"
    assert payload["fields"]["Exit state"] == "MERGE_READY"


def test_check_claim_json_reports_errors_without_stderr(tmp_path: Path, capsys) -> None:
    claim = tmp_path / "surface-claim.json"
    claim.write_text(
        json.dumps(
            {
                "surface": "runtime",
                "proof_kind": "runtime_export_only",
                "claim_proven": "synthetic runtime export checked",
                "claim_not_proven": "no live service checked",
            }
        ),
        encoding="utf-8",
    )

    code, payload = run_json(capsys, ["check-claim", "--json-file", str(claim), "--json"])

    assert code == 1
    assert payload["ok"] is False
    assert payload["warnings"] == []
    assert payload["errors"] == ["Surface claim has unknown surface"]


def test_check_estate_json_includes_surfaces(capsys) -> None:
    code, payload = run_json(
        capsys,
        ["check-estate", "--file", "examples/minimal-homelab/estate.yaml", "--json"],
    )

    assert code == 0
    assert payload["ok"] is True
    assert set(payload["surfaces"]) == {"source", "host", "runtime", "live-config"}


def test_check_privacy_json_reports_failures_without_stderr(tmp_path: Path, capsys) -> None:
    sample = tmp_path / "sample.txt"
    field_name = "api" + "_key"
    sample.write_text(f"{field_name}: synthetic-placeholder\n", encoding="utf-8")

    code, payload = run_json(capsys, ["check-privacy", "--root", str(tmp_path), "--json"])

    assert code == 1
    assert payload["ok"] is False
    assert payload["warnings"] == []
    assert payload["files_scanned"] == 1
    assert any("Privacy scan matched" in error for error in payload["errors"])


def test_doctor_json_includes_nested_checks(capsys) -> None:
    code, payload = run_json(capsys, ["doctor", "--root", ".", "--json"])

    assert code == 0
    assert payload["ok"] is True
    assert payload["errors"] == []
    assert payload["warnings"] == []

    checks = {check["name"]: check for check in payload["checks"]}
    assert set(checks) == {"PR", "receipt", "claim", "estate", "privacy"}
    assert "src/homelab_operator/contracts.py" in checks["PR"]["owned_paths"]
    assert checks["receipt"]["fields"]["Proof kind"] == "repo_only"
    assert set(checks["estate"]["surfaces"]) == {"source", "host", "runtime", "live-config"}
    assert checks["privacy"]["files_scanned"] > 0
