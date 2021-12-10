import unittest

from fastapi import Depends
from fastapi.exceptions import HTTPException
from app import auth, main, schemas
from unittest import mock
from backend.tests.test_entities import get_valid_test_email
import tests.test_entities as te

import pytest


@mock.patch("app.auth.verify_password")
@mock.patch("app.auth.crud.get_user_by_email")
def test_authenticate_user(mock_crud_get_user_by_email, mock_auth_verify_password):

    test_user = te.get_test_user_with_hashed_password()
    email = test_user.email
    password = te.get_valid_password()
    db = None

    mock_crud_get_user_by_email.return_value = test_user
    mock_auth_verify_password.return_value = True

    user = auth.authenticate_user(email=email, password=password, db=db)
    assert user == test_user


@mock.patch("app.auth.crud.get_user_by_email")
def test_authenticate_user_email_not_found(mock_crud_get_user_by_email):

    email = te.get_valid_test_email()
    password = te.get_valid_password()
    db = None
    mock_crud_get_user_by_email.return_value = None

    user = auth.authenticate_user(email=email, password=password, db=db)
    assert user == False


@mock.patch("app.auth.verify_password")
@mock.patch("app.auth.crud.get_user_by_email")
def test_authenticate_user_incorrect_password(mock_crud_get_user_by_email, mock_auth_verify_password):

    email = te.get_valid_test_email()
    password = te.get_valid_password()
    db = None
    mock_crud_get_user_by_email.return_value = te.get_test_user_with_hashed_password()
    mock_auth_verify_password.return_value = False

    user = auth.authenticate_user(email=email, password=password, db=db)
    assert user == False


def test_verify_token():
    token = te.get_access_token()

    email, is_admin = auth.verify_token(token)

    assert email == te.get_valid_test_email()
    assert is_admin == False


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

    main.app.dependency_overrides[auth.get_current_user] = te.get_test_user

    user = te.get_test_user()
    user_expected = auth.get_current_active_user()

    assert user == user_expected


def test_get_current_active_user_inactive():

    main.app.dependency_overrides[auth.get_current_user] = te.get_inactive_test_user

    http_exception = te.get_http_400_inactive_user()

    try:
        user = auth.get_current_active_user()
        raise Exception

    except HTTPException as http:
        assert http == http_exception

    main.app.dependency_overrides = {}


def test_get_current_active_user_credentials_exception():

    main.app.dependency_overrides[auth.get_current_user] = te.raise_http_401_could_not_validate_credentials

    http_exception = te.get_http_401_could_not_validate_credentials()

    try:
        user = auth.get_current_active_user()
        raise Exception

    except HTTPException as http:
        assert http == http_exception

    main.app.dependency_overrides = {}


def test_get_current_active_admin_user():

    main.app.dependency_overrides[auth.get_current_active_user] = te.get_test_admin_user

    main.app.dependency_overrides = {}


def test_get_current_active_admin_user_inactive():

    main.app.dependency_overrides[auth.get_current_active_user] = te.raise_http_400_inactive_user

    http_exception = te.get_http_400_inactive_user

    try:
        user = auth.get_current_active_admin_user()
        raise Exception

    except HTTPException as http:
        assert http == http_exception

    main.app.dependency_overrides = {}


def test_get_current_active_admin_user_credentials_exception():

    main.app.dependency_overrides[auth.get_current_active_user] = te.raise_http_401_could_not_validate_credentials

    http_exception = te.get_http_401_could_not_validate_credentials()

    try:
        user = auth.get_current_active_admin_user()
        raise Exception
    except HTTPException as http:
        assert http == http_exception

    main.app.dependency_overrides = {}


def test_get_current_active_admin_user_not_admin():

    main.app.dependency_overrides[auth.get_current_active_user] = te.get_test_user

    http_exception = te.get_http_401_unauthorized()

    try:
        user = auth.get_current_active_admin_user()
        raise Exception
    except HTTPException as http:
        assert http == http_exception

    main.app.dependency_overrides = {}
