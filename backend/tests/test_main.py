from app import main
from unittest import mock

import pytest


@mock.patch("app.main.crud.get_refresh_token")
@mock.patch("app.main.auth.verify_token")
def test_validate_token(mock_auth_verify_token, mock_crud_refresh_token):
    pass


@mock.patch("app.main.auth.verify_token")
def test_validate_token_not_found(mock_auth_verify_token):
    pass


@mock.patch("app.main.crud.get_refresh_token")
@mock.patch("app.main.auth.verify_token")
def test_validate_token_not_verified(mock_auth_verify_token, mock_crud_refresh_token):
    pass
