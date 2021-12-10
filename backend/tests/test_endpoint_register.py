from unittest import mock

import pytest
import tests.test_entities as te


@ mock.patch("app.main.crud")
def test_register_valid_input_data(mock_crud):

    verification_entry = te.get_test_verification_entry()
    user = te.get_test_user()
    valid_password = te.get_valid_password()
    mock_crud.read_verification_record.return_value = verification_entry

    mock_crud.delete_verification_record.return_value = None
    mock_crud.create_user.return_value = user

    register_json = {"email": user.email, "first_name": user.first_name,
                     "last_name": user.last_name, "password": valid_password, "verification_code": verification_entry.verification_code}
    response_register = te.client.post(
        "/register", json=register_json)
    assert response_register.status_code == 200
    assert response_register.json() == register_json


def test_register_invalid_email():

    verification_entry = te.get_test_verification_entry()
    invalid_email = te.get_invalid_test_email()
    valid_names = te.get_valid_names()
    valid_first_name = valid_names["first_name"]
    valid_last_name = valid_names["last_name"]
    vaild_password = te.get_valid_password()

    register_json = {"email": invalid_email, "first_name": valid_first_name,
                     "last_name": valid_last_name, "password": vaild_password, "verification_code": verification_entry.verification_code}
    response_register = te.client.post(
        "/register", json=register_json)
    assert response_register.status_code == 422
    assert response_register.json() == {"detail": "Invalid request data"}


def test_register_invalid_first_name():

    valid_email = te.get_valid_test_email()
    invalid_first_name = te.get_invalid_names()["first_name"]
    valid_last_name = te.get_valid_names()["last_name"]
    valid_password = te.get_valid_password()
    verfication_entry = te.get_test_verification_entry()

    register_json = {"email": valid_email, "first_name": invalid_first_name,
                     "last_name": valid_last_name, "password": valid_password, "verification_code": verfication_entry.verification_code}
    response_register = te.client.post(
        "/register", json=register_json)
    assert response_register.status_code == 422
    assert response_register.json() == {"detail": "Invalid request data"}


def test_register_invalid_last_name():

    valid_email = te.get_valid_test_email()
    valid_first_name = te.get_valid_names()["first_name"]
    invalid_last_name = te.get_invalid_names()["last_name"]
    valid_password = te.get_valid_password()
    verfication_entry = te.get_test_verification_entry()

    register_json = {"email": valid_email, "first_name": valid_first_name,
                     "last_name": invalid_last_name, "password": valid_password, "verification_code": verfication_entry.verification_code}
    response_register = te.client.post(
        "/register", json=register_json)
    assert response_register.status_code == 422
    assert response_register.json() == {"detail": "Invalid request data"}


def test_register_invalid_password():

    valid_email = te.get_valid_test_email()
    valid_names = te.get_valid_names()
    valid_first_name = valid_names["first_name"]
    valid_last_name = valid_names["last_name"]
    invalid_password = te.get_invalid_password()
    verfication_entry = te.get_test_verification_entry()

    register_json = {"email": valid_email, "first_name": valid_first_name,
                     "last_name": valid_last_name, "password": invalid_password, "verification_code": verfication_entry.verification_code}
    response_register = te.client.post(
        "/register", json=register_json)
    assert response_register.status_code == 422
    assert response_register.json() == {"detail": "Invalid request data"}


@ mock.patch("app.main.crud")
def test_register_no_verification_entry(mock_crud):

    valid_email = te.get_valid_test_email()
    valid_names = te.get_valid_names()
    valid_first_name = valid_names["first_name"]
    valid_last_name = valid_names["last_name"]
    valid_password = te.get_valid_password()
    verfication_entry = te.get_test_verification_entry()

    mock_crud.read_verification_record.return_value = None

    register_json = {"email": valid_email, "first_name": valid_first_name,
                     "last_name": valid_last_name, "password": valid_password, "verification_code": verfication_entry.verification_code}
    response_register = te.client.post(
        "/register", json=register_json)
    assert response_register.status_code == 403
    assert response_register.json() == {
        "detail": "Incorrect verification code"}


@ mock.patch("app.main.crud")
def test_register_invalid_verification_code(mock_crud):

    valid_email = te.get_valid_test_email()
    valid_names = te.get_valid_names()
    valid_first_name = valid_names["first_name"]
    valid_last_name = valid_names["last_name"]
    valid_password = te.get_valid_password()
    verfication_entry = te.get_test_verification_entry()

    mock_crud.read_verification_record.return_value = verfication_entry

    register_json = {"email": valid_email, "first_name": valid_first_name,
                     "last_name": valid_last_name, "password": valid_password, "verification_code": verfication_entry.verification_code + 1}
    response_register = te.client.post(
        "/register", json=register_json)
    assert response_register.status_code == 403
    assert response_register.json() == {
        "detail": "Incorrect verification code"}
