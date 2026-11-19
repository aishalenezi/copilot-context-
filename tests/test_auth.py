import pytest

from app.auth import create_token, decode_token, validate_username


def test_decode_token_round_trip() -> None:
    token = create_token("asha")

    assert decode_token(token) == "asha"


def test_decode_token_invalid_returns_none() -> None:
    assert decode_token("not-a-token") is None


def test_validate_username_accepts_allowed_value() -> None:
    assert validate_username("asha_01") == "asha_01"


@pytest.mark.parametrize("username", ["ab", "a" * 21, "asha-name", "àsha"])
def test_validate_username_rejects_invalid_value(username: str) -> None:
    with pytest.raises(ValueError, match="username must be"):
        validate_username(username)
