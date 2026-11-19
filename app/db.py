USERS: dict[str, dict[str, str]] = {}


def add_user(username: str, password_hash: str, role: str) -> None:
    """Add or replace an in-memory user record.

    Args:
        username: The account name.
        password_hash: The hashed password.
        role: The user's application role.
    """
    USERS[username] = {"password_hash": password_hash, "role": role}


def get_user(username: str) -> dict[str, str] | None:
    """Return a user record by account name.

    Args:
        username: The account name to look up.

    Returns:
        The user record, or None when no matching user exists.
    """
    return USERS.get(username)
