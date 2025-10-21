from unittest.mock import patch
from app.controllers.customer_controller import CustomerController


def test_view_customers_success(
    mock_session,
    fake_customers,
):
    customer_controller = CustomerController()

    mock_session.query.return_value.all.return_value = fake_customers

    patch_can_read = patch.object(
        customer_controller.permission, "can_read", return_value=True
    )
    patch_session = patch(
        "app.controllers.customer_controller.Session", return_value=mock_session
    )
    patch_render = patch(
        "app.controllers.customer_controller.render_view_all_customers"
    )

    with patch_can_read, patch_session, patch_render as mock_render:
        customer_controller.view_customers()

    mock_render.assert_called_once_with(fake_customers)


def test_create_customer_success(
    mock_session,
    customer_controller,
    fake_customer_info,
):

    patch_can_create = patch.object(
        customer_controller.permission, "can_create_customer",
        return_value=True
    )

    patch_session = patch(
        "app.controllers.customer_controller.Session",
        return_value=mock_session
    )
    patch_get_info = patch(
        "app.controllers.customer_controller.get_customer_info",
        return_value=fake_customer_info,
    )
    patch_commit = patch(
        "app.controllers.customer_controller.commit_to_db", return_value=True
    )
    patch_render_success = patch(
        "app.controllers.customer_controller.show_created_customer_success"
    )

    with (
        patch_can_create
    ), (
        patch_session
    ), (
        patch_get_info
    ), patch_commit as mock_commit, patch_render_success as mock_render_success:

        customer_controller.create_customer()

    mock_render_success.assert_called_once()
    mock_commit.assert_called_once()


def test_read_customer_success(
    mock_session,
    customer_controller,
    fake_customers,
):
    patch_can_read = patch.object(
        customer_controller.permission, "can_read", return_value=True
    )

    patch_session = patch(
        "app.controllers.customer_controller.Session",
        return_value=mock_session
    )
    patch_render_choice = patch(
        "app.controllers.customer_controller.render_choice_customer",
        return_value="1: Jean Durand",
    )

    patch_render_read = patch(
        "app.controllers.customer_controller.render_read_customer"
    )

    mock_session.query.return_value.filter.return_value.first.return_value = (
        fake_customers[0]
    )

    with (
        patch_can_read
    ), (
        patch_session
    ), patch_render_choice as mock_render_choice, patch_render_read as mock_render_read:
        customer_controller.read_customer()

    mock_render_read.assert_called_once_with(fake_customers[0])
    mock_render_choice.assert_called_once()


def test_modify_customer_success(
    mock_session,
    customer_controller,
    fake_customers,
    fake_collaborators,
    fake_customer_info,
):
    patch_can_modify = patch.object(
        customer_controller.permission, "can_modify_customer",
        return_value=True
    )

    patch_session = patch(
        "app.controllers.customer_controller.Session",
        return_value=mock_session
    )
    patch_render_choice = patch(
        "app.controllers.customer_controller.render_choice_customer",
        return_value="1: Jean Durand",
    )

    patch_get_info = patch(
        "app.controllers.customer_controller.ask_customer_modification",
        return_value=fake_customer_info,
    )

    patch_commit = patch(
        "app.controllers.customer_controller.commit_to_db", return_value=True
    )

    mock_session.query.return_value.filter.return_value.first.side_effect = [
        fake_customers[0],
        fake_collaborators[2],
    ]

    with (
        patch_can_modify
    ), (
        patch_session
    ), patch_render_choice as mock_render_choice, (
        patch_get_info
    ), patch_commit as mock_commit:
        customer_controller.modify_customer()

    mock_render_choice.assert_called_once()
    mock_commit.assert_called_once()
