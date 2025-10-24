from unittest.mock import patch


def test_signup_success(
        collaborator_controller,
        mock_session,
        mock_get_signup_info,
        fake_collaborator_info
):

    with patch("app.controllers.collaborator_controller.Session",
               return_value=mock_session), \
        patch(
        "app.controllers.collaborator_controller.show_signup_success"
    ) as mock_show_success, patch(
        "app.controllers.collaborator_controller.show_signup_error"
    ) as mock_show_error:
        collaborator_controller.signup()

    mock_show_success.assert_called_once()
    mock_show_error.assert_not_called()


def test_signup_failure(mock_session,
                        collaborator_controller,
                        mock_get_signup_info,
                        fake_collaborator_info):
    mock_session.commit.side_effect = Exception("DB Error")

    with patch("app.controllers.collaborator_controller.Session",
               return_value=mock_session), \
        patch(
        "app.controllers.collaborator_controller.show_signup_success"
    ) as mock_show_signup_success, patch(
        "app.controllers.collaborator_controller.show_signup_error"
    ) as mock_show_signup_error:
        collaborator_controller.signup()

    mock_show_signup_success.assert_not_called()
    mock_show_signup_error.assert_called_once()


def test_signin_success(
    collaborator_controller,
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
    collaborator_controller, mock_session, mock_ask_login, mock_ask_password
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
    collaborator_controller,
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


def test_create_collaborator_success(
    collaborator_controller,
    mock_session,
    mock_query,
    mock_get_signup_info,
):

    patch_session = patch(
        "app.controllers.collaborator_controller.Session",
        return_value=mock_session
    )

    patch_choice = patch(
        "app.controllers.collaborator_controller.render_choice_collaborator",
        return_value="1",
    )
    patch_commit = patch(
        "app.controllers.collaborator_controller.commit_to_db", return_value=True
    )
    patch_show_success = patch(
        "app.controllers.collaborator_controller.show_signup_success"
    )
    patch_show_error = patch(
        "app.controllers.collaborator_controller.show_signup_error"
    )

    with patch_session, patch_choice, patch_commit, \
         patch_show_success as mock_show_success, patch_show_error as mock_show_error:
        collaborator_controller.create_collaborator()

    mock_show_error.assert_not_called()


def test_modify_collaborator_success(
    collaborator_controller,
    mock_session,
    mock_query,
    fake_collaborator_info,
):

    patch_session = patch(
        "app.controllers.collaborator_controller.Session",
        return_value=mock_session
    )

    patch_choice = patch(
        "app.controllers.collaborator_controller.render_choice_collaborator",
        return_value="1",
    )
    patch_ask_modify = patch(
        "app.controllers.collaborator_controller.ask_collaborator_modification",
        return_value=fake_collaborator_info
    )
    patch_commit = patch(
        "app.controllers.collaborator_controller.commit_to_db",
        return_value=True
    )
    patch_show_success = patch(
        "app.controllers.collaborator_controller.show_signup_success"
    )
    patch_show_error = patch(
        "app.controllers.collaborator_controller.show_signup_error"
    )

    with patch_session, patch_choice, patch_commit, patch_ask_modify, \
         patch_show_success as mock_show_success, patch_show_error as mock_show_error:
        collaborator_controller.modify_collaborator()
    mock_show_error.assert_not_called()


def test_delete_collaborator_success(
    collaborator_controller,
    mock_session,
    mock_query,
    mock_is_authenticated_management,
    fake_collaborator,
    fake_collaborator_to_delete,
):

    patch_session = patch(
        "app.controllers.collaborator_controller.Session",
        return_value=mock_session
    )
    patch_choice = patch(
        "app.controllers.collaborator_controller.render_choice_collaborator",
        return_value=f"{fake_collaborator_to_delete.id}: Dupont Jean",
    )
    patch_show_success = patch(
        "app.controllers.collaborator_controller.show_signup_success"
    )
    patch_show_error = patch(
        "app.controllers.collaborator_controller.show_signup_error"
    )

    mock_session.query().filter().first.return_value = fake_collaborator_to_delete

    with patch_session, patch_choice, \
         patch_show_success as mock_show_success, patch_show_error as mock_show_error:
        collaborator_controller.delete_collaborator()

    mock_show_error.assert_not_called()
