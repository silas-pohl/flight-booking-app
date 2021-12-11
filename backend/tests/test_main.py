from app import main, models
from unittest import mock
from tests.test_entities import get_valid_test_email, get_refresh_token
import tests.test_entities as te

import pytest


@pytest.mark.parametrize("is_admin, is_admin_return_expected", [(True, True), (False, False)])
@mock.patch("app.main.crud.get_refresh_token")
@mock.patch("app.main.auth.verify_token")
def test_validate_token(mock_auth_verify_token, mock_crud_get_refresh_token, is_admin, is_admin_return_expected):

    te.setup()

    refreshtoken = get_refresh_token()
    email = get_valid_test_email()

    mock_auth_verify_token.return_value = email, is_admin
    mock_crud_get_refresh_token.return_value = models.RefreshTokens(
        token=refreshtoken)

    email_return, is_admin_return = main.validate_token(
        token=refreshtoken, db=None)

    assert email_return == email
    assert is_admin_return == is_admin_return_expected

    te.teardown()


@mock.patch("app.main.crud.get_refresh_token")
def test_validate_token_not_found(mock_crud_get_refresh_token):

    te.setup()

    refreshtoken = get_refresh_token()

    mock_crud_get_refresh_token.return_value = None

    email_return, is_admin_return = main.validate_token(
        token=refreshtoken, db=None)

    assert email_return == False
    assert is_admin_return == False

    te.teardown()


@mock.patch("app.main.crud.get_refresh_token")
@mock.patch("app.main.auth.verify_token")
def test_validate_token_not_verified(mock_auth_verify_token, mock_crud_get_refresh_token):

    te.setup()

    refreshtoken = get_refresh_token()
    email = get_valid_test_email()

    mock_auth_verify_token.return_value = None, False
    mock_crud_get_refresh_token.return_value = models.RefreshTokens(
        token=refreshtoken)

    email_return, is_admin_return = main.validate_token(refreshtoken, db=None)

    assert email_return == False
    assert is_admin_return == False

    te.teardown()
