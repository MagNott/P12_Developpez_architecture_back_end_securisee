from unittest.mock import patch
from app.controllers.customer_controller import CustomerController


def test_view_customers_success(
    db_session,
    fake_collaborators,
    fake_customers
):
    customer_controller = CustomerController()

    patch_session = patch(
        "app.controllers.customer_controller.Session",
        return_value=db_session
    )

    authenticated_user = fake_collaborators[2]  # Sales department

    patch_render = patch(
        "app.controllers.customer_controller.render_view_all_customers"
    )

    with patch_session, patch_render as mock_render:

        customer_controller.permission.authenticated_collaborator = \
            authenticated_user
        customer_controller.authenticated_collaborator = authenticated_user
        customer_controller.permission.department = \
            authenticated_user.department.name
        customer_controller.view_customers()

    mock_render.assert_called_once_with(fake_customers, authenticated_user)


def test_view_customers_access_denied(
    db_session,
):
    # no authenticated user so access should be denied
    customer_controller = CustomerController()

    patch_session = patch(
        "app.controllers.customer_controller.Session",
        return_value=db_session
    )
    patch_render = patch(
        "app.controllers.customer_controller.render_access_denied"
    )

    with patch_session, patch_render as mock_render:

        customer_controller.view_customers()

    mock_render.assert_called_once()


def test_create_customer_success(
    db_session,
    customer_controller,
    fake_customer_info,
    fake_collaborators,
):
    customer_controller = CustomerController()

    patch_session = patch(
        "app.controllers.customer_controller.Session",
        return_value=db_session
    )

    authenticated_user = fake_collaborators[2]  # Sales department

    patch_get_info = patch(
        "app.controllers.customer_controller.get_customer_info",
        return_value=fake_customer_info,
    )
    patch_render_success = patch(
        "app.controllers.customer_controller.show_created_customer_success"
    )

    with (
        patch_session
    ), (
        patch_get_info
    ), patch_render_success as mock_render_success:

        customer_controller.permission.authenticated_collaborator = \
            authenticated_user
        customer_controller.authenticated_collaborator = authenticated_user
        customer_controller.permission.department = \
            authenticated_user.department.name
        customer_controller.create_customer()

    mock_render_success.assert_called_once()


def test_create_customer_failure_no_auth(
    db_session,
):
    # no authenticated user so access should be denied
    customer_controller = CustomerController()

    patch_session = patch(
        "app.controllers.customer_controller.Session",
        return_value=db_session
    )
    patch_render_access_denied = patch(
        "app.controllers.customer_controller.render_access_denied"
    )

    with (
        patch_session
    ), patch_render_access_denied as mock_render_access_denied:

        customer_controller.create_customer()

    mock_render_access_denied.assert_called_once()


def test_create_customer_failure_is_not_sales(
    db_session,
    fake_collaborators,
):
    customer_controller = CustomerController()

    patch_session = patch(
        "app.controllers.customer_controller.Session",
        return_value=db_session
    )
    authenticated_user = fake_collaborators[0]  # Management department

    patch_render_access_denied = patch(
        "app.controllers.customer_controller.render_access_denied"
    )

    with (
        patch_session
    ), patch_render_access_denied as mock_render_access_denied:

        customer_controller.permission.authenticated_collaborator = \
            authenticated_user
        customer_controller.permission.department = \
            authenticated_user.department.name
        customer_controller.create_customer()

    mock_render_access_denied.assert_called_once()


def test_read_customer_success(
    db_session,
    fake_collaborators,
    fake_customers,
):
    customer_controller = CustomerController()

    authenticated_user = fake_collaborators[0]  # Management department

    patch_session = patch(
        "app.controllers.customer_controller.Session",
        return_value=db_session
    )
    patch_render_choice = patch(
        "app.controllers.customer_controller.render_choice_customer",
        return_value="1: Jean Durand",
    )

    patch_render_read = patch(
        "app.controllers.customer_controller.render_read_customer"
    )

    with (
        patch_session
    ), patch_render_choice, patch_render_read as mock_render_read:

        customer_controller.permission.authenticated_collaborator = \
            authenticated_user
        customer_controller.authenticated_collaborator = authenticated_user
        customer_controller.permission.department = \
            authenticated_user.department.name
        customer_controller.read_customer()

    mock_render_read.assert_called_once_with(
        fake_customers[0],
        authenticated_user
    )


def test_read_customer_failure_no_auth(
    db_session,
):
    # no authenticated user so access should be denied
    customer_controller = CustomerController()

    patch_session = patch(
        "app.controllers.customer_controller.Session",
        return_value=db_session
    )
    patch_render_access_denied = patch(
        "app.controllers.customer_controller.render_access_denied"
    )

    with (
        patch_session
    ), patch_render_access_denied as mock_render_access_denied:

        customer_controller.read_customer()

    mock_render_access_denied.assert_called_once()


def test_modify_customer_success(
    db_session,
    fake_collaborators,
    fake_customer_info,
):
    customer_controller = CustomerController()

    authenticated_user = fake_collaborators[2]  # Sales department

    patch_session = patch(
        "app.controllers.customer_controller.Session",
        return_value=db_session
    )
    patch_render_choice = patch(
        "app.controllers.customer_controller.render_choice_customer",
        return_value="1: Jean Durand",
    )

    patch_get_info = patch(
        "app.controllers.customer_controller.ask_customer_modification",
        return_value=fake_customer_info,
    )

    with (
        patch_session
    ), (
        patch_get_info
    ), patch_render_choice as mock_render_choice:

        customer_controller.permission.authenticated_collaborator = \
            authenticated_user
        customer_controller.authenticated_collaborator = authenticated_user
        customer_controller.permission.department = \
            authenticated_user.department.name
        customer_controller.modify_customer()

    mock_render_choice.assert_called_once()


def test_modify_customer_failure_no_auth(
    db_session,
):
    # no authenticated user so access should be denied
    customer_controller = CustomerController()

    patch_session = patch(
        "app.controllers.customer_controller.Session",
        return_value=db_session
    )
    patch_render_access_denied = patch(
        "app.controllers.customer_controller.render_access_denied"
    )

    with (
        patch_session
    ), patch_render_access_denied as mock_render_access_denied:

        customer_controller.modify_customer()

    mock_render_access_denied.assert_called_once()


def test_modify_customer_failure_not_sales(
    db_session,
    fake_collaborators,
):
    customer_controller = CustomerController()

    authenticated_user = fake_collaborators[0]  # Management department

    patch_session = patch(
        "app.controllers.customer_controller.Session",
        return_value=db_session
    )
    patch_render_access_denied = patch(
        "app.controllers.customer_controller.render_access_denied"
    )

    with (
        patch_session
    ), patch_render_access_denied as mock_render_access_denied:

        customer_controller.permission.authenticated_collaborator = \
            authenticated_user
        customer_controller.permission.department = \
            authenticated_user.department.name
        customer_controller.modify_customer()

    mock_render_access_denied.assert_called_once()


def test_modify_customer_failure_not_owner(
    db_session,
    fake_collaborators,
):
    customer_controller = CustomerController()

    authenticated_user = fake_collaborators[3]  # Sales department

    patch_session = patch(
        "app.controllers.customer_controller.Session",
        return_value=db_session
    )
    patch_render_choice = patch(
        "app.controllers.customer_controller.render_choice_customer",
        return_value="1: Jean Durand",
    )
    patch_render_access_denied = patch(
        "app.controllers.customer_controller.render_access_denied"
    )

    with (
        patch_session
    ), (
        patch_render_choice
    ), patch_render_access_denied as mock_render_access_denied:

        customer_controller.permission.authenticated_collaborator = \
            authenticated_user
        customer_controller.authenticated_collaborator = authenticated_user
        customer_controller.permission.department = \
            authenticated_user.department.name
        customer_controller.modify_customer()

    mock_render_access_denied.assert_called_once()
