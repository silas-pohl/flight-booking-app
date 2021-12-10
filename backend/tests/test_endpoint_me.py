from unittest import mock
import pytest
import tests.test_entities as te
from app import main, auth


def test_me():

    main.app.dependency_overrides[auth.get_current_active_user] = te.get_test_user

    user = te.get_test_user()

    response_me = te.client.get("/me")

    assert response_me.status_code == 200
    assert response_me.json() == {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name
    }

    main.app.dependency_overrides = {}


def test_me_unauthenticated():

    main.app.dependency_overrides[auth.get_current_active_user] = te.raise_http_401_could_not_validate_credentials

    response_me = te.client.get("/me")

    assert response_me.status_code == 401
    assert response_me.json() == {
        "detail": "Could not validate credentials"}
    assert response_me.headers["WWW-Authenticate"] == "Bearer"

    main.app.dependency_overrides = {}


def test_me_inactive():

    main.app.dependency_overrides[auth.get_current_active_user] = te.raise_http_400_inactive_user

    response_me = te.client.get("/me")

    assert response_me.status_code == 400
    assert response_me.json() == {
        "detail": "Inactive user"}

    main.app.dependency_overrides = {}
