from fastapi.testclient import TestClient

from app import main, crud, schemas
from unittest import mock

client = TestClient(main.app)


@mock.patch("app.main.crud")
def test_verification_code_valid_input(mock_crud):

    mock_crud.read_user_by_email.return_value = None
    mock_crud.delete_expired_verification_records.return_value = None
    mock_crud._verification_record.return_value = None

    response_register = client.post(
        "/verificationcode", json={"email": "test@test.test", "action": "register"})
    assert response_register.status_code == 200
    assert response_register.json() == {
        "email": "test@test.test", "action": "register"}

    response_login = client.post(
        "/verificationcode", json={"email": "test@test.test", "action": "login"})
    assert response_login.status_code == 404
    assert response_login.json() == {"detail": "Email not registered"}

    response_reset = client.post(
        "/verificationcode", json={"email": "test@test.test", "action": "reset"})
    assert response_reset.status_code == 404
    assert response_reset.json() == {"detail": "Email not registered"}

    mock_crud.read_user_by_email.return_value = schemas.User(
        email="test@test.test",
        first_name="test",
        last_name="test",
        id="f10c09e6-6f13-4a6a-98b5-b4302656653d",
        is_active=True,
        is_admin=False
    )

    response_register = client.post(
        "/verificationcode", json={"email": "test@test.test", "action": "register"})
    assert response_register.status_code == 409
    assert response_register.json() == {"detail": "Email already registered"}

    response_login = client.post(
        "/verificationcode", json={"email": "test@test.test", "action": "login"})
    assert response_login.status_code == 200
    assert response_login.json() == {
        "email": "test@test.test", "action": "login"}

    response_reset = client.post(
        "/verificationcode", json={"email": "test@test.test", "action": "reset"})
    assert response_reset.status_code == 200
    assert response_reset.json() == {
        "email": "test@test.test", "action": "reset"}


def test_verification_code_invalid_email():
    response_register = client.post(
        "/verificationcode", json={"email": "testtest.test", "action": "register"})
    assert response_register.status_code == 422
    assert response_register.json() == {"detail": "Invalid request data"}


def test_verification_code_invalid_action():
    response_register = client.post(
        "/verificationcode", json={"email": "test@test.test", "action": "invalid_request"})
    assert response_register.status_code == 422
    assert response_register.json() == {"detail": "Invalid request data"}
