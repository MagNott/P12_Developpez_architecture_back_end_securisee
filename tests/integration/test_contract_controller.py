from unittest.mock import patch


def test_view_contract_success(
    mock_session,
    contract_controller,
    fake_contracts,
):

    mock_session.query.return_value.all.return_value = fake_contracts

    patch_can_read = patch.object(
        contract_controller.permission, "can_read", return_value=True
    )
    patch_session = patch(
        "app.controllers.contract_controller.Session",
        return_value=mock_session
    )
    patch_render = patch(
        "app.controllers.contract_controller.render_view_all_contracts"
    )

    with patch_can_read, patch_session, patch_render as mock_render:
        contract_controller.view_contracts()

    mock_render.assert_called_once_with(fake_contracts)
    mock_session.query.assert_called_once()


def test_create_contract_success(
    mock_session,
    contract_controller,
    fake_contract_info,
):

    patch_can_create = patch.object(
        contract_controller.permission, "can_create_contract",
        return_value=True
    )

    patch_session = patch(
        "app.controllers.contract_controller.Session",
        return_value=mock_session
    )
    patch_get_info = patch(
        "app.controllers.contract_controller.get_contract_info",
        return_value=fake_contract_info,
    )
    patch_choice_customer = patch(
        "app.controllers.contract_controller.render_choice_customer",
        return_value="1: Jean Durand"
    )

    patch_commit = patch(
        "app.controllers.contract_controller.commit_to_db", return_value=True
    )
    patch_render_success = patch(
        "app.controllers.contract_controller.show_created_contract_success"
    )

    with (
        patch_can_create
    ), (
        patch_session
    ), (
        patch_get_info
    ), (patch_choice_customer
    ), patch_commit as mock_commit, patch_render_success as mock_render_success:
        contract_controller.create_contract()

    mock_commit.assert_called_once()
    mock_render_success.assert_called_once()


def test_read_contract_success(
    mock_session,
    contract_controller,
    fake_contracts,
):
    patch_can_read = patch.object(
        contract_controller.permission, "can_read", return_value=True
    )

    patch_session = patch(
        "app.controllers.contract_controller.Session",
        return_value=mock_session
    )
    patch_render_choice = patch(
        "app.controllers.contract_controller.render_choice_contract",
        return_value="1: Contract for Jean Durand",
    )
    patch_render = patch(
        "app.controllers.contract_controller.render_read_contract"
    )

    mock_session.query.return_value.filter.return_value.first.return_value = (
        fake_contracts[0]
    )

    with (
        patch_can_read
    ), (
        patch_session
    ), (
        patch_render_choice
    ), patch_render as mock_render:

        contract_controller.read_contract()

    mock_render.assert_called_once_with(fake_contracts[0])


def test_modify_contract_success(
    mock_session,
    contract_controller,
    fake_contracts,
    fake_contract_info,
):
    patch_can_modify = patch.object(
        contract_controller.permission, "can_modify_contract",
        return_value=True
    )

    patch_session = patch(
        "app.controllers.contract_controller.Session",
        return_value=mock_session
    )
    patch_render_choice = patch(
        "app.controllers.contract_controller.render_choice_contract",
        return_value="1: Contract for Jean Durand",
    )
    patch_ask_contract_modification = patch(
        "app.controllers.contract_controller.ask_contract_modification",
        return_value=fake_contract_info
    )
    patch_commit = patch(
        "app.controllers.contract_controller.commit_to_db", return_value=True
    )
    patch_render_success = patch(
        "app.controllers.contract_controller.show_modified_contract_success"
    )

    mock_session.query.return_value.filter.return_value.first.return_value = (
        fake_contracts[0]
    )

    with (
        patch_can_modify
    ), (
        patch_session
    ), (
        patch_render_choice
    ), (
        patch_ask_contract_modification
    ), patch_commit as mock_commit, patch_render_success as mock_render_success:

        contract_controller.modify_contract()

    mock_commit.assert_called_once()
    mock_render_success.assert_called_once()
