from unittest.mock import patch
from app.controllers.contract_controller import ContractController


def test_view_contract_success(
    mock_file,
    db_session,
    fake_contracts,
    fake_collaborators,
):
    contract_controller = ContractController()

    authenticated_user = fake_collaborators[2]  # Sales department

    patch_session = patch(
        "app.controllers.contract_controller.Session",
        return_value=db_session
    )
    patch_render = patch(
        "app.controllers.contract_controller.render_view_all_contracts"
    )

    with patch_session, patch_render as mock_render:

        contract_controller.permission.authenticated_collaborator = \
            authenticated_user
        contract_controller.authenticated_collaborator = authenticated_user
        contract_controller.permission.department = \
            authenticated_user.department.name
        contract_controller.view_contracts()

    mock_render.assert_called_once_with(fake_contracts, authenticated_user)


def test_view_contract_access_denied(
    mock_file,
    db_session,
):
    # no authenticated user so access should be denied
    contract_controller = ContractController()

    patch_session = patch(
        "app.controllers.contract_controller.Session",
        return_value=db_session
    )
    patch_render = patch(
        "app.controllers.contract_controller.render_access_denied"
    )

    with patch_session, patch_render as mock_render:

        contract_controller.view_contracts()

    mock_render.assert_called_once()


def test_create_contract_success(
    mock_file,
    db_session,
    fake_contract_info,
    fake_collaborators
):
    contract_controller = ContractController()
    authenticated_user = fake_collaborators[0]  # Management department

    patch_session = patch(
        "app.controllers.contract_controller.Session",
        return_value=db_session
    )
    patch_get_info = patch(
        "app.controllers.contract_controller.get_contract_info",
        return_value=fake_contract_info,
    )
    patch_choice_customer = patch(
        "app.controllers.contract_controller.render_choice_customer",
        return_value="1: Jean Durand"
    )

    patch_render_success = patch(
        "app.controllers.contract_controller.show_created_contract_success"
    )

    with (
        patch_session
    ), (
        patch_get_info
    ), (
        patch_choice_customer
    ), patch_render_success as mock_render_success:

        contract_controller.permission.authenticated_collaborator = \
            authenticated_user
        contract_controller.permission.department = \
            authenticated_user.department.name
        contract_controller.create_contract()

    mock_render_success.assert_called_once()


def test_create_contract_failure_no_auth(
    mock_file,
    db_session,
):
    # no authenticated user so access should be denied
    contract_controller = ContractController()

    patch_session = patch(
        "app.controllers.contract_controller.Session",
        return_value=db_session
    )
    patch_render_access_denied = patch(
        "app.controllers.contract_controller.render_access_denied"
    )

    with (
        patch_session
    ), patch_render_access_denied as mock_render_access_denied:

        contract_controller.create_contract()

    mock_render_access_denied.assert_called_once()


def test_create_contract_failure_is_not_management(
    mock_file,
    db_session,
    fake_collaborators
):
    contract_controller = ContractController()

    patch_session = patch(
        "app.controllers.contract_controller.Session",
        return_value=db_session
    )
    authenticated_user = fake_collaborators[1]  # Support department

    patch_render_access_denied = patch(
        "app.controllers.contract_controller.render_access_denied"
    )

    with (
        patch_session
    ), patch_render_access_denied as mock_render_access_denied:

        contract_controller.permission.authenticated_collaborator = \
            authenticated_user
        contract_controller.permission.department = \
            authenticated_user.department.name
        contract_controller.create_contract()

    mock_render_access_denied.assert_called_once()


def test_read_contract_success(
    mock_file,
    db_session,
    fake_contracts,
    fake_collaborators,
):
    contract_controller = ContractController()

    patch_session = patch(
        "app.controllers.contract_controller.Session",
        return_value=db_session
    )

    authenticated_user = fake_collaborators[2]  # Sales department

    patch_render_choice = patch(
        "app.controllers.contract_controller.render_choice_contract",
        return_value="1: Contract for Jean Durand",
    )
    patch_render = patch(
        "app.controllers.contract_controller.render_read_contract"
    )

    with (
        patch_session
    ), (
        patch_render_choice
    ), patch_render as mock_render:

        contract_controller.permission.authenticated_collaborator = \
            authenticated_user
        contract_controller.authenticated_collaborator = authenticated_user
        contract_controller.permission.department = \
            authenticated_user.department.name
        contract_controller.read_contract()

    mock_render.assert_called_once_with(fake_contracts[0], authenticated_user)


def test_read_contract_failure_no_auth(
    mock_file,
    db_session,
):
    # no authenticated user so access should be denied
    contract_controller = ContractController()

    patch_session = patch(
        "app.controllers.contract_controller.Session",
        return_value=db_session
    )
    patch_render_access_denied = patch(
        "app.controllers.contract_controller.render_access_denied"
    )

    with (
        patch_session
    ), patch_render_access_denied as mock_render_access_denied:

        contract_controller.read_contract()

    mock_render_access_denied.assert_called_once()


def test_modify_contract_success(
    mock_file,
    db_session,
    fake_contract_info,
    fake_collaborators,
):
    contract_controller = ContractController()

    patch_session = patch(
        "app.controllers.contract_controller.Session",
        return_value=db_session
    )
    authenticated_user = fake_collaborators[2]  # Sales department
    patch_render_choice = patch(
        "app.controllers.contract_controller.render_choice_contract",
        return_value="1: Contract for Jean Durand",
    )
    patch_ask_contract_modification = patch(
        "app.controllers.contract_controller.ask_contract_modification",
        return_value=fake_contract_info
    )

    patch_render_success = patch(
        "app.controllers.contract_controller.show_modified_contract_success"
    )

    with (
        patch_render_choice
    ), (
        patch_session
    ), (
        patch_ask_contract_modification
    ), patch_render_success as mock_render_success:

        contract_controller.permission.authenticated_collaborator = \
            authenticated_user
        contract_controller.authenticated_collaborator = authenticated_user
        contract_controller.permission.department = \
            authenticated_user.department.name
        contract_controller.modify_contract()

    mock_render_success.assert_called_once()


def test_modify_contract_failure_is_not_dedicated_sales(
    mock_file,
    db_session,
    fake_contract_info,
    fake_collaborators,
):
    contract_controller = ContractController()

    patch_session = patch(
        "app.controllers.contract_controller.Session",
        return_value=db_session
    )

    authenticated_user = fake_collaborators[1]  # Support department

    patch_render_choice = patch(
        "app.controllers.contract_controller.render_choice_contract",
        return_value="1: Contract for Jean Durand",
    )
    patch_ask_contract_modification = patch(
        "app.controllers.contract_controller.ask_contract_modification",
        return_value=fake_contract_info
    )
    patch_render_success = patch(
        "app.controllers.contract_controller.render_access_denied"
    )

    with (
        patch_render_choice
    ), (
        patch_session
    ), (
        patch_ask_contract_modification
    ), patch_render_success as mock_render_success:

        contract_controller.permission.authenticated_collaborator = \
            authenticated_user
        contract_controller.permission.department = \
            authenticated_user.department.name
        contract_controller.modify_contract()

    mock_render_success.assert_called_once()


def test_modify_contract_failure_no_auth(
    mock_file,
    db_session,
    fake_contract_info,
):
    # no authenticated user so access should be denied
    contract_controller = ContractController()

    patch_session = patch(
        "app.controllers.contract_controller.Session",
        return_value=db_session
    )
    patch_render_choice = patch(
        "app.controllers.contract_controller.render_choice_contract",
        return_value="1: Contract for Jean Durand",
    )
    patch_ask_contract_modification = patch(
        "app.controllers.contract_controller.ask_contract_modification",
        return_value=fake_contract_info
    )
    patch_render_error = patch(
        "app.controllers.contract_controller.render_access_denied"
    )

    with (
        patch_render_choice
    ), (
        patch_session
    ), (
        patch_ask_contract_modification
    ), patch_render_error as mock_render_error:

        contract_controller.modify_contract()

    mock_render_error.assert_called_once()


def test_filter_contracts_by_status_unsigned_success(
    mock_file,
    db_session,
    fake_contracts,
    fake_collaborators,
):
    contract_controller = ContractController()

    patch_session = patch(
        "app.controllers.contract_controller.Session",
        return_value=db_session
    )

    authenticated_user = fake_collaborators[2]  # Sales department

    patch_render_choice_status = patch(
        "app.controllers.contract_controller.render_choice_status_contracts",
        return_value="1: Unsigned",
    )
    patch_render = patch(
        "app.controllers.contract_controller.render_view_all_contracts"
    )

    with (
        patch_session
    ), (
        patch_render_choice_status
    ), patch_render as mock_render:

        contract_controller.permission.authenticated_collaborator = \
            authenticated_user
        contract_controller.authenticated_collaborator = authenticated_user
        contract_controller.permission.department = \
            authenticated_user.department.name
        contract_controller.filter_contracts_by_status()

    mock_render.assert_called_once_with(
        [fake_contracts[0]],
        authenticated_user
    )


def test_filter_contract_no_auth(
    mock_file,
    db_session,
):
    # no authenticated user so access should be denied
    contract_controller = ContractController()

    patch_session = patch(
        "app.controllers.contract_controller.Session",
        return_value=db_session
    )
    patch_render_access_denied = patch(
        "app.controllers.contract_controller.render_access_denied"
    )

    with (
        patch_session
    ), patch_render_access_denied as mock_render_access_denied:

        contract_controller.filter_contracts_by_status()

    mock_render_access_denied.assert_called_once()


def test_filter_contracts_by_status_not_sales(
    mock_file,
    db_session,
    fake_collaborators,
):
    contract_controller = ContractController()

    patch_session = patch(
        "app.controllers.contract_controller.Session",
        return_value=db_session
    )

    authenticated_user = fake_collaborators[1]  # Support department

    patch_render_choice_status = patch(
        "app.controllers.contract_controller.render_choice_status_contracts",
        return_value="1: Unsigned",
    )
    patch_render_access_denied = patch(
        "app.controllers.contract_controller.render_access_denied"
    )

    with (
        patch_session
    ), (
        patch_render_choice_status
    ), patch_render_access_denied as mock_render_access_denied:

        contract_controller.permission.authenticated_collaborator = \
            authenticated_user
        contract_controller.permission.department = \
            authenticated_user.department.name
        contract_controller.filter_contracts_by_status()

    mock_render_access_denied.assert_called_once()


def test_filter_contracts_not_fully_paid(
    mock_file,
    db_session,
    fake_contracts,
    fake_collaborators,
):
    contract_controller = ContractController()

    patch_session = patch(
        "app.controllers.contract_controller.Session",
        return_value=db_session
    )

    authenticated_user = fake_collaborators[2]  # Sales department

    patch_render = patch(
        "app.controllers.contract_controller.render_view_all_contracts"
    )

    with (
        patch_session
    ), patch_render as mock_render:

        contract_controller.permission.authenticated_collaborator = \
            authenticated_user
        contract_controller.authenticated_collaborator = authenticated_user
        contract_controller.permission.department = \
            authenticated_user.department.name

        contract_controller.filter_contracts_not_fully_paid()

    mock_render.assert_called_once_with(
        [fake_contracts[0], fake_contracts[1]],
        authenticated_user
    )


def test_filter_contracts_not_fully_paid_no_auth(
    mock_file,
    db_session,
):
    # no authenticated user so access should be denied
    contract_controller = ContractController()

    patch_session = patch(
        "app.controllers.contract_controller.Session",
        return_value=db_session
    )
    patch_render_access_denied = patch(
        "app.controllers.contract_controller.render_access_denied"
    )

    with (
        patch_session
    ), patch_render_access_denied as mock_render_access_denied:

        contract_controller.filter_contracts_not_fully_paid()

    mock_render_access_denied.assert_called_once()


def test_filter_contracts_not_fully_paid_not_sales(
    mock_file,
    db_session,
    fake_collaborators,
):
    contract_controller = ContractController()

    patch_session = patch(
        "app.controllers.contract_controller.Session",
        return_value=db_session
    )

    authenticated_user = fake_collaborators[1]  # Support department

    patch_render_access_denied = patch(
        "app.controllers.contract_controller.render_access_denied"
    )

    with (
        patch_session
    ), patch_render_access_denied as mock_render_access_denied:

        contract_controller.permission.authenticated_collaborator = \
            authenticated_user
        contract_controller.permission.department = \
            authenticated_user.department.name

        contract_controller.filter_contracts_not_fully_paid()

    mock_render_access_denied.assert_called_once()
