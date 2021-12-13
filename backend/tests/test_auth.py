import asyncio
from fastapi import Depends
from fastapi.exceptions import HTTPException
from app import auth
from unittest import mock
from jose import JWTError

import tests.test_entities as te


def test_verify_password():
    password, hash = te.get_valid_password_bcrypt_hash_combination()

    assert auth.verify_password(plain_password=password, hashed_password=hash)


def test_verify_password_invalid_password():
    password, hash = te.get_invalid_password_bcrypt_hash_combination()

    assert not auth.verify_password(
        plain_password=password, hashed_password=hash)


@mock.patch("app.auth.verify_password")
@mock.patch("app.auth.crud.get_user_by_email")
def test_authenticate_user(mock_crud_get_user_by_email, mock_auth_verify_password):

    te.setup()

    test_user = te.get_test_user_with_hashed_password()
    email = test_user.email
    password = te.get_valid_password()
    db = None

    mock_crud_get_user_by_email.return_value = test_user
    mock_auth_verify_password.return_value = True

    user = auth.authenticate_user(email=email, password=password, db=db)
    assert user == test_user

    te.teardown()


@mock.patch("app.auth.crud.get_user_by_email")
def test_authenticate_user_email_not_found(mock_crud_get_user_by_email):

    te.setup()

    email = te.get_valid_test_email()
    password = te.get_valid_password()
    db = None
    mock_crud_get_user_by_email.return_value = None

    user = auth.authenticate_user(email=email, password=password, db=db)
    assert user == False

    te.teardown()


@mock.patch("app.auth.verify_password")
@mock.patch("app.auth.crud.get_user_by_email")
def test_authenticate_user_incorrect_password(mock_crud_get_user_by_email, mock_auth_verify_password):

    te.setup()

    email = te.get_valid_test_email()
    password = te.get_valid_password()
    db = None
    mock_crud_get_user_by_email.return_value = te.get_test_user_with_hashed_password()
    mock_auth_verify_password.return_value = False

    user = auth.authenticate_user(email=email, password=password, db=db)
    assert user == False

    te.teardown()


@mock.patch("app.auth.jwt.decode")
def test_verify_token(mock_jwt_decode):

    te.setup()

    payload = te.get_valid_jwt_payload()
    token = te.get_access_token()

    mock_jwt_decode.return_value = payload

    email, is_admin = auth.verify_token(token)

    assert email == te.get_valid_test_email()
    assert is_admin == False

    te.teardown()


@mock.patch("app.auth.jwt.decode")
def test_verify_token_jwt_error(mock_jwt_decode):

    te.setup()

    mock_jwt_decode.side_effect = JWTError()
    token = te.get_access_token()
    assert auth.verify_token(token) == (None, False)

    te.teardown()


@mock.patch("app.auth.jwt.decode")
@mock.patch("app.auth.crud.get_user_by_email")
def test_get_current_user(mock_crud_get_user_by_email, mock_jwt_decode):

    te.setup()

    expected_user = te.get_test_user()
    token = te.get_access_token()
    payload = te.get_valid_jwt_payload()
    mock_crud_get_user_by_email.return_value = expected_user
    mock_jwt_decode.return_value = payload

    user = asyncio.run(auth.get_current_user(token=token))

    assert user == expected_user

    te.teardown()


@mock.patch("app.auth.jwt.decode")
def test_get_current_user_no_username(mock_jwt_decode):

    te.setup()

    http_exception = te.get_http_401_could_not_validate_credentials()
    token = te.get_access_token()
    payload = te.get_valid_jwt_payload()
    payload["sub"] = None

    mock_jwt_decode.return_value = payload

    try:
        user = asyncio.run(auth.get_current_user(token=token, db=None))
        te.teardown()
        raise Exception

    except HTTPException as http:
        assert http.status_code == http_exception.status_code
        assert http.detail == http_exception.detail
        assert http.headers == http_exception.headers

    te.teardown()


@mock.patch("app.auth.jwt.decode")
def test_get_current_user_jwt_error(mock_jwt_decode):

    te.setup()

    http_exception = te.get_http_401_could_not_validate_credentials()
    token = te.get_access_token()

    mock_jwt_decode.side_effect = JWTError()

    try:
        user = asyncio.run(auth.get_current_user(token=token, db=None))
        raise Exception

    except HTTPException as http:
        assert http.status_code == http_exception.status_code
        assert http.detail == http_exception.detail
        assert http.headers == http_exception.headers

    te.teardown()


@mock.patch("app.auth.jwt.decode")
@mock.patch("app.auth.crud.get_user_by_email")
def test_get_current_user_user_not_found(mock_crud_get_user_by_email, mock_jwt_decode):

    te.setup()

    http_exception = te.get_http_401_could_not_validate_credentials()
    token = te.get_access_token()
    payload = te.get_valid_jwt_payload()
    mock_crud_get_user_by_email.return_value = None
    mock_jwt_decode.return_value = payload

    try:
        user = asyncio.run(auth.get_current_user(token=token, db=None))
        raise Exception

    except HTTPException as http:
        assert http.status_code == http_exception.status_code
        assert http.detail == http_exception.detail
        assert http.headers == http_exception.headers

    te.teardown()


def test_get_current_active_user():

    te.setup()

    user_expected = te.get_test_user()

    user = asyncio.run(auth.get_current_active_user(
        current_user=user_expected))

    assert user == user_expected

    te.teardown()


def test_get_current_active_user_inactive():

    te.setup()

    inactive_user = te.get_inactive_test_user()
    http_exception = te.get_http_400_inactive_user()

    try:
        user = asyncio.run(auth.get_current_active_user(
            current_user=inactive_user))
        raise Exception

    except HTTPException as http:
        assert http.status_code == http_exception.status_code
        assert http.detail == http_exception.detail

    te.teardown()


def test_get_current_active_admin_user():

    te.setup()

    user_expected = te.get_test_admin_user()

    user = asyncio.run(auth.get_current_active_admin_user(
        current_user=user_expected))

    assert user == user_expected

    te.teardown()


def test_get_current_active_admin_user_not_admin():

    te.setup()

    non_admin_user = te.get_test_user()
    http_exception = te.get_http_401_unauthorized()

    try:
        user = asyncio.run(auth.get_current_active_admin_user(
            current_user=non_admin_user))
        raise Exception

    except HTTPException as http:
        assert http.status_code == http_exception.status_code
        assert http.detail == http_exception.detail

    te.teardown()
