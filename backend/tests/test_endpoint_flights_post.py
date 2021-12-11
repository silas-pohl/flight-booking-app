from unittest import mock
from datetime import timedelta
import uuid
import tests.test_entities as te
from app import auth, main, crud


@mock.patch("app.main.crud.create_flight")
def test_flights_post(mock_crud_create_flight):

    te.setup()

    main.app.dependency_overrides[auth.get_current_active_admin_user] = te.get_test_admin_user

    flight = te.get_flight()
    flight_json = te.get_flight_json()
    flight_json_no_id = te.get_flight_json()
    flight_json_no_id.pop("id")

    mock_crud_create_flight.return_value = flight

    reponse_flights_post = te.client.post("/flights", json=flight_json_no_id)

    assert reponse_flights_post.status_code == 200
    assert reponse_flights_post.json() == flight_json

    te.teardown()


def test_flights_post_arrival_time_earlier_than_departure_time():

    te.setup()

    main.app.dependency_overrides[auth.get_current_active_admin_user] = te.get_test_admin_user

    flight = te.get_flight()
    flight.arrival_time_utc = flight.departure_time_utc - timedelta(seconds=1)
    flight_json_no_id = {
        "arrival_time_utc": str(flight.arrival_time_utc),
        "destination_airport_id": str(flight.destination_airport_id),
        "seats": flight.seats,
        "departure_time_utc": str(flight.departure_time_utc),
        "departure_airport_id": str(flight.departure_airport_id),
        "ticket_price_dollars": flight.ticket_price_dollars
    }

    reponse_flights_post = te.client.post("/flights", json=flight_json_no_id)

    assert reponse_flights_post.status_code == 422
    assert reponse_flights_post.json(
    ) == {"detail": "Arrival time must not be earlier than departure time."}

    te.teardown()


@mock.patch("app.main.crud.get_airport")
def test_flights_post_unknown_departure_or_destination_airport(mock_crud_get_airport):

    te.setup()

    main.app.dependency_overrides[auth.get_current_active_admin_user] = te.get_test_admin_user

    mock_crud_get_airport.side_effect = te.get_http_404_object_not_found()

    flight = te.get_flight()
    flight_json_no_id = {
        "arrival_time_utc": str(flight.arrival_time_utc),
        "destination_airport_id": str(uuid.uuid4()),
        "seats": flight.seats,
        "departure_time_utc": str(flight.departure_time_utc),
        "departure_airport_id": str(flight.departure_airport_id),
        "ticket_price_dollars": flight.ticket_price_dollars
    }

    reponse_flights_post = te.client.post("/flights", json=flight_json_no_id)

    assert reponse_flights_post.status_code == 404
    assert reponse_flights_post.json(
    ) == {"detail": "Object not found"}

    te.teardown()


def test_flights_post_negative_seats():

    te.setup()

    main.app.dependency_overrides[auth.get_current_active_admin_user] = te.get_test_admin_user

    flight = te.get_flight()
    flight_json_no_id = {
        "arrival_time_utc": str(flight.arrival_time_utc),
        "destination_airport_id": str(flight.destination_airport_id),
        "seats": -1,
        "departure_time_utc": str(flight.departure_time_utc),
        "departure_airport_id": str(flight.departure_airport_id),
        "ticket_price_dollars": flight.ticket_price_dollars
    }

    reponse_flights_post = te.client.post("/flights", json=flight_json_no_id)

    assert reponse_flights_post.status_code == 422
    assert reponse_flights_post.json(
    ) == {"detail": "Number of available seats must be greater than or equal to zero."}

    te.teardown()


def test_flights_post_negative_ticket_price():

    te.setup()

    main.app.dependency_overrides[auth.get_current_active_admin_user] = te.get_test_admin_user

    flight = te.get_flight()
    flight_json_no_id = {
        "arrival_time_utc": str(flight.arrival_time_utc),
        "destination_airport_id": str(flight.destination_airport_id),
        "seats": flight.seats,
        "departure_time_utc": str(flight.departure_time_utc),
        "departure_airport_id": str(flight.departure_airport_id),
        "ticket_price_dollars": -1
    }

    reponse_flights_post = te.client.post("/flights", json=flight_json_no_id)

    assert reponse_flights_post.status_code == 422
    assert reponse_flights_post.json(
    ) == {"detail": "Ticket price must be greater than or equal to zero."}

    te.teardown()


def test_flights_post_unauthenticated():

    te.setup()

    main.app.dependency_overrides[auth.get_current_active_admin_user] = te.raise_http_401_could_not_validate_credentials

    flight_json_no_id = te.get_flight_json()
    flight_json_no_id.pop("id")

    response_flights_post = te.client.post(
        "/flights", json=flight_json_no_id)
    assert response_flights_post.status_code == 401
    assert response_flights_post.json() == {
        "detail": "Could not validate credentials"}
    assert response_flights_post.headers["WWW-Authenticate"] == "Bearer"

    te.teardown()


def test_flights_post_unauthorized():

    te.setup()

    main.app.dependency_overrides[auth.get_current_active_admin_user] = te.raise_http_401_unauthorized

    flight_json_no_id = te.get_flight_json()
    flight_json_no_id.pop("id")

    response_flights_post = te.client.post(
        "/flights", json=flight_json_no_id)
    assert response_flights_post.status_code == 401
    assert response_flights_post.json() == {
        "detail": "Unauthorized"}

    te.teardown()


def test_flight_post_inactive():

    te.setup()

    main.app.dependency_overrides[auth.get_current_active_admin_user] = te.raise_http_400_inactive_user

    flight_json_no_id = te.get_flight_json()
    flight_json_no_id.pop("id")

    response_flights_post = te.client.post(
        "/flights", json=flight_json_no_id)

    assert response_flights_post.status_code == 400
    assert response_flights_post.json() == {
        "detail": "Inactive user"}

    te.teardown()
