import base64
import binascii
import hashlib
import hmac
import time
from functools import wraps
from typing import Callable, Concatenate, ParamSpec

from flask import jsonify, request
from flask.typing import ResponseReturnValue

from app import config
from app.db import get_user


P = ParamSpec("P")


def hash_password(password: str) -> str:
    """Hash a password with PBKDF2 and the configured application secret.

    Args:
        password: The plaintext password.

    Returns:
        The hexadecimal password hash.
    """
    return hashlib.pbkdf2_hmac(
        "sha256", password.encode(), config.SECRET_KEY.encode(), 100_000
    ).hex()


def verify_password(username: str, password: str) -> bool:
    """Check a password against the stored hash for a user.

    Args:
        username: The account name.
        password: The plaintext password to check.

    Returns:
        Whether the password matches the stored hash.
    """
    user = get_user(username)
    if not user:
        return False
    return hmac.compare_digest(user["password_hash"], hash_password(password))


def _sign(payload: str) -> str:
    return hmac.new(
        config.SECRET_KEY.encode(), payload.encode(), "sha256"
    ).hexdigest()


def create_token(username: str) -> str:
    """Create a signed, expiring token for a user.

    Args:
        username: The account name to encode.

    Returns:
        A URL-safe encoded token.
    """
    expires = int(time.time()) + config.TOKEN_TTL_SECONDS
    payload = f"{username}:{expires}"
    raw = f"{payload}:{_sign(payload)}"
    return base64.urlsafe_b64encode(raw.encode()).decode()


def decode_token(token: str) -> str | None:
    """Return the token's username, or None when the token is invalid.

    Args:
        token: The encoded token to validate.

    Returns:
        The username when valid; otherwise, None.
    """
    try:
        raw = base64.urlsafe_b64decode(token.encode()).decode()
        username, expires, signature = raw.split(":")
        expiration = int(expires)
    except (binascii.Error, UnicodeDecodeError, ValueError):
        return None
    if not hmac.compare_digest(signature, _sign(f"{username}:{expires}")):
        return None
    if expiration < time.time():
        return None
    return username


def validate_username(username: str) -> str:
    """Validate a username and return it unchanged.

    Args:
        username: The username to validate.

    Returns:
        The validated username.

    Raises:
        ValueError: If the username violates the allowed length or characters.
    """
    if (
        not isinstance(username, str)
        or not 3 <= len(username) <= 20
        or not username.isascii()
        or not all(
            character.isalnum() or character == "_" for character in username
        )
    ):
        raise ValueError(
            "username must be 3 to 20 characters using only letters, numbers, "
            "and underscores"
        )
    return username


def require_auth(
    view: Callable[Concatenate[str, P], ResponseReturnValue],
) -> Callable[P, ResponseReturnValue]:
    """Protect a Flask view by requiring a valid bearer token.

    Args:
        view: A view function whose first argument is the authenticated username.

    Returns:
        A wrapped view that returns an unauthorized response for invalid tokens.
    """
    @wraps(view)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> ResponseReturnValue:
        header = request.headers.get("Authorization", "")
        username = decode_token(header.removeprefix("Bearer "))
        if not username:
            return jsonify({"error": "unauthorized"}), 401
        return view(username, *args, **kwargs)

    return wrapper
