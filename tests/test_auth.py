import pytest

from app.auth import create_token, decode_token, validate_username


def test_decode_token_round_trip() -> None:
    token = create_token("asha")

    assert decode_token(token) == "asha"


def test_decode_token_invalid_returns_none() -> None:
    assert decode_token("not-a-token") is None


@pytest.mark.parametrize(
    ("username", "expected"),
    [
        ("asha_01", True),
        ("ab", False),
        ("a" * 21, False),
        ("asha-name", False),
    ],
)
def test_validate_username_before_instructions(username: str, expected: bool) -> None:
    assert validate_username(username) is expected
