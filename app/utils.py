import re
import unicodedata


def format_error(message: str, status: int = 400) -> tuple[dict[str, str], int]:
    """Create a consistent JSON error response.

    Args:
        message: The error message to return.
        status: The HTTP status code.

    Returns:
        The JSON-compatible body and HTTP status code.
    """
    return {"error": message}, status


def slugify(text: str) -> str:
    """Convert text to a lowercase, hyphen-separated URL slug.

    Args:
        text: The text to convert.

    Returns:
        An ASCII slug with punctuation and whitespace replaced by hyphens.

    Raises:
        ValueError: If text is not a string.
    """
    if not isinstance(text, str):
        raise ValueError("text must be a string")

    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"[^a-z0-9]+", "-", ascii_text).strip("-")
