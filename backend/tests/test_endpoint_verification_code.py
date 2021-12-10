from unittest import mock

import pytest
import tests.test_entities as te


@ pytest.mark.parametrize("verification_entry", [(te.get_test_verification_entry()), (None)])
@ mock.patch("app.main.mail.send_verification_code")
@ mock.patch("app.main.crud")
def test_verification_code_valid_input_data(mock_crud, mock_send_verification_code, verification_entry):

    mock_crud.get_user_by_email.return_value = None
    mock_crud.delete_expired_verification_records.return_value = None
    mock_crud.read_verification_record.return_value = verification_entry
    mock_crud.create_verification_record.return_value = None
    mock_send_verification_code.return_value = None

    valid_email = te.get_valid_test_email()

    response_register = te.client.post(
        "/verificationcode", json={"email": valid_email, "action": "register"})
    assert response_register.status_code == 200
    assert response_register.json() == {
        "email": "test@test.test", "action": "register"}

    response_login = te.client.post(
        "/verificationcode", json={"email": valid_email, "action": "login"})
    assert response_login.status_code == 404
    assert response_login.json() == {"detail": "Email not registered"}

    response_reset = te.client.post(
        "/verificationcode", json={"email": valid_email, "action": "reset"})
    assert response_reset.status_code == 404
    assert response_reset.json() == {"detail": "Email not registered"}

    mock_crud.get_user_by_email.return_value = te.get_test_user_with_hashed_password()

    response_register = te.client.post(
        "/verificationcode", json={"email": valid_email, "action": "register"})
    assert response_register.status_code == 409
    assert response_register.json() == {"detail": "Email already registered"}

    response_login = te.client.post(
        "/verificationcode", json={"email": valid_email, "action": "login"})
    assert response_login.status_code == 200
    assert response_login.json() == {
        "email": "test@test.test", "action": "login"}

    response_reset = te.client.post(
        "/verificationcode", json={"email": valid_email, "action": "reset"})
    assert response_reset.status_code == 200
    assert response_reset.json() == {
        "email": "test@test.test", "action": "reset"}


def test_verification_code_invalid_email():

    invalid_email = te.get_invalid_test_email()
    response_register = te.client.post(
        "/verificationcode", json={"email": invalid_email, "action": "register"})
    assert response_register.status_code == 422
    assert response_register.json() == {"detail": "Invalid request data"}


def test_verification_code_invalid_action():

    valid_email = te.get_valid_test_email()
    response_register = te.client.post(
        "/verificationcode", json={"email": valid_email, "action": "invalid_request"})
    assert response_register.status_code == 422
    assert response_register.json() == {"detail": "Invalid request data"}
