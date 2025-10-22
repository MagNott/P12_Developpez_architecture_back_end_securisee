from unittest.mock import patch


def test_view_events_success(
    mock_session,
    event_controller,
    fake_events,
):

    mock_session.query.return_value.all.return_value = fake_events

    patch_can_read = patch.object(
        event_controller.permission, "can_read", return_value=True
    )
    patch_session = patch(
        "app.controllers.event_controller.Session", return_value=mock_session
    )
    patch_render = patch("app.controllers.event_controller.render_view_all_events")

    with patch_can_read, patch_session, patch_render as mock_render:
        event_controller.view_events()

    mock_render.assert_called_once_with(fake_events)
    mock_session.query.assert_called_once()


def test_create_event_success(
    mock_session,
    event_controller,
    fake_event_info,
):

    patch_can_create = patch.object(
        event_controller.permission, "can_create_event", return_value=True
    )

    patch_session = patch(
        "app.controllers.event_controller.Session", return_value=mock_session
    )
    patch_get_info = patch(
        "app.controllers.event_controller.get_event_info",
        return_value=fake_event_info,
    )
    patch_commit = patch(
        "app.controllers.event_controller.commit_to_db", return_value=True
    )
    patch_render_success = patch(
        "app.controllers.event_controller.show_created_event_success"
    )

    with (
        patch_can_create
    ), (
        patch_session
    ), patch_get_info, patch_commit, patch_render_success as mock_render_success:
        event_controller.create_event()

    mock_render_success.assert_called_once()


def test_read_events_success(mock_session, event_controller, fake_events):

    mock_session.query.return_value.all.return_value = fake_events

    patch_can_read = patch.object(
        event_controller.permission, "can_read", return_value=True
    )
    patch_session = patch(
        "app.controllers.event_controller.Session", return_value=mock_session
    )
    patch_render = patch(
        "app.controllers.event_controller.render_choice_event",
        return_value="1: Event for Client A",
    )
    patch_render_details = patch(
        "app.controllers.event_controller.render_view_event_details",
        return_value="Event details for Event 1",
    )
    mock_session.query.return_value.filter.return_value.first.return_value = (
        fake_events[0]
    )

    with (
        patch_can_read
    ), patch_session, patch_render, patch_render_details as mock_render_details:
        event_controller.read_event()
    mock_session.query.assert_called()
    mock_render_details.assert_called_once_with(fake_events[0])


def test_modify_event_success(
    mock_session,
    event_controller,
    fake_events,
    fake_event_info,
):

    mock_session.query.return_value.all.return_value = fake_events

    patch_can_modify = patch.object(
        event_controller.permission, "can_modify_event", return_value=True
    )
    patch_session = patch(
        "app.controllers.event_controller.Session", return_value=mock_session
    )
    patch_render = patch(
        "app.controllers.event_controller.render_choice_event",
        return_value="1: Event for Client A",
    )
    patch_ask_modification = patch(
        "app.controllers.event_controller.ask_event_modification",
        return_value=fake_event_info,
    )
    patch_commit = patch(
        "app.controllers.event_controller.commit_to_db", return_value=True
    )
    patch_render_success = patch(
        "app.controllers.event_controller.show_modified_event_success"
    )

    mock_session.query.return_value.filter.return_value.first.return_value = (
        fake_events[0]
    )

    with (
        patch_can_modify
    ), (
        patch_session
    ), (
        patch_render
    ), (
        patch_ask_modification
    ), patch_commit, patch_render_success as mock_render_success:

        event_controller.modify_event()

    mock_render_success.assert_called_once()


def test_assign_event_success(
    mock_session,
    event_controller,
    fake_events,
    fake_collaborators,
):
    patch_can_assign = patch.object(
        event_controller.permission,
        "can_assign_support_collaborator_to_event",
        return_value=True,
    )
    patch_session = patch(
        "app.controllers.event_controller.Session", return_value=mock_session
    )
    patch_render_event = patch(
        "app.controllers.event_controller.render_choice_event",
        return_value="1: Event for Client A",
    )
    patch_render_collaborator = patch(
        "app.controllers.event_controller.render_choice_support_collaborator",
        return_value="2: Collaborator B",
    )
    patch_commit = patch(
        "app.controllers.event_controller.commit_to_db", return_value=True
    )
    patch_get_collaborators = patch(
        "app.controllers.event_controller.get_collaborators",
        return_value=[
            {"id": 1, "name": "Alice", "departement": "Support"},
            {"id": 2, "name": "Benjamin Renard", "departement": "Support"},
        ],
    )
    patch_render_success = patch(
        "app.controllers.event_controller.show_assigned_event_success"
    )

    mock_session.query.return_value.filter.return_value.all.return_value = fake_events
    mock_session.query.return_value.filter.return_value.first.return_value = (
        fake_events[0]
    )

    with (
        patch_can_assign
    ), (
        patch_session
    ), (
        patch_render_event
    ), (
        patch_render_collaborator
    ), (
        patch_commit
    ), patch_get_collaborators, patch_render_success as mock_render_success:

        event_controller.assign_support_collaborator_to_event()

    mock_render_success.assert_called_once()
    assert fake_events[0].collaborator_id == 2


def test_display_my_events_success(
    mock_session,
    event_controller,
    fake_events,
):

    mock_session.query.return_value.filter.return_value.all.return_value = fake_events

    patch_can_display = patch.object(
        event_controller.permission, "can_display_my_events", return_value=True
    )
    patch_session = patch(
        "app.controllers.event_controller.Session", return_value=mock_session
    )
    patch_render = patch("app.controllers.event_controller.render_view_my_events")
    with patch_can_display, patch_session, patch_render as mock_render:
        event_controller.display_my_events()

    mock_render.assert_called_once_with(fake_events)
    mock_session.query.assert_called_once()
