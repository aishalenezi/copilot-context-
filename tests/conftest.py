import os
from collections.abc import Iterator

import pytest
from flask.testing import FlaskClient

os.environ.setdefault("APP_SECRET_KEY", "test-only-secret")
os.environ.setdefault("DEMO_USER_PASSWORD", "test-only-password")


@pytest.fixture
def client() -> Iterator[FlaskClient]:
    from app.routes import app

    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client
