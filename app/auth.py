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
    return hashlib.pbkdf2_hmac(
        "sha256", password.encode(), config.SECRET_KEY.encode(), 100_000
    ).hex()


def verify_password(username: str, password: str) -> bool:
    user = get_user(username)
    if not user:
        return False
    return hmac.compare_digest(user["password_hash"], hash_password(password))


def _sign(payload: str) -> str:
    return hmac.new(
        config.SECRET_KEY.encode(), payload.encode(), "sha256"
    ).hexdigest()


def create_token(username: str) -> str:
    expires = int(time.time()) + config.TOKEN_TTL_SECONDS
    payload = f"{username}:{expires}"
    raw = f"{payload}:{_sign(payload)}"
    return base64.urlsafe_b64encode(raw.encode()).decode()


def decode_token(token: str) -> str | None:
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


def validate_username(username: str) -> bool:
    return (
        3 <= len(username) <= 20
        and username.isascii()
        and all(character.isalnum() or character == "_" for character in username)
    )


def require_auth(
    view: Callable[Concatenate[str, P], ResponseReturnValue],
) -> Callable[P, ResponseReturnValue]:
    @wraps(view)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> ResponseReturnValue:
        header = request.headers.get("Authorization", "")
        username = decode_token(header.removeprefix("Bearer "))
        if not username:
            return jsonify({"error": "unauthorized"}), 401
        return view(username, *args, **kwargs)

    return wrapper
