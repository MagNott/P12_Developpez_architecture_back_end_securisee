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
    ) as mock_show_success, patch(
        "app.controllers.collaborator_controller.show_signup_error"
    ) as mock_show_error, patch("app.utils.database_utils.SessionLocal",
                                return_value=mock_session):
        collaborator_controller.signup()

    mock_show_success.assert_not_called()
    mock_show_error.assert_called_once()
