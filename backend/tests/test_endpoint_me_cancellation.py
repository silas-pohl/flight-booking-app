from unittest import mock
from datetime import datetime, timedelta

import tests.test_entities as te
from app import auth, main


@ mock.patch("app.main.crud")
def me_cancellation(mock_crud):

    te.setup()

    main.app.dependency_overrides[auth.get_current_active_user] = te.get_test_user

    ticket = te.get_ticket()
    ticket.created = datetime.now()
    mock_crud.get_user_ticket.return_value = ticket

    response_me_cancellation = te.client.post(
        "/me/cancellation", json={"ticket_id": str(ticket.id)})

    assert response_me_cancellation.status_code == 200
    assert response_me_cancellation.json() == {"ticket_id": str(ticket.id)}

    te.teardown()


@ mock.patch("app.main.crud.get_user_ticket")
def test_me_cancellation_less_than_48_hours(mock_crud_get_user_ticket):

    te.setup()

    main.app.dependency_overrides[auth.get_current_active_user] = te.get_test_user

    ticket = te.get_ticket()
    ticket.created = datetime.now() - timedelta(hours=48)
    mock_crud_get_user_ticket.return_value = ticket

    response_me_cancellation = te.client.post(
        "/me/cancellation", json={"ticket_id": str(ticket.id)})

    assert response_me_cancellation.status_code == 409
    assert response_me_cancellation.json(
    ) == {"detail": "Cancellation is only available until 48h before takeoff"}

    te.teardown()


@ mock.patch("app.main.crud.get_user_ticket")
def test_me_cancellation_ticket_id_not_found(mock_crud_get_ticket):

    te.setup()

    main.app.dependency_overrides[auth.get_current_active_user] = te.get_test_user

    mock_crud_get_ticket.side_effect = te.get_http_404_object_not_found()

    response_me_cancellation = te.client.post(
        "/me/cancellation", json={"ticket_id": "20453064-2468-48ef-896f-b4a251394444"})

    assert response_me_cancellation.status_code == 404
    assert response_me_cancellation.json() == {
        "detail": "Object not found"}

    te.teardown()


def test_me_cancellation_ticket_id_invalid_id_format():

    te.setup()

    main.app.dependency_overrides[auth.get_current_active_user] = te.get_test_user

    response_me_cancellation = te.client.post(
        "/me/cancellation", json={"ticket_id": "1234"})

    assert response_me_cancellation.status_code == 422
    assert response_me_cancellation.json() == {"detail": [
        {
            "loc": [
                "body",
                "ticket_id"
            ],
            "msg": "value is not a valid uuid",
            "type": "type_error.uuid"
        }
    ]}

    te.teardown()


def test_me_cancellation_unauthenticated():

    te.setup()

    main.app.dependency_overrides[auth.get_current_active_user] = te.raise_http_401_could_not_validate_credentials

    response_me_cancellation = te.client.post(
        "/me/cancellation", json={"ticket_id": "20453064-2468-48ef-896f-b4a2513973a3"})

    assert response_me_cancellation.status_code == 401
    assert response_me_cancellation.json() == {
        "detail": "Could not validate credentials"}
    assert response_me_cancellation.headers["WWW-Authenticate"] == "Bearer"

    te.teardown()


def test_me_cancellation_inactive():

    te.setup()

    main.app.dependency_overrides[auth.get_current_active_user] = te.raise_http_400_inactive_user

    response_me_cancellation = te.client.post(
        "/me/cancellation", json={"ticket_id": "20453064-2468-48ef-896f-b4a2513973a3"})

    assert response_me_cancellation.status_code == 400
    assert response_me_cancellation.json() == {
        "detail": "Inactive user"}

    te.teardown()


def test_me_booking_admin():

    te.setup()

    main.app.dependency_overrides[auth.get_current_active_user] = te.get_test_admin_user

    response_me_booking = te.client.post(
        "/me/booking", json={"ticket_id": "20453064-2468-48ef-896f-b4a2513973a3"})

    assert response_me_booking.status_code == 401
    assert response_me_booking.json() == {
        "detail": "Action not allowed for admins"}

    te.teardown()
