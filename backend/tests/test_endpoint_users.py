from unittest import mock

import tests.test_entities as te
from app import auth, main


@mock.patch("app.main.crud.get_users")
def test_users(mock_crud_get_users):

    te.setup()

    main.app.dependency_overrides[auth.get_current_active_admin_user] = te.get_test_admin_user

    users = te.get_test_users()
    users_json = te.get_test_users_json()

    mock_crud_get_users.return_value = users

    response_users = te.client.get(
        "/users")
    assert response_users.status_code == 200
    assert response_users.json() == users_json

    te.teardown()


def test_users_unauthenticated():

    te.setup()

    main.app.dependency_overrides[auth.get_current_active_admin_user] = te.raise_http_401_could_not_validate_credentials

    response_users = te.client.get(
        "/users")
    assert response_users.status_code == 401
    assert response_users.json() == {
        "detail": "Could not validate credentials"}
    assert response_users.headers["WWW-Authenticate"] == "Bearer"

    te.teardown()


def test_users_unauthorized():

    te.setup()

    main.app.dependency_overrides[auth.get_current_active_admin_user] = te.raise_http_401_unauthorized

    response_users = te.client.get("/users")
    assert response_users.status_code == 401
    assert response_users.json() == {
        "detail": "Unauthorized"}

    te.teardown()


def test_users_inactive():

    te.setup()

    main.app.dependency_overrides[auth.get_current_active_admin_user] = te.raise_http_400_inactive_user

    response_users = te.client.get("/users")

    assert response_users.status_code == 400
    assert response_users.json() == {
        "detail": "Inactive user"}

    te.teardown()
