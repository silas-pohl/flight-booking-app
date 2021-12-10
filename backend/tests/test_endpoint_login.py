from unittest import mock

import pytest
import tests.test_entities as te
from app import auth


@ mock.patch("app.main.auth.create_access_token")
@ mock.patch("app.main.auth.create_refresh_token")
@ mock.patch("app.main.auth.authenticate_user")
def test_login_valid_login(mock_auth_authenticate_user, mock_auth_create_refresh_token, mock_auth_create_access_token):
    mock_auth_authenticate_user.return_value = te.get_test_user()
    mock_auth_create_refresh_token.return_value = te.get_refresh_token()
    mock_auth_create_access_token.return_value = te.get_access_token()

    refresh_token = te.get_refresh_token()
    access_token = te.get_access_token()
    refresh_token = te.get_refresh_token()
    valid_username = te.get_valid_test_email()
    valid_password = te.get_valid_password()

    response_login = te.client.post(
        "/login", json={"email": valid_username, "password": valid_password
                        })

    assert response_login.status_code == 200
    assert response_login.json() == {
        "access_token": access_token, "token_type": "bearer", "expires_in": auth.ACCESS_TOKEN_EXPIRE_MINUTES*60*1000}
    assert response_login.cookies.get_dict(
    ) == {"refresh_token": refresh_token}


@ mock.patch("app.main.auth.authenticate_user")
def test_login_non_matching_credentials(mock_auth_authenticate_user):
    mock_auth_authenticate_user.return_value = None

    valid_username = te.get_valid_test_email()
    valid_password = te.get_valid_password()

    response_login = te.client.post(
        "/login", json={"email": valid_username, "password": valid_password
                        })

    assert response_login.status_code == 401
    assert response_login.headers["WWW-Authenticate"] == "Bearer"
    assert response_login.json() == {
        "detail": "Incorrect email or password"}
