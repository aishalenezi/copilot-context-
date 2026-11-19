import pytest

from app.utils import format_error, slugify


def test_format_error_returns_body_and_status() -> None:
    assert format_error("not found", 404) == ({"error": "not found"}, 404)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hello, World!", "hello-world"),
        ("Café au lait", "cafe-au-lait"),
        ("already-slugged", "already-slugged"),
    ],
)
def test_slugify_converts_text(text: str, expected: str) -> None:
    assert slugify(text) == expected


def test_slugify_rejects_non_string_input() -> None:
    with pytest.raises(ValueError, match="text must be a string"):
        slugify(None)  # type: ignore[arg-type]
