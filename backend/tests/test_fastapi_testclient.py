from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest import mock
from app import main, crud, schemas, mail

import pytest


client = TestClient(main.app)


def get_test_user():
    return schemas.User(
        email="test@test.test",
        first_name="test",
        last_name="test",
        id="f10c09e6-6f13-4a6a-98b5-b4302656653d",
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


@pytest.mark.parametrize("verification_entry", [(get_test_verification_entry()), (None)])
@mock.patch("app.main.mail.send_verification_code")
@mock.patch("app.main.get_db")
@mock.patch("app.main.crud")
def test_verification_code_valid_input_data(mock_crud, mock_get_db, mock_send_verification_code, verification_entry):

    mock_crud.read_user_by_email.return_value = None
    mock_crud.delete_expired_verification_records.return_value = None
    mock_crud.read_verification_record.return_value = verification_entry
    mock_crud.create_verification_record.return_value = None
    mock_get_db.return_value = None
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


@mock.patch("app.main.get_db")
def test_verification_code_invalid_email(mock_get_db):
    mock_get_db.return_value = None

    invalid_email = get_invalid_test_email()
    response_register = client.post(
        "/verificationcode", json={"email": invalid_email, "action": "register"})
    assert response_register.status_code == 422
    assert response_register.json() == {"detail": "Invalid request data"}


@mock.patch("app.main.get_db")
def test_verification_code_invalid_action(mock_get_db):
    mock_get_db.return_value = None

    valid_email = get_valid_test_email()
    response_register = client.post(
        "/verificationcode", json={"email": valid_email, "action": "invalid_request"})
    assert response_register.status_code == 422
    assert response_register.json() == {"detail": "Invalid request data"}


@mock.patch("app.main.get_db")
@mock.patch("app.main.crud")
def test_register_valid_input_data(mock_crud, mock_get_db):
    verification_entry = get_test_verification_entry()
    user = get_test_user()
    valid_password = get_valid_password()
    mock_crud.read_verification_record.return_value = verification_entry

    mock_crud.delete_verification_record.return_value = None
    mock_crud.create_user.return_value = user
    mock_get_db.return_value = None

    register_json = {"email": user.email, "first_name": user.first_name,
                     "last_name": user.last_name, "password": valid_password, "verification_code": verification_entry.verification_code}
    response_register = client.post(
        "/register", json=register_json)
    assert response_register.status_code == 200
    assert response_register.json() == register_json


@mock.patch("app.main.get_db")
def test_register_invalid_email(mock_get_db):
    mock_get_db.return_value = None

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


@mock.patch("app.main.get_db")
def test_register_invalid_first_name(mock_get_db):
    mock_get_db.return_value = None

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


@mock.patch("app.main.get_db")
def test_register_invalid_last_name(mock_get_db):
    mock_get_db.return_value = None

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


@mock.patch("app.main.get_db")
def test_register_invalid_password(mock_get_db):
    mock_get_db.return_value = None

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


@mock.patch("app.main.get_db")
@mock.patch("app.main.crud")
def test_register_no_verification_entry(mock_crud, mock_get_db):
    mock_get_db.return_value = None

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


@mock.patch("app.main.get_db")
@mock.patch("app.main.crud")
def test_register_invalid_verification_code(mock_crud, mock_get_db):
    mock_get_db.return_value = None

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


@mock.patch("app.main.get_db")
@mock.patch("app.main.auth.create_access_token")
@mock.patch("app.main.authenticate_user")
def test_token_valid_login(mock_authenticate_user, mock_create_access_token, mock_get_db):
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


@mock.patch("app.main.get_db")
@mock.patch("app.main.authenticate_user")
def test_token_non_matching_credentials(mock_authenticate_user, mock_get_db):
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
