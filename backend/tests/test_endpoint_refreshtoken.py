from unittest import mock

from app import auth
import tests.test_entities as te


@mock.patch("app.main.validate_token")
@mock.patch("app.main.auth.create_access_token")
@mock.patch("app.main.auth.create_refresh_token")
@mock.patch("app.main.crud.delete_refresh_token")
def test_refresh_token(mock_crud_delete_refresh_token, mock_auth_create_refresh_token, mock_auth_create_access_token, mock_validate_token):

    te.setup()

    refresh_token = te.get_refresh_token()
    access_token = te.get_access_token()

    mock_crud_delete_refresh_token.return_value = None
    mock_auth_create_refresh_token.return_value = refresh_token
    mock_auth_create_access_token.return_value = access_token
    mock_validate_token.return_value = (te.get_valid_test_email, False)

    cookies = {"refresh_token": refresh_token}

    response_refresh_token = te.client.get("/refreshtoken", cookies=cookies)

    assert response_refresh_token.status_code == 200
    assert response_refresh_token.json() == {"access_token": access_token,
                                             "token_type": "bearer",
                                             "expires_in": auth.ACCESS_TOKEN_EXPIRE_MINUTES*60*1000}
    assert response_refresh_token.cookies.get_dict(
    ) == {"refresh_token": refresh_token}

    te.teardown()


@mock.patch("app.main.validate_token")
def test_refresh_token_invalid_refresh_token(mock_validate_token):

    te.setup()

    mock_validate_token.return_value = (False, False)

    refresh_token = te.get_refresh_token()
    cookies = {"refresh_token": refresh_token}

    response_refresh_token = te.client.get("/refreshtoken", cookies=cookies)

    assert response_refresh_token.status_code == 401
    assert response_refresh_token.headers["WWW-Authenticate"] == "Bearer"
    assert response_refresh_token.json() == {"detail": "Invalid refresh token"}

    te.teardown()
