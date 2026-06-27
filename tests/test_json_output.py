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


def test_check_pr_github_annotations_point_to_validation_section(tmp_path: Path, capsys) -> None:
    body = tmp_path / "pr-body.md"
    body.write_text(
        """## Summary

Add a synthetic source-only check.

## Linked Issues

Refs #2

## Owned Paths

- `src/homelab_operator/cli.py`

## Validation

Not supplied.

## Claim Boundary

Proof kind: repo_only
""",
        encoding="utf-8",
    )

    code = main(["check-pr", "--body-file", str(body), "--github-annotations"])
    captured = capsys.readouterr()

    assert code == 1
    assert captured.out == ""
    assert f"file={body}" in captured.err
    assert "line=13" in captured.err
    assert "title=homelab-operator/pr.validation-section-must-include" in captured.err
    assert "Validation section must include commands/results or an explicit blocker" in captured.err


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
    assert payload["privacy_config"] is None
    assert payload["custom_privacy_rules"] == 0
    assert any("Privacy scan matched" in error for error in payload["errors"])


def test_check_privacy_github_annotations_include_line_and_rule_without_leaking_match(
    tmp_path: Path, capsys
) -> None:
    sample = tmp_path / "sample.txt"
    field_name = "api" + "_key"
    sample.write_text(f"safe line\n{field_name}: synthetic-placeholder\n", encoding="utf-8")

    code = main(["check-privacy", "--root", str(tmp_path), "--github-annotations"])
    captured = capsys.readouterr()

    assert code == 1
    assert captured.out == ""
    assert f"file={sample}" in captured.err
    assert "line=2" in captured.err
    assert "title=homelab-operator/builtin.credential-assignment" in captured.err
    assert "Privacy scan matched rule `builtin.credential-assignment`: Credential-like assignment" in captured.err
    assert "synthetic-placeholder" not in captured.err


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


def test_check_privacy_json_loads_default_config_without_leaking_match(tmp_path: Path, capsys) -> None:
    config = tmp_path / ".homelab-operator-privacy.toml"
    sample = tmp_path / "sample.txt"
    config.write_text(
        """[privacy]
[[privacy.deny_patterns]]
id = "synthetic.project-code"
description = "Synthetic project marker"
pattern = 'SYNTHETIC-PROJECT'
""",
        encoding="utf-8",
    )
    sample.write_text("public sample uses SYNTHETIC-PROJECT\n", encoding="utf-8")

    code, payload = run_json(capsys, ["check-privacy", "--root", str(tmp_path), "--json"])

    assert code == 1
    assert payload["ok"] is False
    assert payload["privacy_config"] == str(config)
    assert payload["custom_privacy_rules"] == 1
    assert payload["files_scanned"] == 2
    assert payload["errors"] == [
        f"{sample}: Privacy scan matched rule `synthetic.project-code`: Synthetic project marker"
    ]
    assert "SYNTHETIC-PROJECT" not in payload["errors"][0]


def test_check_privacy_json_does_not_self_match_config_patterns(tmp_path: Path, capsys) -> None:
    config = tmp_path / ".homelab-operator-privacy.toml"
    config.write_text(
        """[privacy]
[[privacy.deny_patterns]]
id = "synthetic.literal"
description = "Synthetic literal marker"
pattern = 'SECRET_PROJECT'
""",
        encoding="utf-8",
    )

    code, payload = run_json(capsys, ["check-privacy", "--root", str(tmp_path), "--json"])

    assert code == 0
    assert payload["ok"] is True
    assert payload["privacy_config"] == str(config)
    assert payload["custom_privacy_rules"] == 1
    assert payload["files_scanned"] == 1
    assert payload["errors"] == []


def test_check_privacy_json_reports_invalid_config_without_leaking_pattern(tmp_path: Path, capsys) -> None:
    config = tmp_path / "privacy.toml"
    pattern = "SECRET-SAMPLE-" * 24
    config.write_text(
        f"""[privacy]
[[privacy.deny_patterns]]
id = "synthetic.long"
description = "Synthetic long literal"
pattern = '{pattern}'
""",
        encoding="utf-8",
    )

    code, payload = run_json(
        capsys,
        ["check-privacy", "--root", str(tmp_path), "--privacy-config", "privacy.toml", "--json"],
    )

    assert code == 1
    assert payload["ok"] is False
    assert payload["files_scanned"] == 0
    assert payload["privacy_config"] == str(config)
    assert payload["custom_privacy_rules"] == 0
    assert payload["errors"] == ["Privacy config rule `synthetic.long` has `pattern` longer than 256 characters"]
    assert pattern not in payload["errors"][0]


def test_check_privacy_json_reports_non_utf8_config_without_traceback(tmp_path: Path, capsys) -> None:
    config = tmp_path / "privacy.toml"
    config.write_bytes(b"\xff\xfe\xfa")

    code, payload = run_json(
        capsys,
        ["check-privacy", "--root", str(tmp_path), "--privacy-config", "privacy.toml", "--json"],
    )

    assert code == 1
    assert payload["ok"] is False
    assert payload["files_scanned"] == 0
    assert payload["privacy_config"] == str(config)
    assert payload["custom_privacy_rules"] == 0
    assert payload["errors"] == ["Privacy config must be valid UTF-8 text"]
