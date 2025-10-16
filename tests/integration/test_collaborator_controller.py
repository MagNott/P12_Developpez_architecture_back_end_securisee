from unittest.mock import patch
from app.controllers import collaborator_controller


def test_signup_success(mock_session, mock_get_signup_info, fake_user_info):

    with patch(
        "app.controllers.collaborator_controller.show_signup_success"
    ) as mock_show_success, patch(
        "app.controllers.collaborator_controller.show_signup_error"
    ) as mock_show_error:
        collaborator_controller.signup()

    mock_show_success.assert_called_once()
    mock_show_error.assert_not_called()


def test_signup_failure(mock_session, mock_get_signup_info, fake_user_info):
    mock_session.commit.side_effect = Exception("DB Error")

    with patch(
        "app.controllers.collaborator_controller.show_signup_success"
    ) as mock_show_signup_success, patch(
        "app.controllers.collaborator_controller.show_signup_error"
    ) as mock_show_signup_error, patch(
        "app.utils.database_utils.SessionLocal", return_value=mock_session
    ):
        collaborator_controller.signup()

    mock_show_signup_success.assert_not_called()
    mock_show_signup_error.assert_called_once()


def test_signin_success(
    mock_session,
    mock_query,
    mock_ask_login,
    mock_ask_password,
    fake_collaborator,
    mock_department_menu,
):

    with patch(
        "app.controllers.collaborator_controller.show_signin_success"
    ) as mock_show_signin_success, patch(
        "app.controllers.collaborator_controller.show_signin_error"
    ) as mock_show_signin_error, patch(
        "app.controllers.collaborator_controller.save_token"
    ) as mock_save_token, patch(
        "app.controllers.collaborator_controller.verify_password",
        return_value=True,
    ):
        collaborator_controller.signin()

    mock_show_signin_success.assert_called_once()
    mock_show_signin_error.assert_not_called()
    mock_save_token.assert_called_once()


def test_signin_failure_wrong_login(
    mock_session, mock_ask_login, mock_ask_password
):

    with patch(
        "app.controllers.collaborator_controller.find_collaborator_by_login",
        return_value=None,
    ), patch(
        "app.controllers.collaborator_controller.show_signin_success"
    ) as mock_show_signin_success, patch(
        "app.controllers.collaborator_controller.show_signin_error"
    ) as mock_show_signin_error, patch(
        "app.controllers.collaborator_controller.verify_password"
    ):
        collaborator_controller.signin()

    mock_show_signin_success.assert_not_called()
    mock_show_signin_error.assert_called_once()


def test_signin_failure_wrong_password(
    mock_session,
    mock_query,
    mock_ask_login,
    mock_ask_password,
    fake_collaborator,
):

    with patch(
        "app.controllers.collaborator_controller.show_signin_success"
    ) as mock_show_signin_success, patch(
        "app.controllers.collaborator_controller.show_signin_error"
    ) as mock_show_signin_error, patch(
        "app.controllers.collaborator_controller.verify_password",
        return_value=False,
    ):
        collaborator_controller.signin()

    mock_show_signin_success.assert_not_called()
    mock_show_signin_error.assert_called_once()
