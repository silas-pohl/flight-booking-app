from unittest import mock

import pytest
import tests.test_entities as te
from app import auth, main


@ mock.patch("app.main.crud.get_airports")
def test_airports(mock_crud_get_airports):

    main.app.dependency_overrides[auth.get_current_active_user] = te.get_test_user

    airports_json = te.get_airports_json()
    airports = te.get_airports()

    mock_crud_get_airports.return_value = airports

    response_airports = te.client.get("/airports")

    assert response_airports.status_code == 200
    assert response_airports.json() == airports_json

    main.app.dependency_overrides = {}


def test_airports_unauthenticated():

    main.app.dependency_overrides[auth.get_current_active_user] = te.raise_http_401_could_not_validate_credentials

    response_airports = te.client.get("/airports")

    assert response_airports.status_code == 401
    assert response_airports.json() == {
        "detail": "Could not validate credentials"}
    assert response_airports.headers["WWW-Authenticate"] == "Bearer"

    main.app.dependency_overrides = {}


def test_airports_inactive():

    main.app.dependency_overrides[auth.get_current_active_user] = te.raise_http_400_inactive_user

    response_airports = te.client.get("/airports")

    assert response_airports.status_code == 400
    assert response_airports.json() == {
        "detail": "Inactive user"}

    main.app.dependency_overrides = {}
