import sys
from pathlib import Path
import datetime
sys.path.append(str(Path(__file__).parent.parent))
import pytest  # noqa: E402
from unittest.mock import mock_open, patch, MagicMock  # noqa: E402
from app.models.collaborator import Collaborator  # noqa: E402
from app.models.department import Department  # noqa: E402
from app.models.customer import Customer  # noqa: E402
from app.models.contract import Contract  # noqa: E402
from app.models.status import Status  # noqa: E402
from app.controllers.customer_controller import CustomerController  # noqa: E402
from app.controllers.contract_controller import ContractController  # noqa: E402

sys.path.append(str(Path(__file__).parent.parent))


@pytest.fixture
def mock_session():
    fake_session = MagicMock(name="Session")
    with patch(
        "db.Session", return_value=fake_session
    ):
        yield fake_session


@pytest.fixture
def fake_authenticated_collaborator():
    return MagicMock(id=1)


@pytest.fixture
def mock_query(fake_collaborator):
    with patch(
        "app.controllers.collaborator_controller.find_collaborator_by_login",
        return_value=fake_collaborator,
    ):
        yield


@pytest.fixture
def customer_controller(fake_authenticated_collaborator):
    controller = CustomerController()
    controller.authenticated_collaborator = fake_authenticated_collaborator
    return controller


@pytest.fixture
def contract_controller(fake_authenticated_collaborator):
    controller = ContractController()
    controller.authenticated_collaborator = fake_authenticated_collaborator
    return controller


@pytest.fixture
def mock_get_signup_info(fake_collaborator_info):
    with patch(
        "app.controllers.collaborator_controller.get_signup_info",
        return_value=fake_collaborator_info,
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
def fake_collaborators() -> list[Collaborator]:
    return [
        Collaborator(
            first_name="Alice",
            last_name="Martin",
            mail="alice@example.com",
            phone_number="0606060606",
            login="AMartin",
            password="hashed",
            department_id=1,
            department=Department(id=1, name="Management"),
        ),
        Collaborator(
            first_name="Bob",
            last_name="Defrance",
            mail="bob@example.com",
            phone_number="0707070707",
            login="BDefrance",
            password="hashed",
            department_id=2,
            department=Department(id=2, name="Support"),
        ),
        Collaborator(
            first_name="Carole",
            last_name="Blanchard",
            mail="carole@example.com",
            phone_number="0808080808",
            login="CBlanchard",
            password="hashed",
            department_id=3,
            department=Department(id=3, name="Sales"),
        ),
    ]


@pytest.fixture
def fake_collaborator_info() -> dict:
    return {
        "first_name": "Alice",
        "last_name": "Martin",
        "email": "alice@example.com",
        "phone_number": "0606060606",
        "login": "AMartin",
        "password": "password123",
        "department_id": 1,
    }


@pytest.fixture
def fake_customer(fake_collaborator) -> Customer:
    now = datetime.date.today()

    customer = Customer(
        first_name="Jean",
        last_name="Durand",
        mail="jean.durand@example.com",
        phone_number="0707070707",
        company_name="Durand SARL",
        creation_date=now,
        last_update=now,
        commercial_id=fake_collaborator.id,
        collaborator=fake_collaborator,  # Bi-directional link
    )

    return customer


@pytest.fixture
def fake_customers(fake_collaborator) -> list[Customer]:
    now = datetime.date.today()

    customers = [
        Customer(
            first_name="Jean",
            last_name="Durand",
            mail="jean.durand@example.com",
            phone_number="0707070707",
            company_name="Durand SARL",
            creation_date=now,
            last_update=now,
            commercial_id=fake_collaborator.id,
            collaborator=fake_collaborator,
        ),
        Customer(
            first_name="Lucie",
            last_name="Moreau",
            mail="lucie.moreau@example.com",
            phone_number="0601020304",
            company_name="Moreau Consulting",
            creation_date=now,
            last_update=now,
            commercial_id=fake_collaborator.id,
            collaborator=fake_collaborator,
        ),
    ]

    return customers


@pytest.fixture
def fake_customer_info() -> dict:
    return {
        "first_name": "Jean",
        "last_name": "Durand",
        "email": "jean.durand@example.com",
        "phone_number": "0707070707",
        "company_name": "Durand SARL",
    }


@pytest.fixture
def fake_contracts(fake_customers) -> list[Contract]:
    today = datetime.date.today()

    status_pending = Status(id=1, name="Pending")
    status_signed = Status(id=2, name="Signed")
    status_unsigned = Status(id=3, name="Unsigned")

    return [
        Contract(
            id=1,
            contract_amount=1500.0,
            amount_due=1500.0,
            creation_date=today,
            customer=fake_customers[0],
            status=status_pending,
        ),
        Contract(
            id=2,
            contract_amount=2500.0,
            amount_due=1000.0,
            creation_date=today,
            customer=fake_customers[1],
            status=status_signed,
        ),
        Contract(
            id=3,
            contract_amount=3000.0,
            amount_due=0.0,
            creation_date=today,
            customer=fake_customers[0],
            status=status_unsigned,
        ),
    ]


@pytest.fixture
def fake_contract_info() -> dict:
    return {
        "contract_amount": 2500.0,
        "amount_due": 1500.0,
        "status_id": 1,  # Pending
    }
