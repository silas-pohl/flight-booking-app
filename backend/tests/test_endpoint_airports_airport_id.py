from unittest import mock

import pytest
import tests.test_entities as te
from app import auth, main


@ mock.patch("app.main.crud.get_airport")
def test_airports_airport_id(mock_crud_get_airport):

    main.app.dependency_overrides[auth.get_current_active_user] = te.get_test_user

    airport_json = te.get_airport_json()
    airport = te.get_airport()
    mock_crud_get_airport.return_value = airport

    response_airports = te.client.get(
        f"/airports/{airport.id}")

    assert response_airports.status_code == 200
    assert response_airports.json() == airport_json

    main.app.dependency_overrides = {}


@ mock.patch("app.main.crud.get_airport")
def test_airports_airport_id_not_found(mock_crud_get_airport):

    main.app.dependency_overrides[auth.get_current_active_user] = te.get_test_user

    mock_crud_get_airport.side_effect = te.get_http_404_object_not_found()

    response_airports = te.client.get(
        "/airports/9407584e-18b4-4023-86b1-884cc21e4444")

    assert response_airports.status_code == 404
    assert response_airports.json() == {
        "detail": "Object not found"}

    main.app.dependency_overrides = {}


def test_airports_airport_id_invalid_id_format():

    main.app.dependency_overrides[auth.get_current_active_user] = te.get_test_user

    response_airports = te.client.get(
        "/airports/1234")

    assert response_airports.status_code == 422
    assert response_airports.json() == {"detail": [
        {
            "loc": [
                "path",
                "airport_id"
            ],
            "msg": "value is not a valid uuid",
            "type": "type_error.uuid"
        }
    ]}

    main.app.dependency_overrides = {}


def test_airports_airport_id_unauthenticated():

    main.app.dependency_overrides[auth.get_current_active_user] = te.raise_http_401_could_not_validate_credentials

    response_airports = te.client.get(
        "/airports/9407584e-18b4-4023-86b1-884cc21e4444")

    assert response_airports.status_code == 401
    assert response_airports.json() == {
        "detail": "Could not validate credentials"}
    assert response_airports.headers["WWW-Authenticate"] == "Bearer"

    main.app.dependency_overrides = {}


def test_airports_airport_id_inactive():

    main.app.dependency_overrides[auth.get_current_active_user] = te.raise_http_400_inactive_user

    response_airports = te.client.get(
        "/airports/9407584e-18b4-4023-86b1-884cc21e4444")

    assert response_airports.status_code == 400
    assert response_airports.json() == {
        "detail": "Inactive user"}

    main.app.dependency_overrides = {}
