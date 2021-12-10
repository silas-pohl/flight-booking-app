from unittest import mock
import pytest
import tests.test_entities as te
from app import main, auth


@ mock.patch("app.main.crud.get_user_ticket")
def test_me_tickets_tickets_id(mock_crud_get_user_ticket):

    main.app.dependency_overrides[auth.get_current_active_user] = te.get_test_user

    ticket_json = te.get_ticket_json()
    ticket = te.get_ticket()
    mock_crud_get_user_ticket.return_value = ticket
    ticket_id = ticket.id

    response_me_tickets = te.client.get(
        f"/me/tickets/{ticket_id}")

    assert response_me_tickets.status_code == 200
    assert response_me_tickets.json() == ticket_json

    main.app.dependency_overrides = {}


@ mock.patch("app.main.crud.get_user_ticket")
def test_me_tickets_tickets_id_not_found(mock_crud_get_user_ticket):

    main.app.dependency_overrides[auth.get_current_active_user] = te.get_test_user

    mock_crud_get_user_ticket.side_effect = te.get_http_404_object_not_found()

    response_me_tickets = te.client.get(
        "/me/tickets/23c557f8-5fb6-4fc0-8cf6-a685d7684444")

    assert response_me_tickets.status_code == 404
    assert response_me_tickets.json() == {
        "detail": "Object not found"}

    main.app.dependency_overrides = {}


def test_me_tickets_tickets_id_invalid_id_format():

    main.app.dependency_overrides[auth.get_current_active_user] = te.get_test_user

    response_me_tickets = te.client.get(
        "/me/tickets/1234")

    assert response_me_tickets.status_code == 422
    assert response_me_tickets.json() == {"detail": [
        {
            "loc": [
                "path",
                "ticket_id"
            ],
            "msg": "value is not a valid uuid",
            "type": "type_error.uuid"
        }
    ]}

    main.app.dependency_overrides = {}


def test_me_tickets_ticket_id_unauthenticated():

    main.app.dependency_overrides[auth.get_current_active_user] = te.raise_http_401_could_not_validate_credentials

    response_me_tickets = te.client.get(
        "/me/tickets/23c557f8-5fb6-4fc0-8cf6-a685d7680112")

    assert response_me_tickets.status_code == 401
    assert response_me_tickets.json() == {
        "detail": "Could not validate credentials"}
    assert response_me_tickets.headers["WWW-Authenticate"] == "Bearer"

    main.app.dependency_overrides = {}


def test_me_tickets_ticket_id_inactive():

    main.app.dependency_overrides[auth.get_current_active_user] = te.raise_http_400_inactive_user

    response_me_tickets = te.client.get(
        "/me/tickets/23c557f8-5fb6-4fc0-8cf6-a685d7680112")

    assert response_me_tickets.status_code == 400
    assert response_me_tickets.json() == {
        "detail": "Inactive user"}

    main.app.dependency_overrides = {}
