from app.utils import database_utils


def test_commit_to_db_success(mock_session, fake_management_collaborator):

    result = database_utils.commit_to_db(mock_session, fake_management_collaborator)

    assert result is True
    mock_session.add.assert_called_once_with(fake_management_collaborator)
    mock_session.commit.assert_called_once()
    mock_session.rollback.assert_not_called()


def test_commit_to_db_failure(mock_session, fake_management_collaborator):
    mock_session.commit.side_effect = Exception("DB Error")

    result = database_utils.commit_to_db(
        mock_session,
        fake_management_collaborator
    )

    assert result is False
    mock_session.add.assert_called_once_with(fake_management_collaborator)
    mock_session.commit.assert_called_once()
    mock_session.rollback.assert_called_once()
