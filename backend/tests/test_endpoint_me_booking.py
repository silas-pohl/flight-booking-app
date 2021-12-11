from unittest import mock

import tests.test_entities as te
from app import auth, main


@ mock.patch("app.main.crud")
def test_me_booking(mock_crud):

    te.setup()

    main.app.dependency_overrides[auth.get_current_active_user] = te.get_test_user

    flight = te.get_flight()
    ticket = te.get_ticket()
    mock_crud.get_booked_tickets_number.return_value = flight.seats - 1
    mock_crud.get_flight.return_value = flight
    mock_crud.create_user_ticket.return_value = ticket

    response_me_booking = te.client.post(
        "/me/booking", json={"flight_id": str(flight.id)})

    assert response_me_booking.status_code == 200
    assert response_me_booking.json() == {"ticket_id": str(ticket.id)}

    te.teardown()


@ mock.patch("app.main.crud")
def test_me_booking_no_more_tickets_available(mock_crud):

    te.setup()

    main.app.dependency_overrides[auth.get_current_active_user] = te.get_test_user

    flight = te.get_flight()
    mock_crud.get_booked_tickets_number.return_value = flight.seats
    mock_crud.get_flight.return_value = flight

    response_me_booking = te.client.post(
        "/me/booking", json={"flight_id": str(flight.id)})

    assert response_me_booking.status_code == 409
    assert response_me_booking.json(
    ) == {"detail": "No more tickets available for this flight."}

    te.teardown()


@ mock.patch("app.main.crud.get_flight")
def test_me_booking_flight_id_not_found(mock_crud_get_flight):

    te.setup()

    main.app.dependency_overrides[auth.get_current_active_user] = te.get_test_user

    mock_crud_get_flight.side_effect = te.get_http_404_object_not_found()

    response_me_booking = te.client.post(
        "/me/booking", json={"flight_id": "20453064-2468-48ef-896f-b4a251394444"})

    assert response_me_booking.status_code == 404
    assert response_me_booking.json() == {
        "detail": "Object not found"}

    te.teardown()


def test_me_booking_flight_id_invalid_id_format():

    te.setup()

    main.app.dependency_overrides[auth.get_current_active_user] = te.get_test_user

    response_me_booking = te.client.post(
        "/me/booking", json={"flight_id": "1234"})

    assert response_me_booking.status_code == 422
    assert response_me_booking.json() == {"detail": [
        {
            "loc": [
                "body",
                "flight_id"
            ],
            "msg": "value is not a valid uuid",
            "type": "type_error.uuid"
        }
    ]}

    te.teardown()


def test_me_booking_unauthenticated():

    te.setup()

    main.app.dependency_overrides[auth.get_current_active_user] = te.raise_http_401_could_not_validate_credentials

    response_me_booking = te.client.post(
        "/me/booking", json={"flight_id": "20453064-2468-48ef-896f-b4a2513973a3"})

    assert response_me_booking.status_code == 401
    assert response_me_booking.json() == {
        "detail": "Could not validate credentials"}
    assert response_me_booking.headers["WWW-Authenticate"] == "Bearer"

    te.teardown()


def test_me_booking_inactive():

    te.setup()

    main.app.dependency_overrides[auth.get_current_active_user] = te.raise_http_400_inactive_user

    response_me_booking = te.client.post(
        "/me/booking", json={"flight_id": "20453064-2468-48ef-896f-b4a2513973a3"})

    assert response_me_booking.status_code == 400
    assert response_me_booking.json() == {
        "detail": "Inactive user"}

    te.teardown()
