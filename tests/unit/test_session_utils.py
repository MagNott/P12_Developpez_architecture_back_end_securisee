from app.utils.session_utils import generate_token, save_token
import datetime
import jwt


def test_generate_token_success(fake_collaborator):
    token = generate_token(fake_collaborator)
    decoded = jwt.decode(token, "ma_cle_secrete", algorithms=["HS256"])

    assert token is not None
    assert isinstance(token, str)
    assert decoded["login"] == fake_collaborator.login
    assert decoded["department"] == fake_collaborator.department.name
    assert "exp" in decoded
    assert decoded["exp"] > datetime.datetime.now().timestamp()


def test_save_token_success(mock_file, fake_collaborator):
    token = generate_token(fake_collaborator)
    save_token(token)

    # called open with correct file .session
    mock_file.assert_called_once_with(".session", "w", encoding='utf-8')
    # called write with the correct token
    mock_file().write.assert_called_once_with(token)
