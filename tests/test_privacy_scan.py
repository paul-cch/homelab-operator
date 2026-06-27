from __future__ import annotations

import pytest

from homelab_operator.contracts import PrivacyConfigError, load_privacy_config, scan_privacy


def dotted(*octets: int) -> str:
    return ".".join(str(octet) for octet in octets)


@pytest.mark.parametrize(
    "address",
    [
        dotted(10, 0, 0, 42),
        dotted(127, 0, 0, 1),
        dotted(172, 16, 0, 8),
        dotted(172, 31, 255, 9),
        dotted(192, 168, 12, 34),
    ],
)
def test_privacy_scan_rejects_loopback_and_private_addresses(address: str) -> None:
    result = scan_privacy(f"synthetic endpoint address: {address}")

    assert not result.ok
    assert result.errors == ("Privacy scan matched rule `builtin.private-ipv4`: Private or loopback IPv4 address",)


@pytest.mark.parametrize(
    "address",
    [
        dotted(172, 15, 0, 8),
        dotted(172, 32, 0, 8),
        dotted(192, 0, 2, 10),
        dotted(198, 51, 100, 22),
        dotted(203, 0, 113, 44),
    ],
)
def test_privacy_scan_accepts_adjacent_and_documentation_addresses(address: str) -> None:
    result = scan_privacy(f"public documentation example address: {address}")

    assert result.ok


@pytest.mark.parametrize(
    ("name", "separator"),
    [
        ("api_key", " = "),
        ("access-token", ": "),
        ("password", "='"),
        ("authorization", ': "'),
    ],
)
def test_privacy_scan_rejects_credential_assignments(name: str, separator: str) -> None:
    assignment = f"{name}{separator}synthetic-placeholder"

    result = scan_privacy(assignment)

    assert not result.ok
    assert result.errors == ("Privacy scan matched rule `builtin.credential-assignment`: Credential-like assignment",)
    assert "synthetic-placeholder" not in result.errors[0]


@pytest.mark.parametrize(
    "key_prefix",
    [
        "",
        "RSA ",
        "OPENSSH ",
    ],
)
def test_privacy_scan_rejects_private_key_blocks(key_prefix: str) -> None:
    key_block = (
        f"-----BEGIN {key_prefix}PRIVATE KEY-----\n"
        "synthetic-placeholder\n"
        f"-----END {key_prefix}PRIVATE KEY-----"
    )

    result = scan_privacy(key_block)

    assert not result.ok
    assert result.errors == ("Privacy scan matched rule `builtin.private-key-block`: Private key block marker",)


def test_privacy_scan_accepts_safe_public_policy_text() -> None:
    text = f"""Public contribution policy:
- Use synthetic fixtures and documentation examples such as {dotted(203, 0, 113, 7)}.
- Mention that secrets, credentials, private topology, and raw logs must stay out of the repo.
- Keep proof labels source-only unless a public example validates a wider claim.
"""

    result = scan_privacy(text)

    assert result.ok


def test_privacy_config_loads_custom_rules(tmp_path) -> None:
    config = tmp_path / ".homelab-operator-privacy.toml"
    config.write_text(
        """[privacy]
[[privacy.deny_patterns]]
id = "synthetic.project-code"
description = "Synthetic project marker"
pattern = 'SYNTHETIC-PROJECT'
""",
        encoding="utf-8",
    )

    rules = load_privacy_config(config)
    result = scan_privacy("public sample uses SYNTHETIC-PROJECT", rules)

    assert len(rules) == 1
    assert not result.ok
    assert result.errors == ("Privacy scan matched rule `synthetic.project-code`: Synthetic project marker",)
    assert "SYNTHETIC-PROJECT" not in result.errors[0]


def test_privacy_config_keeps_builtin_rules_enabled(tmp_path) -> None:
    config = tmp_path / ".homelab-operator-privacy.toml"
    config.write_text(
        """[privacy]
[[privacy.deny_patterns]]
id = "synthetic.project-code"
description = "Synthetic project marker"
pattern = 'SYNTHETIC-PROJECT'
""",
        encoding="utf-8",
    )

    rules = load_privacy_config(config)
    result = scan_privacy(f"synthetic endpoint address: {dotted(192, 168, 12, 34)}", rules)

    assert not result.ok
    assert result.errors == ("Privacy scan matched rule `builtin.private-ipv4`: Private or loopback IPv4 address",)


def test_privacy_config_rejects_long_literal_without_echoing_pattern(tmp_path) -> None:
    config = tmp_path / ".homelab-operator-privacy.toml"
    bad_pattern = "SECRET-SAMPLE-" * 24
    config.write_text(
        f"""[privacy]
[[privacy.deny_patterns]]
id = "synthetic.long"
description = "Synthetic long literal"
pattern = '{bad_pattern}'
""",
        encoding="utf-8",
    )

    with pytest.raises(PrivacyConfigError) as exc_info:
        load_privacy_config(config)

    message = str(exc_info.value)
    assert "synthetic.long" in message
    assert "longer than 256" in message
    assert bad_pattern not in message


def test_privacy_config_patterns_are_literal_not_regex(tmp_path) -> None:
    config = tmp_path / ".homelab-operator-privacy.toml"
    config.write_text(
        """[privacy]
[[privacy.deny_patterns]]
id = "synthetic.literal"
description = "Synthetic literal marker"
pattern = '(a+)+$'
""",
        encoding="utf-8",
    )

    rules = load_privacy_config(config)
    result = scan_privacy("aaaaaaaaaaaaaaaaaaaaaaaaaaaa!", rules)

    assert result.ok
    assert scan_privacy("literal text contains (a+)+$", rules).errors == (
        "Privacy scan matched rule `synthetic.literal`: Synthetic literal marker",
    )


def test_privacy_config_rejects_malformed_shape(tmp_path) -> None:
    config = tmp_path / ".homelab-operator-privacy.toml"
    config.write_text("[privacy]\ndeny_patterns = \"not-a-list\"\n", encoding="utf-8")

    with pytest.raises(PrivacyConfigError, match="privacy.deny_patterns"):
        load_privacy_config(config)
