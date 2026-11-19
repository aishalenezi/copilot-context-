def format_error(message: str, status: int = 400) -> tuple[dict[str, str], int]:
    return {"error": message}, status
