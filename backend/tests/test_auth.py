import unittest
from app import auth, main, schemas
from unittest import mock
from tests.test_fastapi_testclient import get_test_user, get_test_admin_user, get_valid_test_email, get_valid_password, get_test_user_with_hashed_password, raise_http_401_could_not_validate_credentials, get_http_401_could_not_validate_credentials

import pytest


def test_get_password_hash():
    pass


def test_verify_password():
    pass


def test_verify_password_incorrect():
    pass


@mock.patch("app.auth.verify_password")
@mock.patch("app.auth.crud.get_user_by_email")
def test_authenticate_user(mock_crud_get_user_by_email, mock_auth_verify_password):

    test_user = get_test_user_with_hashed_password()
    email = test_user.email
    password = get_valid_password()
    db = None

    mock_crud_get_user_by_email.return_value = test_user
    mock_auth_verify_password.return_value = True

    user = auth.authenticate_user(email=email, password=password, db=db)
    assert user == test_user


@mock.patch("app.auth.crud.get_user_by_email")
def test_authenticate_user_email_not_found(mock_crud_get_user_by_email):

    email = get_valid_test_email()
    password = get_valid_password()
    db = None
    mock_crud_get_user_by_email.return_value = None

    user = auth.authenticate_user(email=email, password=password, db=db)
    assert user == False


@mock.patch("app.auth.verify_password")
@mock.patch("app.auth.crud.get_user_by_email")
def test_authenticate_user_incorrect_password(mock_crud_get_user_by_email, mock_auth_verify_password):

    email = get_valid_test_email()
    password = get_valid_password()
    db = None
    mock_crud_get_user_by_email.return_value = get_test_user_with_hashed_password()
    mock_auth_verify_password.return_value = False

    user = auth.authenticate_user(email=email, password=password, db=db)
    assert user == False


def test_create_access_token():
    pass


def test_create_access_token_with_expires_delta():
    pass


@mock.patch("app.auth.crud.add_refresh_token")
def test_create_refresh_token(mock_crud_add_refresh_token):
    pass


def test_verify_token():
    pass


def test_verify_token_no_email():
    pass


@mock.patch("app.auth.jwt.decode")
def test_verify_token_jwt_error(mock_jwt_decode):
    pass


@mock.patch("app.auth.crud.get_user_by_email")
def test_get_current_user(mock_crud_get_user_by_email):
    pass


@mock.patch("app.auth.crud.get_user_by_email")
def test_get_current_user_no_username(mock_crud_get_user_by_email):
    pass


@mock.patch("app.auth.crud.get_user_by_email")
def test_get_current_user_jwt_error(mock_crud_get_user_by_email):
    pass


@mock.patch("app.auth.crud.get_user_by_email")
def test_get_current_user_user_not_found(mock_crud_get_user_by_email):
    pass


def test_get_current_active_user():
    main.app.dependency_overrides[auth.get_current_user] = get_test_user
    user = get_test_user()
    assert auth.get_current_active_user() == user

    main.app.dependency_overrides = {}


def test_get_current_active_user_inactive():
    main.app.dependency_overrides[auth.get_current_user] = get_test_user

    main.app.dependency_overrides = {}


def test_get_current_active_user_credentials_exception():
    main.app.dependency_overrides[auth.get_current_user] = raise_http_401_could_not_validate_credentials
    http_exception = get_http_401_could_not_validate_credentials()
    unittest.TestCase.assertRaises(
        http_exception, auth.get_current_active_user)
    main.app.dependency_overrides = {}


def test_get_current_active_admin_user():
    main.app.dependency_overrides[auth.get_current_active_user] = get_test_admin_user

    main.app.dependency_overrides = {}


def test_get_current_active_admin_user_inactive():
    main.app.dependency_overrides[auth.get_current_active_user] = None

    main.app.dependency_overrides = {}


def test_get_current_active_admin_user_credentials_exception():
    main.app.dependency_overrides[auth.get_current_active_user] = None

    main.app.dependency_overrides = {}


def test_get_current_active_admin_user_not_admin():
    main.app.dependency_overrides[auth.get_current_active_user] = get_test_user

    main.app.dependency_overrides = {}
