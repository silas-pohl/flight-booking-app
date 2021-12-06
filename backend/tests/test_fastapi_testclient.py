from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest import mock
from app import main, crud, schemas, mail, auth
from fastapi import HTTPException, status

import pytest


client = TestClient(main.app)


# test objects for mocking
def get_test_user():
    return schemas.User(
        email="test@test.test",
        first_name="test",
        last_name="test",
        id="0deb3503-8efd-4f47-b842-44975098ff32",
        is_active=True,
        is_admin=False
    )


def get_access_token():
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJwYXltZW50cy5mbGlnaHQuYm9va2luZ0BnbWFpbC5jb20iLCJhZG1pbiI6ZmFsc2UsImV4cCI6MTYzODU1MDI4N30.pcjYDatsOw7rtbOl36s0aruAaKwl6dWYPHrxR94iI-A"


def get_test_verification_entry():
    return schemas.EmailVerificationEntry(email="test@test.test",
                                          verification_code=12345678,
                                          created=datetime.now())


def get_valid_test_email():
    return "test@test.test"


def get_invalid_test_email():
    return "testtest.test"


def get_valid_names():
    return {
        "first_name": "Test",
        "last_name": "Test"
    }


def get_invalid_names():
    return {
        "first_name": "T",
        "last_name": "T"
    }


def get_valid_password():
    return "TestT3stT€st"


def get_invalid_password():
    return "TestT3st"


def get_tickets():
    ticket1 = schemas.Ticket(id="23c557f8-5fb6-4fc0-8cf6-a685d7680112", created=datetime(
        year=2021, month=12, day=3, hour=11, minute=23, second=25, microsecond=177772), owner_id="0deb3503-8efd-4f47-b842-44975098ff32", flight_id="20453064-2468-48ef-896f-b4a2513973a3")

    ticket2 = schemas.Ticket(id="e1d11a21-d346-4480-b4bb-c16da0347c3b", created=datetime(
        year=2021, month=12, day=4, hour=18, minute=14, second=9, microsecond=819645), owner_id="0deb3503-8efd-4f47-b842-44975098ff32", flight_id="20453064-2468-48ef-896f-b4a2513973a3")

    return [ticket1, ticket2]


def get_tickets_json():
    return [
        {
            "id": "23c557f8-5fb6-4fc0-8cf6-a685d7680112",
            "created": "2021-12-03T11:23:25.177772",
            "owner_id": "0deb3503-8efd-4f47-b842-44975098ff32",
            "flight_id": "20453064-2468-48ef-896f-b4a2513973a3"
        },
        {
            "id": "e1d11a21-d346-4480-b4bb-c16da0347c3b",
            "created": "2021-12-04T18:14:09.819645",
            "owner_id": "0deb3503-8efd-4f47-b842-44975098ff32",
            "flight_id": "20453064-2468-48ef-896f-b4a2513973a3"
        }
    ]


def get_ticket():
    return schemas.Ticket(id="23c557f8-5fb6-4fc0-8cf6-a685d7680112", created=datetime(
        year=2021, month=12, day=3, hour=11, minute=23, second=25, microsecond=177772), owner_id="0deb3503-8efd-4f47-b842-44975098ff32", flight_id="20453064-2468-48ef-896f-b4a2513973a3")


def get_ticket_json():
    return {
        "id": "23c557f8-5fb6-4fc0-8cf6-a685d7680112",
        "created": "2021-12-03T11:23:25.177772",
        "owner_id": "0deb3503-8efd-4f47-b842-44975098ff32",
        "flight_id": "20453064-2468-48ef-896f-b4a2513973a3"
    }


def get_airports():
    airport1 = schemas.Airport(
        title="JFK New York", id="9407584e-18b4-4023-86b1-884cc21ec647", description=None)
    airport2 = schemas.Airport(
        title="Munich Airport", id="41a7ead7-6dc3-4720-8108-35180659e39e", description=None)

    return [airport1, airport2]


def get_airports_json():
    return [
        {
            "title": "JFK New York",
            "id": "9407584e-18b4-4023-86b1-884cc21ec647",
            "description": None
        },
        {
            "title": "Munich Airport",
            "id": "41a7ead7-6dc3-4720-8108-35180659e39e",
            "description": None
        }
    ]


def get_airport():
    return schemas.Airport(
        title="JFK New York", id="9407584e-18b4-4023-86b1-884cc21ec647", description=None)


def get_airport_json():
    return {
        "title": "JFK New York",
        "id": "9407584e-18b4-4023-86b1-884cc21ec647",
        "description": None
    }


def get_flights():

    arrival_time = datetime(year=2021, month=12, day=3,
                            hour=11, minute=23, second=25, microsecond=151590)
    departure_time = datetime(
        year=2021, month=12, day=3, hour=11, minute=23, second=25, microsecond=151582)

    return [schemas.Flight(id="20453064-2468-48ef-896f-b4a2513973a3", arrival_time_utc=arrival_time,
                           destination_airport_id="41a7ead7-6dc3-4720-8108-35180659e39e", seats=24, departure_time_utc=departure_time,
                           departure_airport_id="9407584e-18b4-4023-86b1-884cc21ec647", ticket_price_dollars=20.0)]


def get_flights_json():
    return [
        {
            "id": "20453064-2468-48ef-896f-b4a2513973a3",
            "arrival_time_utc": "2021-12-03T11:23:25.151590",
            "destination_airport_id": "41a7ead7-6dc3-4720-8108-35180659e39e",
            "seats": 24,
            "departure_time_utc": "2021-12-03T11:23:25.151582",
            "departure_airport_id": "9407584e-18b4-4023-86b1-884cc21ec647",
            "ticket_price_dollars": 20.0
        }
    ]


def get_flight():
    arrival_time = datetime(year=2021, month=12, day=3,
                            hour=11, minute=23, second=25, microsecond=151590)
    departure_time = datetime(
        year=2021, month=12, day=3, hour=11, minute=23, second=25, microsecond=151582)

    return schemas.Flight(id="20453064-2468-48ef-896f-b4a2513973a3", arrival_time_utc=arrival_time,
                          destination_airport_id="41a7ead7-6dc3-4720-8108-35180659e39e", seats=24, departure_time_utc=departure_time,
                          departure_airport_id="9407584e-18b4-4023-86b1-884cc21ec647", ticket_price_dollars=20.0)


def get_flight_json():
    return{
        "id": "20453064-2468-48ef-896f-b4a2513973a3",
        "arrival_time_utc": "2021-12-03T11:23:25.151590",
        "destination_airport_id": "41a7ead7-6dc3-4720-8108-35180659e39e",
        "seats": 24,
        "departure_time_utc": "2021-12-03T11:23:25.151582",
        "departure_airport_id": "9407584e-18b4-4023-86b1-884cc21ec647",
        "ticket_price_dollars": 20.0
    }


# test exceptions for mocking
def raise_http_401_could_not_validate_credentials():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )


def raise_http_400_inactive_user():
    raise HTTPException(status_code=400, detail="Inactive user")


def raise_http_401_unauthorized():
    raise HTTPException(status_code=401, detail="Unauthorized")


def get_http_404_object_not_found():
    return HTTPException(status_code=404, detail="Object not found")


def get_http_422_invalid_id_format(id_type: str):
    return HTTPException(status_code=422, detail=[
        {
            "loc": [
                "path",
                id_type
            ],
            "msg": "value is not a valid uuid",
            "type": "type_error.uuid"
        }
    ])


# Endpoint unit tests

# /verificationcode
@ pytest.mark.parametrize("verification_entry", [(get_test_verification_entry()), (None)])
@ mock.patch("app.main.mail.send_verification_code")
@ mock.patch("app.main.crud")
def test_verification_code_valid_input_data(mock_crud, mock_send_verification_code, verification_entry):

    mock_crud.read_user_by_email.return_value = None
    mock_crud.delete_expired_verification_records.return_value = None
    mock_crud.read_verification_record.return_value = verification_entry
    mock_crud.create_verification_record.return_value = None
    mock_send_verification_code.return_value = None

    valid_email = get_valid_test_email()

    response_register = client.post(
        "/verificationcode", json={"email": valid_email, "action": "register"})
    assert response_register.status_code == 200
    assert response_register.json() == {
        "email": "test@test.test", "action": "register"}

    response_login = client.post(
        "/verificationcode", json={"email": valid_email, "action": "login"})
    assert response_login.status_code == 404
    assert response_login.json() == {"detail": "Email not registered"}

    response_reset = client.post(
        "/verificationcode", json={"email": valid_email, "action": "reset"})
    assert response_reset.status_code == 404
    assert response_reset.json() == {"detail": "Email not registered"}

    mock_crud.read_user_by_email.return_value = get_test_user()

    response_register = client.post(
        "/verificationcode", json={"email": valid_email, "action": "register"})
    assert response_register.status_code == 409
    assert response_register.json() == {"detail": "Email already registered"}

    response_login = client.post(
        "/verificationcode", json={"email": valid_email, "action": "login"})
    assert response_login.status_code == 200
    assert response_login.json() == {
        "email": "test@test.test", "action": "login"}

    response_reset = client.post(
        "/verificationcode", json={"email": valid_email, "action": "reset"})
    assert response_reset.status_code == 200
    assert response_reset.json() == {
        "email": "test@test.test", "action": "reset"}


def test_verification_code_invalid_email():

    invalid_email = get_invalid_test_email()
    response_register = client.post(
        "/verificationcode", json={"email": invalid_email, "action": "register"})
    assert response_register.status_code == 422
    assert response_register.json() == {"detail": "Invalid request data"}


def test_verification_code_invalid_action():

    valid_email = get_valid_test_email()
    response_register = client.post(
        "/verificationcode", json={"email": valid_email, "action": "invalid_request"})
    assert response_register.status_code == 422
    assert response_register.json() == {"detail": "Invalid request data"}

# /register


@ mock.patch("app.main.crud")
def test_register_valid_input_data(mock_crud):

    verification_entry = get_test_verification_entry()
    user = get_test_user()
    valid_password = get_valid_password()
    mock_crud.read_verification_record.return_value = verification_entry

    mock_crud.delete_verification_record.return_value = None
    mock_crud.create_user.return_value = user

    register_json = {"email": user.email, "first_name": user.first_name,
                     "last_name": user.last_name, "password": valid_password, "verification_code": verification_entry.verification_code}
    response_register = client.post(
        "/register", json=register_json)
    assert response_register.status_code == 200
    assert response_register.json() == register_json


def test_register_invalid_email():

    verification_entry = get_test_verification_entry()
    invalid_email = get_invalid_test_email()
    valid_names = get_valid_names()
    valid_first_name = valid_names["first_name"]
    valid_last_name = valid_names["last_name"]
    vaild_password = get_valid_password()

    register_json = {"email": invalid_email, "first_name": valid_first_name,
                     "last_name": valid_last_name, "password": vaild_password, "verification_code": verification_entry.verification_code}
    response_register = client.post(
        "/register", json=register_json)
    assert response_register.status_code == 422
    assert response_register.json() == {"detail": "Invalid request data"}


def test_register_invalid_first_name():

    valid_email = get_valid_test_email()
    invalid_first_name = get_invalid_names()["first_name"]
    valid_last_name = get_valid_names()["last_name"]
    valid_password = get_valid_password()
    verfication_entry = get_test_verification_entry()

    register_json = {"email": valid_email, "first_name": invalid_first_name,
                     "last_name": valid_last_name, "password": valid_password, "verification_code": verfication_entry.verification_code}
    response_register = client.post(
        "/register", json=register_json)
    assert response_register.status_code == 422
    assert response_register.json() == {"detail": "Invalid request data"}


def test_register_invalid_last_name():

    valid_email = get_valid_test_email()
    valid_first_name = get_valid_names()["first_name"]
    invalid_last_name = get_invalid_names()["last_name"]
    valid_password = get_valid_password()
    verfication_entry = get_test_verification_entry()

    register_json = {"email": valid_email, "first_name": valid_first_name,
                     "last_name": invalid_last_name, "password": valid_password, "verification_code": verfication_entry.verification_code}
    response_register = client.post(
        "/register", json=register_json)
    assert response_register.status_code == 422
    assert response_register.json() == {"detail": "Invalid request data"}


def test_register_invalid_password():

    valid_email = get_valid_test_email()
    valid_names = get_valid_names()
    valid_first_name = valid_names["first_name"]
    valid_last_name = valid_names["last_name"]
    invalid_password = get_invalid_password()
    verfication_entry = get_test_verification_entry()

    register_json = {"email": valid_email, "first_name": valid_first_name,
                     "last_name": valid_last_name, "password": invalid_password, "verification_code": verfication_entry.verification_code}
    response_register = client.post(
        "/register", json=register_json)
    assert response_register.status_code == 422
    assert response_register.json() == {"detail": "Invalid request data"}


@ mock.patch("app.main.crud")
def test_register_no_verification_entry(mock_crud):

    valid_email = get_valid_test_email()
    valid_names = get_valid_names()
    valid_first_name = valid_names["first_name"]
    valid_last_name = valid_names["last_name"]
    valid_password = get_valid_password()
    verfication_entry = get_test_verification_entry()

    mock_crud.read_verification_record.return_value = None

    register_json = {"email": valid_email, "first_name": valid_first_name,
                     "last_name": valid_last_name, "password": valid_password, "verification_code": verfication_entry.verification_code}
    response_register = client.post(
        "/register", json=register_json)
    assert response_register.status_code == 403
    assert response_register.json() == {
        "detail": "Incorrect verification code"}


@ mock.patch("app.main.crud")
def test_register_invalid_verification_code(mock_crud):

    valid_email = get_valid_test_email()
    valid_names = get_valid_names()
    valid_first_name = valid_names["first_name"]
    valid_last_name = valid_names["last_name"]
    valid_password = get_valid_password()
    verfication_entry = get_test_verification_entry()

    mock_crud.read_verification_record.return_value = verfication_entry

    register_json = {"email": valid_email, "first_name": valid_first_name,
                     "last_name": valid_last_name, "password": valid_password, "verification_code": verfication_entry.verification_code + 1}
    response_register = client.post(
        "/register", json=register_json)
    assert response_register.status_code == 403
    assert response_register.json() == {
        "detail": "Incorrect verification code"}


# /token
@ mock.patch("app.main.auth.create_access_token")
@ mock.patch("app.main.authenticate_user")
def test_token_valid_login(mock_authenticate_user, mock_create_access_token):
    mock_authenticate_user.return_value = get_test_user()
    mock_create_access_token.return_value = get_access_token()

    access_token = get_access_token()
    valid_username = get_valid_test_email()
    valid_password = get_valid_password()

    response_token = client.post(
        "/token", json={"username": valid_username, "password": valid_password
                        })

    assert response_token.status_code == 200
    assert response_token.json() == {
        "access_token": access_token, "token_type": "bearer"}


@ mock.patch("app.main.authenticate_user")
def test_token_non_matching_credentials(mock_authenticate_user):
    mock_authenticate_user.return_value = None

    valid_username = get_valid_test_email()
    valid_password = get_valid_password()

    response_token = client.post(
        "/token", json={"username": valid_username, "password": valid_password
                        })

    assert response_token.status_code == 401
    assert response_token.headers["WWW-Authenticate"] == "Bearer"
    assert response_token.json() == {
        "detail": "Incorrect email or password"}


# /me
def test_me():

    user = get_test_user()
    main.app.dependency_overrides[auth.get_current_active_user] = get_test_user
    response_me = client.get("/me")

    assert response_me.status_code == 200
    assert response_me.json() == {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name
    }
    main.app.dependency_overrides = {}


def test_me_unauthorized():

    main.app.dependency_overrides[auth.get_current_active_user] = raise_http_401_could_not_validate_credentials

    response_me = client.get("/me")

    assert response_me.status_code == 401
    assert response_me.json() == {
        "detail": "Could not validate credentials"}
    assert response_me.headers["WWW-Authenticate"] == "Bearer"
    main.app.dependency_overrides = {}


def test_me_inactive():

    main.app.dependency_overrides[auth.get_current_active_user] = raise_http_400_inactive_user

    response_me = client.get("/me")

    assert response_me.status_code == 400
    assert response_me.json() == {
        "detail": "Inactive user"}
    main.app.dependency_overrides = {}


# /me/tickets
@ mock.patch("app.main.crud.get_user_tickets")
def test_me_tickets(mock_crud_get_user_tickets):

    main.app.dependency_overrides[auth.get_current_active_user] = get_test_user

    tickets_json = get_tickets_json()
    tickets = get_tickets()
    mock_crud_get_user_tickets.return_value = tickets

    response_me_tickets = client.get("/me/tickets")

    assert response_me_tickets.status_code == 200
    assert response_me_tickets.json() == tickets_json

    main.app.dependency_overrides = {}


def test_me_tickets_unauthorized():

    main.app.dependency_overrides[auth.get_current_active_user] = raise_http_401_could_not_validate_credentials

    response_me_tickets = client.get("/me/tickets")

    assert response_me_tickets.status_code == 401
    assert response_me_tickets.json() == {
        "detail": "Could not validate credentials"}
    assert response_me_tickets.headers["WWW-Authenticate"] == "Bearer"
    main.app.dependency_overrides = {}


def test_me_tickets_inactive():

    main.app.dependency_overrides[auth.get_current_active_user] = raise_http_400_inactive_user

    response_me_tickets = client.get("/me/tickets")

    assert response_me_tickets.status_code == 400
    assert response_me_tickets.json() == {
        "detail": "Inactive user"}
    main.app.dependency_overrides = {}


# /me/tickets/ticket_id
@ mock.patch("app.main.crud.get_user_ticket")
def test_me_tickets_tickets_id(mock_crud_get_user_ticket):

    main.app.dependency_overrides[auth.get_current_active_user] = get_test_user

    ticket_json = get_ticket_json()
    ticket = get_ticket()
    mock_crud_get_user_ticket.return_value = ticket
    ticket_id = ticket.id

    response_me_tickets = client.get(
        f"/me/tickets/{ticket_id}")

    assert response_me_tickets.status_code == 200
    assert response_me_tickets.json() == ticket_json

    main.app.dependency_overrides = {}


@ mock.patch("app.main.crud.get_user_ticket")
def test_me_tickets_tickets_id_not_found(mock_crud_get_user_ticket):

    main.app.dependency_overrides[auth.get_current_active_user] = get_test_user

    mock_crud_get_user_ticket.side_effect = get_http_404_object_not_found()

    response_me_tickets = client.get(
        "/me/tickets/23c557f8-5fb6-4fc0-8cf6-a685d7684444")

    assert response_me_tickets.status_code == 404
    assert response_me_tickets.json() == {
        "detail": "Object not found"}

    main.app.dependency_overrides = {}


def test_me_tickets_tickets_id_invalid_id_format():

    main.app.dependency_overrides[auth.get_current_active_user] = get_test_user

    response_me_tickets = client.get(
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


def test_me_tickets_ticket_id_unauthorized():

    main.app.dependency_overrides[auth.get_current_active_user] = raise_http_401_could_not_validate_credentials

    response_me_tickets = client.get(
        "/me/tickets/23c557f8-5fb6-4fc0-8cf6-a685d7680112")

    assert response_me_tickets.status_code == 401
    assert response_me_tickets.json() == {
        "detail": "Could not validate credentials"}
    assert response_me_tickets.headers["WWW-Authenticate"] == "Bearer"
    main.app.dependency_overrides = {}


def test_me_tickets_ticket_id_inactive():

    main.app.dependency_overrides[auth.get_current_active_user] = raise_http_400_inactive_user

    response_me_tickets = client.get(
        "/me/tickets/23c557f8-5fb6-4fc0-8cf6-a685d7680112")

    assert response_me_tickets.status_code == 400
    assert response_me_tickets.json() == {
        "detail": "Inactive user"}
    main.app.dependency_overrides = {}


# /airports
@ mock.patch("app.main.crud.get_airports")
def test_airports(mock_crud_get_airports):

    main.app.dependency_overrides[auth.get_current_active_user] = get_test_user

    airports_json = get_airports_json()
    airports = get_airports()

    mock_crud_get_airports.return_value = airports

    response_airports = client.get("/airports")

    assert response_airports.status_code == 200
    assert response_airports.json() == airports_json

    main.app.dependency_overrides = {}


def test_airports_unauthorized():

    main.app.dependency_overrides[auth.get_current_active_user] = raise_http_401_could_not_validate_credentials

    response_airports = client.get("/airports")

    assert response_airports.status_code == 401
    assert response_airports.json() == {
        "detail": "Could not validate credentials"}
    assert response_airports.headers["WWW-Authenticate"] == "Bearer"
    main.app.dependency_overrides = {}


def test_airports_inactive():

    main.app.dependency_overrides[auth.get_current_active_user] = raise_http_400_inactive_user

    response_airports = client.get("/airports")

    assert response_airports.status_code == 400
    assert response_airports.json() == {
        "detail": "Inactive user"}
    main.app.dependency_overrides = {}


# /airports/airport_id
@ mock.patch("app.main.crud.get_airport")
def test_airports_airport_id(mock_crud_get_airport):

    main.app.dependency_overrides[auth.get_current_active_user] = get_test_user

    airport_json = get_airport_json()
    airport = get_airport()
    mock_crud_get_airport.return_value = airport

    response_airports = client.get(
        "/airports/9407584e-18b4-4023-86b1-884cc21ec647")

    assert response_airports.status_code == 200
    assert response_airports.json() == airport_json

    main.app.dependency_overrides = {}


@ mock.patch("app.main.crud.get_airport")
def test_airports_airport_id_not_found(mock_crud_get_airport):

    main.app.dependency_overrides[auth.get_current_active_user] = get_test_user

    mock_crud_get_airport.side_effect = get_http_404_object_not_found()

    response_airports = client.get(
        "/airports/9407584e-18b4-4023-86b1-884cc21e4444")

    assert response_airports.status_code == 404
    assert response_airports.json() == {
        "detail": "Object not found"}

    main.app.dependency_overrides = {}


def test_airports_airport_id_invalid_id_format():

    main.app.dependency_overrides[auth.get_current_active_user] = get_test_user

    response_airports = client.get(
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


def test_airports_airport_id_unauthorized():

    main.app.dependency_overrides[auth.get_current_active_user] = raise_http_401_could_not_validate_credentials

    response_airports = client.get(
        "/airports/9407584e-18b4-4023-86b1-884cc21e4444")

    assert response_airports.status_code == 401
    assert response_airports.json() == {
        "detail": "Could not validate credentials"}
    assert response_airports.headers["WWW-Authenticate"] == "Bearer"
    main.app.dependency_overrides = {}


def test_airports_airport_id_inactive():

    main.app.dependency_overrides[auth.get_current_active_user] = raise_http_400_inactive_user

    response_airports = client.get(
        "/airports/9407584e-18b4-4023-86b1-884cc21e4444")

    assert response_airports.status_code == 400
    assert response_airports.json() == {
        "detail": "Inactive user"}
    main.app.dependency_overrides = {}


# /flights
@ mock.patch("app.main.crud.get_all_flights")
def test_flights(mock_crud_get_all_flights):

    main.app.dependency_overrides[auth.get_current_active_user] = get_test_user

    flights_json = get_flights_json()
    flights = get_flights()

    mock_crud_get_all_flights.return_value = flights

    response_flights = client.get("/flights")

    assert response_flights.status_code == 200
    assert response_flights.json() == flights_json

    main.app.dependency_overrides = {}


def test_flights_unauthorized():

    main.app.dependency_overrides[auth.get_current_active_user] = raise_http_401_could_not_validate_credentials

    response_flights = client.get("/flights")

    assert response_flights.status_code == 401
    assert response_flights.json() == {
        "detail": "Could not validate credentials"}
    assert response_flights.headers["WWW-Authenticate"] == "Bearer"
    main.app.dependency_overrides = {}


def test_flights_inactive():

    main.app.dependency_overrides[auth.get_current_active_user] = raise_http_400_inactive_user

    response_flights = client.get("/flights")

    assert response_flights.status_code == 400
    assert response_flights.json() == {
        "detail": "Inactive user"}
    main.app.dependency_overrides = {}


# /flights/flight_id
@ mock.patch("app.main.crud.get_flight")
def test_flights_flight_id(mock_crud_get_flight):

    main.app.dependency_overrides[auth.get_current_active_user] = get_test_user

    flight_json = get_flight_json()
    flight = get_flight()

    mock_crud_get_flight.return_value = flight

    response_flights = client.get(
        "/flights/20453064-2468-48ef-896f-b4a2513973a3")

    assert response_flights.status_code == 200
    assert response_flights.json() == flight_json

    main.app.dependency_overrides = {}


@ mock.patch("app.main.crud.get_flight")
def test_flights_flight_id_not_found(mock_crud_get_flight):

    main.app.dependency_overrides[auth.get_current_active_user] = get_test_user

    mock_crud_get_flight.side_effect = get_http_404_object_not_found()

    response_flights = client.get(
        "/flights/20453064-2468-48ef-896f-b4a251394444")

    assert response_flights.status_code == 404
    assert response_flights.json() == {
        "detail": "Object not found"}

    main.app.dependency_overrides = {}


def test_flights_flight_id_invalid_id_format():

    main.app.dependency_overrides[auth.get_current_active_user] = get_test_user

    response_flights = client.get(
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


def test_flights_flight_id_unauthorized():

    main.app.dependency_overrides[auth.get_current_active_user] = raise_http_401_could_not_validate_credentials

    response_flights = client.get(
        "/flights/20453064-2468-48ef-896f-b4a2513973a3")

    assert response_flights.status_code == 401
    assert response_flights.json() == {
        "detail": "Could not validate credentials"}
    assert response_flights.headers["WWW-Authenticate"] == "Bearer"
    main.app.dependency_overrides = {}


def test_flights_flight_id_inactive():

    main.app.dependency_overrides[auth.get_current_active_user] = raise_http_400_inactive_user

    response_flights = client.get(
        "/flights/20453064-2468-48ef-896f-b4a2513973a3")

    assert response_flights.status_code == 400
    assert response_flights.json() == {
        "detail": "Inactive user"}
    main.app.dependency_overrides = {}


# /me/booking
@ mock.patch("app.main.crud")
def test_me_booking(mock_crud):
    main.app.dependency_overrides[auth.get_current_active_user] = get_test_user

    flight = get_flight()
    ticket = get_ticket()
    mock_crud.get_booked_tickets_number.return_value = flight.seats - 1
    mock_crud.get_flight.return_value = flight
    mock_crud.create_user_ticket.return_value = ticket

    response_me_booking = client.post(
        "/me/booking", json={"flight_id": str(flight.id)})
    assert response_me_booking.status_code == 200
    assert response_me_booking.json() == {"ticket_id": str(ticket.id)}


@ mock.patch("app.main.crud")
def test_me_booking_no_more_tickets_available(mock_crud):
    main.app.dependency_overrides[auth.get_current_active_user] = get_test_user

    flight = get_flight()
    mock_crud.get_booked_tickets_number.return_value = flight.seats
    mock_crud.get_flight.return_value = flight

    response_me_booking = client.post(
        "/me/booking", json={"flight_id": str(flight.id)})
    assert response_me_booking.status_code == 409
    assert response_me_booking.json(
    ) == {"detail": "No more tickets available for this flight."}


@ mock.patch("app.main.crud.get_flight")
def test_me_booking_flight_id_not_found(mock_crud_get_flight):

    main.app.dependency_overrides[auth.get_current_active_user] = get_test_user

    mock_crud_get_flight.side_effect = get_http_404_object_not_found()

    response_me_booking = client.post(
        "/me/booking", json={"flight_id": "20453064-2468-48ef-896f-b4a251394444"})

    assert response_me_booking.status_code == 404
    assert response_me_booking.json() == {
        "detail": "Object not found"}

    main.app.dependency_overrides = {}


def test_me_booking_flight_id_invalid_id_format():

    main.app.dependency_overrides[auth.get_current_active_user] = get_test_user

    respnse_me_booking = client.post(
        "/me/booking", json={"flight_id": "1234"})

    assert respnse_me_booking.status_code == 422
    assert respnse_me_booking.json() == {"detail": [
        {
            "loc": [
                "body",
                "flight_id"
            ],
            "msg": "value is not a valid uuid",
            "type": "type_error.uuid"
        }
    ]}

    main.app.dependency_overrides = {}


def test_me_booking_unauthorized():

    main.app.dependency_overrides[auth.get_current_active_user] = raise_http_401_could_not_validate_credentials

    respnse_me_booking = client.post(
        "/me/booking", json={"flight_id": "20453064-2468-48ef-896f-b4a2513973a3"})

    assert respnse_me_booking.status_code == 401
    assert respnse_me_booking.json() == {
        "detail": "Could not validate credentials"}
    assert respnse_me_booking.headers["WWW-Authenticate"] == "Bearer"
    main.app.dependency_overrides = {}


def test_me_booking_inactive():

    main.app.dependency_overrides[auth.get_current_active_user] = raise_http_400_inactive_user

    respnse_me_booking = client.post(
        "/me/booking", json={"flight_id": "20453064-2468-48ef-896f-b4a2513973a3"})

    assert respnse_me_booking.status_code == 400
    assert respnse_me_booking.json() == {
        "detail": "Inactive user"}
    main.app.dependency_overrides = {}


# /me/cancellation
