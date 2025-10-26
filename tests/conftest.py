import sys
from pathlib import Path
import datetime
from datetime import date
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
from app.models.event import Event  # noqa: E402
from app.controllers.event_controller import EventController  # noqa: E402
from app.controllers.collaborator_controller import CollaboratorController  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402
from db import BaseModel  # noqa: E402


@pytest.fixture
def db_engine():
    engine = create_engine("sqlite:///:memory:")
    BaseModel.metadata.create_all(engine)
    return engine


@pytest.fixture(scope="function")
def db_session(db_engine, fake_collaborators, fake_customers, fake_contracts, fake_events, department_management, department_support, department_sales, status_pending, status_signed, status_unsigned):
    Session = sessionmaker(bind=db_engine)
    session = Session()

    # adding initial department data
    session.add_all([
        department_management,
        department_support,
        department_sales
    ])
    session.commit()

    # adding initial collaborator data
    for collaborator in fake_collaborators:
        session.add(collaborator)
    session.commit()

    # adding initial customer data
    for customer in fake_customers:
        session.add(customer)
    session.commit()

    # adding initial status data (required for contracts)
    session.add_all([
        status_pending,
        status_signed,
        status_unsigned
    ])
    session.commit()

    # adding initial contract data
    for contract in fake_contracts:
        # link the status already added to the session
        session.add(contract)
    session.commit()

    # adding initial event data
    for event in fake_events:
        session.add(event)
    session.commit()

    yield session
    session.close()


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
def mock_query(fake_management_collaborator):
    with patch(
        "app.controllers.collaborator_controller.find_collaborator_by_login",
        return_value=fake_management_collaborator,
    ):
        yield


@pytest.fixture
def customer_controller(fake_authenticated_collaborator):
    controller = CustomerController()
    controller.authenticated_collaborator = fake_authenticated_collaborator
    return controller


@pytest.fixture
def collaborator_controller(fake_authenticated_collaborator):
    controller = CollaboratorController()
    controller.authenticated_collaborator = fake_authenticated_collaborator
    return controller


@pytest.fixture
def contract_controller():
    controller = ContractController()
    #controller.authenticated_collaborator = fake_authenticated_collaborator
    return controller


@pytest.fixture
def event_controller():
    return EventController()


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
        return_value="AMartin",
    ) as mocked:
        yield mocked


@pytest.fixture
def mock_ask_login_fail():
    with patch(
        "app.controllers.collaborator_controller.ask_login",
        return_value="Toto",
    ) as mocked:
        yield mocked


@pytest.fixture
def mock_ask_password():
    with patch(
        "app.controllers.collaborator_controller.ask_password",
        return_value="hashed",
    ) as mocked:
        yield mocked


@pytest.fixture
def mock_file():
    with patch("builtins.open", mock_open()) as mocked_file:
        yield mocked_file


@pytest.fixture
def mock_is_authenticated_management(fake_management_collaborator):
    with patch(
        "app.utils.session_utils.is_authenticated",
        return_value=fake_management_collaborator,
    ):
        yield fake_management_collaborator


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
def department_management():
    return Department(id=1, name="Management")


@pytest.fixture
def department_support():
    return Department(id=2, name="Support")


@pytest.fixture
def department_sales():
    return Department(id=3, name="Sales")


@pytest.fixture
def fake_management_collaborator(department_management) -> Collaborator:
    fake_management_collaborator = Collaborator(
        first_name="Alice",
        last_name="Martin",
        mail="alice.martin@example.com",
        phone_number="0606060606",
        login="AliceMartin",
        password="hashed",
        department_id=1,
        department=department_management,
    )
    # Adding a department object to avoid AttributeError in tests
    return fake_management_collaborator


@pytest.fixture
def fake_collaborator_to_delete(department_support):
    return Collaborator(
        id=2,
        first_name="Jean",
        last_name="Dupont",
        login="JDupont",
        password="hashed",
        mail="jean@example.com",
        department_id=1,
        department=department_support,
    )


@pytest.fixture
def fake_collaborators(
    department_management,
    department_support,
    department_sales
) -> list[Collaborator]:
    return [
        Collaborator(
            first_name="Alice",
            last_name="Martin",
            mail="alice.martin@example.com",
            phone_number="0606060606",
            login="AMartin",
            password="hashed",
            department_id=1,
            department=department_management,
        ),
        Collaborator(
            first_name="Bob",
            last_name="Defrance",
            mail="bob.defrance@example.com",
            phone_number="0707070707",
            login="BDefrance",
            password="hashed",
            department_id=2,
            department=department_support,
        ),
        Collaborator(
            first_name="Carole",
            last_name="Blanchard",
            mail="carole.blanchard@example.com",
            phone_number="0808080808",
            login="CBlanchard",
            password="hashed",
            department_id=3,
            department=department_sales,
        ),
        Collaborator(
            first_name="David",
            last_name="Dupuis",
            mail="david.dupuis@example.com",
            phone_number="0909090909",
            login="DDupuis",
            password="hashed",
            department_id=3,
            department=department_sales,
        ),
        Collaborator(
            first_name="Margot",
            last_name="Gomes",
            mail="margot.gomes@example.com",
            phone_number="0707070707",
            login="MGomes",
            password="hashed",
            department_id=2,
            department=department_support,
        ),
    ]


@pytest.fixture
def fake_collaborator_info() -> dict:
    return {
        "first_name": "Diana",
        "last_name": "Jones",
        "email": "diana.jones@example.com",
        "phone_number": "0707070707",
        "login": "DJones",
        "password": "password123",
        "department_id": 1,
    }

@pytest.fixture
def fake_collaborator_info_already_exists() -> dict:
    return {
        "first_name": "Alice",
        "last_name": "Martin",
        "email": "alice.martin@example.com",
        "phone_number": "0606060606",
        "login": "AMartin",
        "password": "password123",
        "department_id": 1,
    }


@pytest.fixture
def fake_customer(fake_collaborators) -> Customer:
    now = datetime.date.today()

    customer = Customer(
        first_name="Jean",
        last_name="Durand",
        mail="jean.durand@example.com",
        phone_number="0707070707",
        company_name="Durand SARL",
        creation_date=now,
        last_update=now,
        commercial_id=fake_collaborators[2].id,
        collaborator=fake_collaborators[2],  # Bi-directional link
    )
    return customer


@pytest.fixture
def fake_customers(fake_collaborators) -> list[Customer]:
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
            commercial_id=fake_collaborators[2].id,
            collaborator=fake_collaborators[2],
        ),
        Customer(
            first_name="Lucie",
            last_name="Moreau",
            mail="lucie.moreau@example.com",
            phone_number="0601020304",
            company_name="Moreau Consulting",
            creation_date=now,
            last_update=now,
            commercial_id=fake_collaborators[2].id,
            collaborator=fake_collaborators[2],
        ),
    ]

    return customers


@pytest.fixture
def fake_customer_info() -> dict:
    return {
        "first_name": "Éloïse",
        "last_name": "Bertillon",
        "email": "eloise.bertillond@example.com",
        "phone_number": "0755123489",
        "company_name": "NebulaTech",
    }


@pytest.fixture
def status_pending():
    return Status(id=1, name="Pending")

@pytest.fixture
def status_signed():
    return Status(id=2, name="Signed")

@pytest.fixture
def status_unsigned():
    return Status(id=3, name="Unsigned")


@pytest.fixture
def fake_contracts(fake_customers, status_pending, status_signed, status_unsigned) -> list[Contract]:
    today = datetime.date.today()

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


@pytest.fixture
def fake_events(fake_contracts, fake_collaborators) -> list[Event]:
    return [
        Event(
            id=1,
            location="Paris",
            attendees=50,
            notes="Tech Conference",
            start_date=date(2025, 11, 1),
            end_date=date(2025, 11, 3),
            contract_id=fake_contracts[0].id,
            contract=fake_contracts[0],
            collaborator_id=fake_collaborators[1].id,
            collaborator=fake_collaborators[1],
        ),
        Event(
            id=2,
            location="Lyon",
            attendees=30,
            notes="Annual Meetup",
            start_date=date(2025, 12, 5),
            end_date=date(2025, 12, 6),
            contract_id=fake_contracts[1].id,
            contract=fake_contracts[1],
            collaborator_id=None,
            collaborator=None,
        ),
        Event(
            id=3,
            location="Marseille",
            attendees=20,
            notes="Client Workshop",
            start_date=date(2025, 12, 10),
            end_date=date(2025, 12, 11),
            contract_id=fake_contracts[2].id,
            contract=fake_contracts[2],
            collaborator_id=fake_collaborators[1].id,
            collaborator=fake_collaborators[1],
        ),
    ]


@pytest.fixture
def fake_event_info(fake_contracts, fake_collaborators) -> dict:
    return {
        "location": "Toulouse",
        "attendees": 15,
        "notes": "Internal Seminar",
        "start_date": date(2025, 11, 20),
        "end_date": date(2025, 11, 21),
        "contract_id": fake_contracts[0].id,
        "collaborator_id": fake_collaborators[1].id,
    }
