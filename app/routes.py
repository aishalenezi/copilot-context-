from flask import Flask, jsonify, request
from flask.typing import ResponseReturnValue

from app import config
from app.auth import create_token, hash_password, require_auth, verify_password
from app.db import add_user, get_user
from app.utils import format_error


app = Flask(__name__)

if config.DEMO_USER_PASSWORD:
    add_user("asha", hash_password(config.DEMO_USER_PASSWORD), "admin")


@app.route("/login", methods=["POST"])
def login() -> ResponseReturnValue:
    """Authenticate a user and return an access token."""
    data = request.get_json(silent=True) or {}
    username = data.get("username", "")
    password = data.get("password", "")
    if not verify_password(username, password):
        return format_error("invalid credentials", 401)
    return jsonify({"token": create_token(username)})


@app.route("/profile")
@require_auth
def profile(username: str) -> ResponseReturnValue:
    """Return the authenticated user's profile."""
    user = get_user(username)
    if user is None:
        return format_error("user not found", 404)
    return jsonify({"username": username, "role": user["role"]})


@app.route("/health")
def health() -> ResponseReturnValue:
    """Return the service health status."""
    return jsonify({"status": "healthy"})


@app.route("/me/role")
@require_auth
def me_role(username: str) -> ResponseReturnValue:
    """Return only the authenticated user's role."""
    user = get_user(username)
    if user is None:
        return format_error("user not found", 404)
    return jsonify({"role": user["role"]})
