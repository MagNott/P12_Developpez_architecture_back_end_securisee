from unittest.mock import patch
from app.controllers.collaborator_controller import CollaboratorController
from app.models.collaborator import Collaborator


def test_signup_success(
        db_session,
        fake_collaborator_info
):
    collaborator_controller = CollaboratorController()

    patch_session = patch(
        "app.controllers.collaborator_controller.Session",
        return_value=db_session
    )
    patch_get_info = patch(
        "app.controllers.collaborator_controller.get_signup_info",
        return_value=fake_collaborator_info,
    )
    patch_render_success = patch(
        "app.controllers.collaborator_controller.show_signup_success"
    )

    with (
        patch_session
        ), (
        patch_get_info
        ), (
        patch_render_success
      ) as mock_show_success:

        collaborator_controller.signup()

    mock_show_success.assert_called_once()


def test_signup_failure(
        db_session,
        fake_collaborator_info_already_exists
):
    collaborator_controller = CollaboratorController()

    patch_session = patch(
        "app.controllers.collaborator_controller.Session",
        return_value=db_session
    )

    patch_get_info = patch(
        "app.controllers.collaborator_controller.get_signup_info",
        return_value=fake_collaborator_info_already_exists
    )
    patch_render_failure = patch(
        "app.controllers.collaborator_controller.show_signup_error"
    )

    with (
        patch_session
    ), (
        patch_get_info
    ), patch_render_failure as mock_show_signup_error:
        collaborator_controller.signup()

    mock_show_signup_error.assert_called_once()


def test_signin_success(
    db_session,
    mock_ask_login,
    mock_ask_password,
):
    collaborator_controller = CollaboratorController()

    patch_session = patch(
        "app.controllers.collaborator_controller.Session",
        return_value=db_session
    )
    patch_signin_success = patch(
        "app.controllers.collaborator_controller.show_signin_success"
    )
    # avoid to write into file system during test
    patch_save_tocken = patch(
        "app.controllers.collaborator_controller.save_token"
    )
    # test database does not contains hashed password so I mock verify_password
    patch_verify_password = patch(
        "app.controllers.collaborator_controller.verify_password",
        return_value=True,
    )

    with (
        patch_session
    ), (
        patch_verify_password
    ), (
        patch_save_tocken
    ) as mock_save_token, patch_signin_success as mock_show_signin_success:

        collaborator_controller.signin()

    mock_show_signin_success.assert_called_once()
    mock_save_token.assert_called_once()


def test_signin_failure_wrong_login(
    db_session,
    mock_ask_login_fail,
    mock_ask_password
):
    collaborator_controller = CollaboratorController()

    patch_session = patch(
        "app.controllers.collaborator_controller.Session",
        return_value=db_session
    )
    patch_render_error = patch(
        "app.controllers.collaborator_controller.show_signin_error"
    )
    with patch_session, patch_render_error as mock_show_signin_error:
        collaborator_controller.signin()

    mock_show_signin_error.assert_called_once()


def test_signin_failure_wrong_password(
    db_session,
    mock_ask_login,
    mock_ask_password,
):
    collaborator_controller = CollaboratorController()

    patch_session = patch(
        "app.controllers.collaborator_controller.Session",
        return_value=db_session
    )

    patch_render_success = patch(
        "app.controllers.collaborator_controller.show_signin_success"
    )
    # test database does not contains hashed password so I mock verify_password
    patch_verify_password = patch(
        "app.controllers.collaborator_controller.verify_password",
        return_value=False,
    )

    with (
        patch_session
    ), (
        patch_verify_password
    ), patch_render_success as mock_render_success:
        collaborator_controller.signin()

    mock_render_success.assert_not_called()


def test_create_collaborator_success(
    db_session,
    fake_collaborators,
    fake_collaborator_info,
):
    collaborator_controller = CollaboratorController()

    patch_session = patch(
        "app.controllers.collaborator_controller.Session",
        return_value=db_session
    )
    authenticated_user = fake_collaborators[0]  # Management department

    patch_get_info = patch(
        "app.controllers.collaborator_controller.get_signup_info",
        return_value=fake_collaborator_info,
    )
    patch_show_success = patch(
        "app.controllers.collaborator_controller.show_signup_success"
    )

    with (
        patch_session
    ), (
        patch_get_info
    ), patch_show_success as mock_show_success:

        collaborator_controller.permission.authenticated_collaborator = \
            authenticated_user
        collaborator_controller.permission.department = \
            authenticated_user.department.name
        collaborator_controller.create_collaborator()

    mock_show_success.assert_called_once()


def test_create_collaborator_failure_no_auth(
    db_session,
):
    # no authenticated user so access should be denied
    collaborator_controller = CollaboratorController()

    patch_session = patch(
        "app.controllers.collaborator_controller.Session",
        return_value=db_session
    )
    patch_render_access_denied = patch(
        "app.controllers.collaborator_controller.render_access_denied"
    )

    with patch_session, patch_render_access_denied as mock_render:
        collaborator_controller.create_collaborator()

    mock_render.assert_called_once()


def test_create_collaborator_failure_wrong_department(
    db_session,
    fake_collaborators,
    fake_collaborator_info,
):
    collaborator_controller = CollaboratorController()

    patch_session = patch(
        "app.controllers.collaborator_controller.Session",
        return_value=db_session
    )
    authenticated_user = fake_collaborators[1]  # Support department

    patch_get_info = patch(
        "app.controllers.collaborator_controller.get_signup_info",
        return_value=fake_collaborator_info,
    )
    patch_render_access_denied = patch(
        "app.controllers.collaborator_controller.render_access_denied"
    )

    with (
        patch_session
    ), (
        patch_get_info
    ), patch_render_access_denied as mock_render_denied:

        collaborator_controller.permission.authenticated_collaborator = \
            authenticated_user
        collaborator_controller.permission.department = \
            authenticated_user.department.name
        collaborator_controller.create_collaborator()

    mock_render_denied.assert_called_once()


def test_modify_collaborator_success(
    db_session,
    fake_collaborators,
    fake_collaborator_info,
):
    collaborator_controller = CollaboratorController()

    patch_session = patch(
        "app.controllers.collaborator_controller.Session",
        return_value=db_session
    )
    authenticated_user = fake_collaborators[0]  # Management department
    patch_choice = patch(
        "app.controllers.collaborator_controller.render_choice_collaborator",
        return_value="1",
    )
    patch_ask_modify = patch(
        "app.controllers.collaborator_controller."
        "ask_collaborator_modification",
        return_value=fake_collaborator_info
    )
    patch_show_success = patch(
        "app.controllers.collaborator_controller.show_signup_success"
    )

    with (
        patch_session
    ), (
        patch_choice
    ), (
        patch_ask_modify
    ), patch_show_success as mock_show_success:
        collaborator_controller.permission.authenticated_collaborator = \
            authenticated_user
        collaborator_controller.permission.department = \
            authenticated_user.department.name
        collaborator_controller.modify_collaborator()
    mock_show_success.assert_called_once()


def test_modify_collaborator_failure_no_auth(
    db_session,
):
    # no authenticated user so access should be denied
    collaborator_controller = CollaboratorController()

    patch_session = patch(
        "app.controllers.collaborator_controller.Session",
        return_value=db_session
    )
    patch_render_access_denied = patch(
        "app.controllers.collaborator_controller.render_access_denied"
    )

    with patch_session, patch_render_access_denied as mock_render:
        collaborator_controller.modify_collaborator()

    mock_render.assert_called_once()


def test_modify_collaborator_failure_wrong_department(
    db_session,
    fake_collaborators,
    fake_collaborator_info,
):
    collaborator_controller = CollaboratorController()

    patch_session = patch(
        "app.controllers.collaborator_controller.Session",
        return_value=db_session
    )
    authenticated_user = fake_collaborators[1]  # Support department
    patch_choice = patch(
        "app.controllers.collaborator_controller.render_choice_collaborator",
        return_value="1",
    )
    patch_ask_modify = patch(
        "app.controllers.collaborator_controller."
        "ask_collaborator_modification",
        return_value=fake_collaborator_info
    )
    patch_render_access_denied = patch(
        "app.controllers.collaborator_controller.render_access_denied"
    )

    with (
        patch_session
    ), (
        patch_choice
    ), (
        patch_ask_modify
    ), patch_render_access_denied as mock_render_denied:

        collaborator_controller.permission.authenticated_collaborator = \
            authenticated_user
        collaborator_controller.permission.department = \
            authenticated_user.department.name
        collaborator_controller.modify_collaborator()

    mock_render_denied.assert_called_once()


def test_delete_collaborator_success(
    db_session,
    fake_collaborators,
):
    collaborator_controller = CollaboratorController()

    authenticated_user = fake_collaborators[0]  # Management department

    patch_session = patch(
        "app.controllers.collaborator_controller.Session",
        return_value=db_session
    )
    patch_choice = patch(
        "app.controllers.collaborator_controller.render_choice_collaborator",
        return_value=f"{fake_collaborators[1].id}: Defrance Bob",
    )
    patch_confirm = patch(
        "app.controllers.collaborator_controller.ask_confirm_delete",
        return_value=True  # Confirmer la suppression
    )

    with (
        patch_session
    ), patch_choice, patch_confirm:

        collaborator_controller.permission.authenticated_collaborator = \
            authenticated_user
        collaborator_controller.authenticated_collaborator = authenticated_user
        collaborator_controller.permission.department = \
            authenticated_user.department.name
        collaborator_controller.delete_collaborator()

    assert db_session.query(Collaborator).filter_by(
        login=fake_collaborators[1].login
    ).first() is None


def test_delete_collaborator_forbidden_self_deletion(
    db_session,
    fake_collaborators,
):
    collaborator_controller = CollaboratorController()

    authenticated_user = fake_collaborators[0]  # Management department

    patch_session = patch(
        "app.controllers.collaborator_controller.Session",
        return_value=db_session
    )
    patch_choice = patch(
        "app.controllers.collaborator_controller.render_choice_collaborator",
        return_value=f"{fake_collaborators[0].id}: Alice Martin",
    )
    patch_show_cannot_delete_self = patch(
        "app.controllers.collaborator_controller.show_cannot_delete_self"
    )

    with (
        patch_session
    ), (
        patch_choice
    ), patch_show_cannot_delete_self as mock_show_cannot_delete_self:

        collaborator_controller.permission.authenticated_collaborator = \
            authenticated_user
        collaborator_controller.authenticated_collaborator = authenticated_user
        collaborator_controller.permission.department = \
            authenticated_user.department.name
        collaborator_controller.delete_collaborator()

    mock_show_cannot_delete_self.assert_called_once()


def test_delete_collaborator_failure_no_auth(
    db_session,
):
    # no authenticated user so access should be denied
    collaborator_controller = CollaboratorController()

    patch_session = patch(
        "app.controllers.collaborator_controller.Session",
        return_value=db_session
    )
    patch_render_access_denied = patch(
        "app.controllers.collaborator_controller.render_access_denied"
    )

    with patch_session, patch_render_access_denied as mock_render:
        collaborator_controller.delete_collaborator()

    mock_render.assert_called_once()


def test_delete_collaborator_failure_wrong_department(
    db_session,
    fake_collaborators,
):
    collaborator_controller = CollaboratorController()

    patch_session = patch(
        "app.controllers.collaborator_controller.Session",
        return_value=db_session
    )
    authenticated_user = fake_collaborators[1]  # Support department
    patch_choice = patch(
        "app.controllers.collaborator_controller.render_choice_collaborator",
        return_value="1: Alice Martin",
    )
    patch_render_access_denied = patch(
        "app.controllers.collaborator_controller.render_access_denied"
    )

    with (
        patch_session
    ), (
        patch_choice
    ), patch_render_access_denied as mock_render_denied:

        collaborator_controller.permission.authenticated_collaborator = \
            authenticated_user
        collaborator_controller.permission.department = \
            authenticated_user.department.name
        collaborator_controller.delete_collaborator()

    mock_render_denied.assert_called_once()
