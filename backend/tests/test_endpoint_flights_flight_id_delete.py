from unittest import mock

import tests.test_entities as te
from app import auth, main, schemas


@ mock.patch("app.main.crud.delete_flight")
def test_flights_flight_id_delete(mock_crud_delete_flight):

    te.setup()

    main.app.dependency_overrides[auth.get_current_active_user] = te.get_test_admin_user

    flight = te.get_flight()

    mock_crud_delete_flight.return_value = schemas.FlightID(
        flight_id=flight.id)

    response_flights_delete = te.client.delete(
        f"/flights/{flight.id}")

    assert response_flights_delete.status_code == 200
    assert response_flights_delete.json() == {
        "flight_id": f"{flight.id}"}

    te.teardown()


@ mock.patch("app.main.crud.delete_flight")
def test_flights_flight_id_delete_id_not_found(mock_crud_delete_flight):

    te.setup()

    main.app.dependency_overrides[auth.get_current_active_user] = te.get_test_admin_user

    mock_crud_delete_flight.side_effect = te.get_http_404_object_not_found()

    response_flights_delete = te.client.delete(
        "/flights/20453064-2468-48ef-896f-b4a251394444")

    assert response_flights_delete.status_code == 404
    assert response_flights_delete.json() == {
        "detail": "Object not found"}

    te.teardown()


def test_flights_flight_id_delete_invalid_id_format():

    te.setup()

    main.app.dependency_overrides[auth.get_current_active_user] = te.get_test_admin_user

    response_flights_delete = te.client.delete("/flights/1234")

    assert response_flights_delete.status_code == 422
    assert response_flights_delete.json() == {"detail": [
        {
            "loc": [
                "path",
                "flight_id"
            ],
            "msg": "value is not a valid uuid",
            "type": "type_error.uuid"
        }
    ]}

    te.teardown()


def test_flights_flight_id_delete_unauthenticated():

    te.setup()

    main.app.dependency_overrides[auth.get_current_active_admin_user] = te.raise_http_401_could_not_validate_credentials

    response_flights_delete = te.client.delete(
        "/flights/20453064-2468-48ef-896f-b4a251394444")
    assert response_flights_delete.status_code == 401
    assert response_flights_delete.json() == {
        "detail": "Could not validate credentials"}
    assert response_flights_delete.headers["WWW-Authenticate"] == "Bearer"

    te.teardown()


def test_flights_flight_id_delete_unauthorized():

    te.setup()

    main.app.dependency_overrides[auth.get_current_active_admin_user] = te.raise_http_401_unauthorized

    response_flights_delete = te.client.delete(
        "/flights/20453064-2468-48ef-896f-b4a251394444")
    assert response_flights_delete.status_code == 401
    assert response_flights_delete.json() == {
        "detail": "Unauthorized"}

    te.teardown()


def test_flights_flight_id_delete_inactive():

    te.setup()

    main.app.dependency_overrides[auth.get_current_active_admin_user] = te.raise_http_400_inactive_user

    response_flights_delete = te.client.delete(
        "/flights/20453064-2468-48ef-896f-b4a251394444")

    assert response_flights_delete.status_code == 400
    assert response_flights_delete.json() == {
        "detail": "Inactive user"}

    te.teardown()
