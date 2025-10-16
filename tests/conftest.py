import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import pytest  # noqa: E402
from unittest.mock import mock_open, patch, MagicMock  # noqa: E402
from app.models.collaborator import Collaborator  # noqa: E402
from app.models.department import Department  # noqa: E402


@pytest.fixture
def mock_session():
    fake_session = MagicMock(name="Session")
    with patch(
        "app.utils.database_utils.SessionLocal", return_value=fake_session
    ):
        yield fake_session


@pytest.fixture
def mock_query(fake_collaborator):
    with patch(
        "app.controllers.collaborator_controller.find_collaborator_by_login",
        return_value=fake_collaborator,
    ):
        yield


@pytest.fixture
def mock_get_signup_info(fake_user_info):
    with patch(
        "app.controllers.collaborator_controller.get_signup_info",
        return_value=fake_user_info,
    ):
        yield


@pytest.fixture
def mock_ask_login():
    with patch(
        "app.controllers.collaborator_controller.ask_login",
        return_value="Alice",
    ):
        yield


@pytest.fixture
def mock_ask_password():
    with patch(
        "app.controllers.collaborator_controller.ask_password",
        return_value="hashed",
    ):
        yield


@pytest.fixture
def mock_file():
    with patch("builtins.open", mock_open()) as mocked_file:
        yield mocked_file


@pytest.fixture
def mock_is_authenticated_management(fake_collaborator):
    with patch(
        "app.utils.session_utils.is_authenticated",
        return_value=fake_collaborator,
    ):
        yield fake_collaborator


@pytest.fixture
def mock_is_authenticated_no_auth():
    with patch(
        "app.utils.session_utils.is_authenticated",
        return_value=None,
    ):
        yield


@pytest.fixture
def mock_department_menu():
    with patch("app.controllers.menu_controller.department_menu"):
        yield


@pytest.fixture
def fake_collaborator() -> Collaborator:
    fake_collaborator = Collaborator(
        first_name="Alice",
        last_name="Martin",
        mail="alice@example.com",
        phone_number="0606060606",
        login="AMartin",
        password="hashed",
        department_id=1,
        department=Department(id=1, name="Management"),
    )
    # Adding a department object to avoid AttributeError in tests
    return fake_collaborator


@pytest.fixture
def fake_user_info() -> dict:
    return {
        "first_name": "Alice",
        "last_name": "Martin",
        "email": "alice@example.com",
        "phone_number": "0606060606",
        "login": "AMartin",
        "password": "password123",
        "department_id": 1,
    }
