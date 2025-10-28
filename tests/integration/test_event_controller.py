from unittest.mock import patch
from app.controllers.event_controller import EventController


def test_view_events_success(
    db_session,
    fake_collaborators,
    fake_events,
):
    event_controller = EventController()

    authenticated_user = fake_collaborators[1]  # Support department

    patch_session = patch(
        "app.controllers.event_controller.Session", return_value=db_session
    )
    patch_render = patch("app.controllers.event_controller."
                         "render_view_all_events")

    with patch_session, patch_render as mock_render:
        event_controller.permission.authenticated_collaborator = (
            authenticated_user
        )
        event_controller.authenticated_collaborator = authenticated_user
        event_controller.permission.department = (
            authenticated_user.department.name
        )
        event_controller.view_events()

    mock_render.assert_called_once_with(fake_events, authenticated_user)


def test_view_events_failure_no_auth(
    db_session,
):
    # no authenticated user so access should be denied
    event_controller = EventController()

    patch_session = patch(
        "app.controllers.event_controller.Session", return_value=db_session
    )
    patch_render_access_denied = patch(
        "app.controllers.event_controller.render_access_denied"
    )

    with patch_session, \
            patch_render_access_denied as mock_render_access_denied:

        event_controller.view_events()

    mock_render_access_denied.assert_called_once()


def test_create_event_success(
    db_session,
    fake_collaborators,
    fake_event_info,
):
    event_controller = EventController()

    authenticated_user = fake_collaborators[2]  # Sales department

    patch_session = patch(
        "app.controllers.event_controller.Session", return_value=db_session
    )
    patch_get_info = patch(
        "app.controllers.event_controller.get_event_info",
        return_value=fake_event_info,
    )
    patch_render_success = patch(
        "app.controllers.event_controller.show_created_event_success"
    )

    with patch_session, patch_get_info, \
            patch_render_success as mock_render_success:

        event_controller.permission.authenticated_collaborator = (
            authenticated_user
        )
        event_controller.authenticated_collaborator = authenticated_user
        event_controller.permission.department = (
            authenticated_user.department.name
        )
        event_controller.create_event()

    mock_render_success.assert_called_once()


def test_create_event_failure_no_auth(
    db_session,
):
    # no authenticated user so access should be denied
    event_controller = EventController()

    patch_session = patch(
        "app.controllers.event_controller.Session", return_value=db_session
    )
    patch_render_access_denied = patch(
        "app.controllers.event_controller.render_access_denied"
    )

    with patch_session, \
            patch_render_access_denied as mock_render_access_denied:

        event_controller.create_event()

    mock_render_access_denied.assert_called_once()


def test_create_event_failure_wrong_department(
    db_session,
    fake_collaborators,
):
    # authenticated user is not in Sales department so access should be denied
    event_controller = EventController()

    authenticated_user = fake_collaborators[1]  # Support department

    patch_session = patch(
        "app.controllers.event_controller.Session", return_value=db_session
    )
    patch_render_access_denied = patch(
        "app.controllers.event_controller.render_access_denied"
    )

    with patch_session, \
            patch_render_access_denied as mock_render_access_denied:

        event_controller.permission.authenticated_collaborator = (
            authenticated_user
        )
        event_controller.permission.department = (
            authenticated_user.department.name
        )
        event_controller.create_event()

    mock_render_access_denied.assert_called_once()


def test_read_events_success(
    db_session,
    fake_collaborators,
    fake_events,
):
    event_controller = EventController()

    authenticated_user = fake_collaborators[0]  # Management department

    patch_session = patch(
        "app.controllers.event_controller.Session", return_value=db_session
    )
    patch_render = patch(
        "app.controllers.event_controller.render_choice_event",
        return_value="1: Event for Client A",
    )
    patch_render_details = patch(
        "app.controllers.event_controller.render_view_event_details",
        return_value="Event details for Event 1",
    )

    with patch_session, patch_render, \
            patch_render_details as mock_render_details:

        event_controller.permission.authenticated_collaborator = (
            authenticated_user
        )
        event_controller.authenticated_collaborator = authenticated_user
        event_controller.permission.department = (
            authenticated_user.department.name
        )
        event_controller.read_event()

    mock_render_details.assert_called_once_with(
        fake_events[0],
        authenticated_user
    )


def test_read_events_failure_no_auth(
    db_session,
):
    # no authenticated user so access should be denied
    event_controller = EventController()

    patch_session = patch(
        "app.controllers.event_controller.Session", return_value=db_session
    )
    patch_render_access_denied = patch(
        "app.controllers.event_controller.render_access_denied"
    )

    with patch_session, \
            patch_render_access_denied as mock_render_access_denied:

        event_controller.read_event()

    mock_render_access_denied.assert_called_once()


def test_modify_event_success(
    db_session,
    fake_collaborators,
    fake_event_info,
):
    event_controller = EventController()

    authenticated_user = fake_collaborators[1]  # Support department

    patch_session = patch(
        "app.controllers.event_controller.Session", return_value=db_session
    )
    patch_render = patch(
        "app.controllers.event_controller.render_choice_event",
        return_value="1: Event for Client A",
    )
    patch_ask_modification = patch(
        "app.controllers.event_controller.ask_event_modification",
        return_value=fake_event_info,
    )
    patch_render_success = patch(
        "app.controllers.event_controller.show_modified_event_success"
    )

    with (
        patch_session
    ), (
        patch_render
    ), patch_ask_modification, patch_render_success as mock_render_success:

        event_controller.permission.authenticated_collaborator = (
            authenticated_user
        )
        event_controller.authenticated_collaborator = authenticated_user
        event_controller.permission.department = (
            authenticated_user.department.name
        )
        event_controller.modify_event()

    mock_render_success.assert_called_once()


def test_modify_event_failure_no_auth(
    db_session,
):
    # no authenticated user so access should be denied
    event_controller = EventController()

    patch_session = patch(
        "app.controllers.event_controller.Session", return_value=db_session
    )
    patch_render_access_denied = patch(
        "app.controllers.event_controller.render_access_denied"
    )

    with patch_session, \
            patch_render_access_denied as mock_render_access_denied:

        event_controller.modify_event()

    mock_render_access_denied.assert_called_once()


def test_modify_event_failure_not_dedicated_collaborator(
    db_session,
    fake_collaborators,
    fake_event_info,
):
    # authenticated user is not the dedicated collaborator for the event
    event_controller = EventController()

    authenticated_user = fake_collaborators[4]  # Support department

    patch_session = patch(
        "app.controllers.event_controller.Session", return_value=db_session
    )
    patch_render = patch(
        "app.controllers.event_controller.render_choice_event",
        return_value="1: Event for Client A",
    )
    patch_ask_modification = patch(
        "app.controllers.event_controller.ask_event_modification",
        return_value=fake_event_info,
    )
    patch_render_access_denied = patch(
        "app.controllers.event_controller.render_access_denied"
    )

    with (
        patch_session
    ), (
        patch_render
    ), patch_ask_modification, \
            patch_render_access_denied as mock_render_access_denied:

        event_controller.permission.authenticated_collaborator = (
            authenticated_user
        )
        event_controller.authenticated_collaborator = authenticated_user
        event_controller.permission.department = (
            authenticated_user.department.name
        )
        event_controller.modify_event()

    mock_render_access_denied.assert_called_once()


def test_assign_event_success(
    db_session,
    fake_events,
    fake_collaborators,
):
    event_controller = EventController()

    authenticated_user = fake_collaborators[0]  # Management department

    patch_session = patch(
        "app.controllers.event_controller.Session", return_value=db_session
    )
    patch_render_event = patch(
        "app.controllers.event_controller.render_choice_event",
        return_value="1: Event for Client A",
    )
    patch_render_collaborator = patch(
        "app.controllers.event_controller.render_choice_support_collaborator",
        return_value="2:",
    )
    patch_choice_collaborators = patch(
        "app.controllers.event_controller.render_choice_support_collaborator",
        return_value=(
            f"{fake_collaborators[1].id}: "
            f"{fake_collaborators[1].first_name} "
            f"{fake_collaborators[1].last_name}"
        ),
    )
    patch_render_success = patch(
        "app.controllers.event_controller.show_assigned_event_success"
    )

    with (
        patch_session
    ), (
        patch_render_event
    ), (
        patch_render_collaborator
    ), patch_choice_collaborators, patch_render_success as mock_render_success:

        event_controller.permission.authenticated_collaborator = (
            authenticated_user
        )
        event_controller.authenticated_collaborator = authenticated_user
        event_controller.permission.department = (
            authenticated_user.department.name
        )
        event_controller.assign_support_collaborator_to_event()

    mock_render_success.assert_called_once()


def test_assign_event_failure_no_auth(
    db_session,
):
    # no authenticated user so access should be denied
    event_controller = EventController()

    patch_session = patch(
        "app.controllers.event_controller.Session", return_value=db_session
    )
    patch_render_access_denied = patch(
        "app.controllers.event_controller.render_access_denied"
    )

    with patch_session, \
            patch_render_access_denied as mock_render_access_denied:

        event_controller.assign_support_collaborator_to_event()

    mock_render_access_denied.assert_called_once()


def test_assign_event_failure_not_management(
    db_session,
    fake_collaborators,
):
    # authenticated user is not in Management department so access
    # should be denied
    event_controller = EventController()

    authenticated_user = fake_collaborators[1]  # Support department

    patch_session = patch(
        "app.controllers.event_controller.Session", return_value=db_session
    )
    patch_render_access_denied = patch(
        "app.controllers.event_controller.render_access_denied"
    )

    with patch_session, \
            patch_render_access_denied as mock_render_access_denied:

        event_controller.permission.authenticated_collaborator = (
            authenticated_user
        )
        event_controller.permission.department = (
            authenticated_user.department.name
        )
        event_controller.assign_support_collaborator_to_event()

    mock_render_access_denied.assert_called_once()


def test_display_my_events_success(
    db_session,
    fake_events,
    fake_collaborators,
):
    event_controller = EventController()

    authenticated_user = fake_collaborators[1]  # Support department

    patch_session = patch(
        "app.controllers.event_controller.Session", return_value=db_session
    )
    patch_render = patch("app.controllers.event_controller."
                         "render_view_my_events")

    with patch_session, patch_render as mock_render:

        event_controller.permission.authenticated_collaborator = (
            authenticated_user
        )
        event_controller.authenticated_collaborator = authenticated_user
        event_controller.permission.department = (
            authenticated_user.department.name
        )
        event_controller.display_my_events()

    mock_render.assert_called_once_with(
        [fake_events[0], fake_events[2]], authenticated_user
    )


def test_display_my_events_failure_no_auth(
    db_session,
):
    # no authenticated user so access should be denied
    event_controller = EventController()

    patch_session = patch(
        "app.controllers.event_controller.Session", return_value=db_session
    )
    patch_render_access_denied = patch(
        "app.controllers.event_controller.render_access_denied"
    )

    with patch_session, \
            patch_render_access_denied as mock_render_access_denied:

        event_controller.display_my_events()

    mock_render_access_denied.assert_called_once()


def test_display_my_events_failure_not_support(
    db_session,
    fake_collaborators,
):
    # authenticated user is not in Support department so access
    # should be denied
    event_controller = EventController()

    authenticated_user = fake_collaborators[0]  # Management department

    patch_session = patch(
        "app.controllers.event_controller.Session", return_value=db_session
    )
    patch_render_access_denied = patch(
        "app.controllers.event_controller.render_access_denied"
    )

    with patch_session, \
            patch_render_access_denied as mock_render_access_denied:

        event_controller.permission.authenticated_collaborator = (
            authenticated_user
        )
        event_controller.permission.department = (
            authenticated_user.department.name
        )
        event_controller.display_my_events()

    mock_render_access_denied.assert_called_once()
