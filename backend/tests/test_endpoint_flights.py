from unittest import mock

import pytest
import tests.test_entities as te
from app import auth, main


@ mock.patch("app.main.crud.get_all_flights")
def test_flights(mock_crud_get_all_flights):

    main.app.dependency_overrides[auth.get_current_active_user] = te.get_test_user

    flights_json = te.get_flights_json()
    flights = te.get_flights()

    mock_crud_get_all_flights.return_value = flights

    response_flights = te.client.get("/flights")

    assert response_flights.status_code == 200
    assert response_flights.json() == flights_json

    main.app.dependency_overrides = {}


def test_flights_unautenticated():

    main.app.dependency_overrides[auth.get_current_active_user] = te.raise_http_401_could_not_validate_credentials

    response_flights = te.client.get("/flights")

    assert response_flights.status_code == 401
    assert response_flights.json() == {
        "detail": "Could not validate credentials"}
    assert response_flights.headers["WWW-Authenticate"] == "Bearer"

    main.app.dependency_overrides = {}


def test_flights_inactive():

    main.app.dependency_overrides[auth.get_current_active_user] = te.raise_http_400_inactive_user

    response_flights = te.client.get("/flights")

    assert response_flights.status_code == 400
    assert response_flights.json() == {
        "detail": "Inactive user"}

    main.app.dependency_overrides = {}
