from unittest import mock

import pytest
import tests.test_entities as te
from app import auth, main


@ mock.patch("app.main.crud.get_flight")
def test_flights_flight_id(mock_crud_get_flight):

    main.app.dependency_overrides[auth.get_current_active_user] = te.get_test_user

    flight_json = te.get_flight_json()
    flight = te.get_flight()

    mock_crud_get_flight.return_value = flight

    response_flights = te.client.get(
        f"/flights/{flight.id}")

    assert response_flights.status_code == 200
    assert response_flights.json() == flight_json

    main.app.dependency_overrides = {}


@ mock.patch("app.main.crud.get_flight")
def test_flights_flight_id_not_found(mock_crud_get_flight):

    main.app.dependency_overrides[auth.get_current_active_user] = te.get_test_user

    mock_crud_get_flight.side_effect = te.get_http_404_object_not_found()

    response_flights = te.client.get(
        "/flights/20453064-2468-48ef-896f-b4a251394444")

    assert response_flights.status_code == 404
    assert response_flights.json() == {
        "detail": "Object not found"}

    main.app.dependency_overrides = {}


def test_flights_flight_id_invalid_id_format():

    main.app.dependency_overrides[auth.get_current_active_user] = te.get_test_user

    response_flights = te.client.get(
        "/flights/1234")

    assert response_flights.status_code == 422
    assert response_flights.json() == {"detail": [
        {
            "loc": [
                "path",
                "flight_id"
            ],
            "msg": "value is not a valid uuid",
            "type": "type_error.uuid"
        }
    ]}

    main.app.dependency_overrides = {}


def test_flights_flight_id_unauthenticated():

    main.app.dependency_overrides[auth.get_current_active_user] = te.raise_http_401_could_not_validate_credentials

    response_flights = te.client.get(
        "/flights/20453064-2468-48ef-896f-b4a2513973a3")

    assert response_flights.status_code == 401
    assert response_flights.json() == {
        "detail": "Could not validate credentials"}
    assert response_flights.headers["WWW-Authenticate"] == "Bearer"

    main.app.dependency_overrides = {}


def test_flights_flight_id_inactive():

    main.app.dependency_overrides[auth.get_current_active_user] = te.raise_http_400_inactive_user

    response_flights = te.client.get(
        "/flights/20453064-2468-48ef-896f-b4a2513973a3")

    assert response_flights.status_code == 400
    assert response_flights.json() == {
        "detail": "Inactive user"}

    main.app.dependency_overrides = {}
