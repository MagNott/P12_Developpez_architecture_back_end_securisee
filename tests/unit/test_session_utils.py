from app.utils.session_utils import (
    generate_token,
    get_authenticated_department,
    save_token,
)
import datetime
import jwt
from app.utils.session_utils import is_authenticated
from unittest.mock import mock_open, patch


def test_generate_token_success(fake_management_collaborator):
    token = generate_token(fake_management_collaborator)
    decoded = jwt.decode(token, "ma_cle_secrete", algorithms=["HS256"])

    assert token is not None
    assert isinstance(token, str)
    assert decoded["login"] == fake_management_collaborator.login
    assert decoded["department"] == fake_management_collaborator.department.name
    assert "exp" in decoded
    assert decoded["exp"] > datetime.datetime.now().timestamp()


def test_save_token_success(mock_file, fake_management_collaborator):
    token = generate_token(fake_management_collaborator)
    save_token(token)

    # called open with correct file .session
    mock_file.assert_called_once_with(".session", "w", encoding="utf-8")
    # called write with the correct token
    mock_file().write.assert_called_once_with(token)


def test_get_authenticated_department(mock_is_authenticated_management):
    result = get_authenticated_department()
    assert result is not None
    assert str(result.name) == "Management"


def test_get_authenticated_department_no_auth(mock_is_authenticated_no_auth):
    result = get_authenticated_department()
    assert result is None


def test_is_authenticated_success(
        mock_file,
        mock_query,
        fake_management_collaborator
):
    token = generate_token(fake_management_collaborator)
    with patch("builtins.open", mock_open(read_data=token)), \
         patch("app.utils.session_utils.find_collaborator_by_login",
               return_value=fake_management_collaborator):
        result = is_authenticated()

    assert result is not False
    assert str(result.login) == "AliceMartin"
    assert result.department.name == "Management"


def test_is_authenticated_expired_token(mock_file, fake_management_collaborator):
    expired_payload = {
        "login": fake_management_collaborator.login,
        "exp": datetime.datetime.now() - datetime.timedelta(days=4000),
        "department": fake_management_collaborator.department.name,
    }
    expired_token = jwt.encode(
        expired_payload, "ma_cle_secrete", algorithm="HS256"
    )

    with patch(
        "builtins.open",
        mock_open(read_data=expired_token),
    ):
        result = is_authenticated()

    assert result is False


def test_is_authenticated_no_auth(mock_file):
    result = is_authenticated()
    assert result is False
