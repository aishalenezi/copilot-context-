from flask.testing import FlaskClient

from app.auth import create_token


def test_me_role_requires_authentication(client: FlaskClient) -> None:
    response = client.get("/me/role")

    assert response.status_code == 401


def test_me_role_returns_only_authenticated_user_role(client: FlaskClient) -> None:
    token = create_token("asha")
    response = client.get(
        "/me/role", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.get_json() == {"role": "admin"}
