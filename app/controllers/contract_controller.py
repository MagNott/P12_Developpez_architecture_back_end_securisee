from app.models.customer import Customer
from app.permissions.permission import Permission
from app.models.contract import Contract
from app.utils.contract_utils import get_contracts
from app.utils.security_utils import hash_anonymize
from app.views.customer_view import render_choice_customer
from app.views.menu_view import render_access_denied
from db import Session
import datetime
from app.views.contract_view import (
    render_view_all_contracts,
    get_contract_info,
    show_created_contract_error,
    show_created_contract_success,
    render_choice_contract,
    render_read_contract,
    show_modified_contract_error,
    show_modified_contract_success,
    render_choice_status_contracts,
)
from app.views.contract_input_view import (
    ask_contract_modification,
)
from app.utils.database_utils import commit_to_db
from app.utils.constants import MANAGEMENT, SALES
from app.models.collaborator import Collaborator
from app.views.event_view import show_no_contracts_available
from app.utils.status_utils import get_statuses
import sentry_sdk


class ContractController:
    def __init__(self):
        self.permission = Permission()
        self.authenticated_collaborator: Collaborator = self.permission.authenticated_collaborator  # noqa: E501

    def view_contracts(self):
        """
        View all contracts.

        - Requires read permission.
        - Retrieves all contracts from the database via SQLAlchemy.
        - Displays the contract list using the appropriate view function.
        """
        if not self.permission.can_read():
            render_access_denied()
            return

        session = Session()

        try:
            contracts = get_contracts(session)
            render_view_all_contracts(
                contracts,
                self.authenticated_collaborator
            )

        finally:
            session.close()
            Session.remove()

    def create_contract(self):
        """
        Create a new contract.

        - Requires create permission.
        - Prompts for contract details using an interactive form.
        - Prompts to select a customer from the list.
        - Retrieves the "Unsigned" status from the database.
        - Creates and stores the contract in the database via SQLAlchemy.
        - Displays a success or error message based on the result.
        """
        if not self.permission.can_create_contract():
            render_access_denied()
            return

        session = Session()

        try:
            contract_info = get_contract_info(
                session,
                self.authenticated_collaborator
            )

            customer_list = session.query(Customer).all()
            customer_contract_choice = render_choice_customer(
                customer_list,
                self.authenticated_collaborator
            )
            if not customer_contract_choice:
                show_created_contract_error()
                return

            customer_object_contract = (
                session.query(Customer)
                .filter(Customer.id == int(
                    customer_contract_choice.split(":")[0]))
                .first()
            )
            if not customer_object_contract:
                return

            statuses: list[dict] = get_statuses(session)

            unsigned_status = None
            for status in statuses:
                if status["name"] == "Unsigned":
                    unsigned_status = status["id"]
                    break

            if not unsigned_status:
                show_created_contract_error()
                return

            now = datetime.datetime.now()
            contract = Contract(
                contract_amount=contract_info["contract_amount"],
                amount_due=contract_info["amount_due"],
                creation_date=now,
                customer_id=customer_object_contract.id,
                status_id=unsigned_status,
            )
            if commit_to_db(session, contract):
                show_created_contract_success()

            else:
                show_created_contract_error()
        finally:
            session.close()
            Session.remove()

    def read_contract(self):
        """
        Read a contract's details.

        - Requires read permission.
        - Retrieves all contracts from the database via SQLAlchemy.
        - Prompts the user to select a contract.
        - Displays the details of the selected contract.
        """
        if not self.permission.can_read():
            render_access_denied()
            return

        session = Session()

        try:
            contracts = get_contracts(session)

            contract_choice = render_choice_contract(
                contracts,
                self.authenticated_collaborator
            )
            if not contract_choice:
                return

            contract_object = (
                session.query(Contract)
                .filter(Contract.id == int(contract_choice.split(":")[0]))
                .first()
            )
            if not contract_object:
                return

            render_read_contract(
                contract_object,
                self.authenticated_collaborator
            )

        finally:
            session.close()
            Session.remove()

    def modify_contract(self):
        """
        Modify an existing contract.

        - Requires modify permission.
        - Retrieves 2 lists of contracts according to the department
        collaborator.
            - If sales, only contracts of their own customers.
            - If management, all contracts.
        - Prompts the user to select a contract to modify.
        - Collects updated contract details using an interactive form.
        - Applies the updates to the contract in the database via SQLAlchemy.
        - If the status is changed to "Signed", logs the action with anonymized
        IDs to Sentry.
        - Displays success or error message based on the result.
        """
        if not self.permission.can_modify_contract():
            render_access_denied()
            return

        session = Session()
        try:
            # Only commercial collaborator can modify their own
            # customers' contracts, a management collaborator can modify all.
            if self.authenticated_collaborator.department.name == SALES:
                contracts = get_contracts(session)
                filtered_contracts = [
                    c for c in contracts
                    if c.customer.commercial_id == self.authenticated_collaborator.id]  # noqa: E501
            elif self.authenticated_collaborator.department.name == MANAGEMENT:
                filtered_contracts = get_contracts(session)
            else:
                render_access_denied()
                return

            contract_choice = render_choice_contract(
                filtered_contracts,
                self.authenticated_collaborator
            )
            if not contract_choice:
                show_no_contracts_available()
                return

            # view return string like "1: Contract for John Doe"
            contract_object = (
                session.query(Contract)
                .filter(Contract.id == int(contract_choice.split(":")[0]))
                .first()
            )
            if not contract_object:
                return

            statuses = get_statuses(session)

            current_status = contract_object.status
            if not current_status:
                return

            # Even though the contract list is pre-filtered, need to
            # double-check access rights for safety.
            if not (
                self.permission.department == MANAGEMENT
                or contract_object.customer.commercial_id
                == self.authenticated_collaborator.id  # type: ignore
            ):
                render_access_denied()
                return

            contract_updated = ask_contract_modification(
                contract_object,
                current_status,
                statuses
            )
            if not contract_updated:
                return

            if contract_updated.get("status_id"):
                for status in statuses:
                    if status["id"] == contract_updated["status_id"]:
                        selected_status_name = status["name"]
                        break

                if (selected_status_name == "Signed" and current_status.name != "Signed"):  # noqa: E501
                    id_contract_anonimized = hash_anonymize(str(contract_object.id))  # noqa: E501
                    id_collaborator_anonimized = hash_anonymize(
                        str(self.authenticated_collaborator.id)
                    )
                    sentry_sdk.capture_message(  #
                        f"Contract ID {id_contract_anonimized} marked as Signed "  # noqa: E501
                        f"by Collaborator ID "
                        f"{id_collaborator_anonimized}"
                    )

            # Apply updates to the contract object
            for key, value in contract_updated.items():
                setattr(contract_object, key, value)

            if commit_to_db(session, contract_object):
                show_modified_contract_success()
            else:
                show_modified_contract_error()

        finally:
            session.close()
            Session.remove()

    def filter_contracts_by_status(self):
        """
        View all contracts filtered by a selected status.

        - Requires filter permission, accessible to sales authenticated
        collaborators.
        - Prompts the user to select a status from the list.
        - Retrieves contracts with the selected status and belonging to
        the authenticated collaborator's customers.
        - Displays the filtered contract list using the appropriate view
        function.
        """
        if not self.permission.can_filter_contracts_by_status():
            render_access_denied()
            return

        session = Session()

        try:
            statuses: list[dict] = get_statuses(session)
            if not statuses:
                return

            status_choices = [f"{status['id']}: {status['name']}"
                              for status in statuses]
            status_choice = render_choice_status_contracts(status_choices)
            if not status_choice:
                return

            status_id = int(status_choice.split(":")[0])

            filtered_contracts = (
                session.query(Contract)
                .join(Contract.customer)
                .filter(
                    Contract.status_id == status_id,
                    Customer.commercial_id == self.authenticated_collaborator.id  # noqa: E501
                )
                .all()
            )

            render_view_all_contracts(
                filtered_contracts,
                self.authenticated_collaborator
            )

        finally:
            session.close()
            Session.remove()

    def filter_contracts_not_fully_paid(self):
        """
        View all contracts that are not fully paid.

        - Required filter permission, Accessible to sales authenticated
        collaborators.
        - Retrieves contracts with an an unpaid balance and belonging
        to the authenticated collaborator's customers.
        - Displays the filtered contract list.
        """
        if not self.permission.can_filter_contracts_not_fully_paid():
            render_access_denied()
            return

        session = Session()

        try:
            filtered_contracts = (
                session.query(Contract)
                .join(Contract.customer)
                .filter(
                    Contract.amount_due > 0,
                    Customer.commercial_id == self.authenticated_collaborator.id  # noqa: E501
                    )
                .all()
            )

            render_view_all_contracts(
                filtered_contracts,
                self.authenticated_collaborator
            )

        finally:
            session.close()
            Session.remove()
