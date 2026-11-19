USERS: dict[str, dict[str, str]] = {}


def add_user(username: str, password_hash: str, role: str) -> None:
    USERS[username] = {"password_hash": password_hash, "role": role}


def get_user(username: str) -> dict[str, str] | None:
    return USERS.get(username)
