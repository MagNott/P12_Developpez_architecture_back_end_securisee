from app.utils.collaborator_utils import (
    find_collaborator_by_login,
    get_collaborators
)


def test_find_collaborator_by_login_success(
        db_session,
        fake_collaborators
):

    found_collaborator = find_collaborator_by_login("AMartin", db_session)

    assert found_collaborator is not None
    assert found_collaborator.id == fake_collaborators[0].id


def test_find_collaborator_by_login_not_found(
        db_session,
        fake_collaborators
):

    found_collaborator = find_collaborator_by_login(
        "NonExistentLogin",
        db_session
    )

    assert found_collaborator is None


def test_get_collaborators_success(
        db_session,
        fake_collaborators,
):

    collaborators = get_collaborators(db_session)

    assert len(collaborators) == len(fake_collaborators)
