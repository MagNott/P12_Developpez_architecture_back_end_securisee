from app.models.customer import Customer
from app.permissions.permission import Permission
from app.models.status import Status
from app.models.contract import Contract
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
    get_statuses,
    show_modified_contract_error,
    show_modified_contract_success,
)
from app.views.contract_input_view import (
    ask_contract_modification,
)
from app.utils.database_utils import commit_to_db
from app.utils.constants import MANAGEMENT


class ContractController:
    def __init__(self):
        self.permission = Permission()
        self.authenticated_collaborator = self.permission.authenticated_collaborator

    def view_contracts(self):
        if not self.permission.can_read():
            render_access_denied()
            return

        session = Session()

        try:
            contracts = session.query(Contract).all()
            render_view_all_contracts(
                contracts,
                self.authenticated_collaborator
            )

        finally:
            session.close()
            Session.remove()

    def create_contract(self):
        if not self.permission.can_create_contract():
            render_access_denied()
            return

        session = Session()

        try:
            contract_info = get_contract_info(self.authenticated_collaborator)

            customer_list = session.query(Customer).all()
            customer_contract_choice = render_choice_customer(customer_list)
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

            now = datetime.datetime.now()
            contract = Contract(
                contract_amount=contract_info["contract_amount"],
                amount_due=contract_info["amount_due"],
                creation_date=now,
                customer_id=customer_object_contract.id,
                status_id=contract_info["status_id"],
            )
            if commit_to_db(session, contract):
                show_created_contract_success()

            else:
                show_created_contract_error()
        finally:
            session.close()
            Session.remove()

    def read_contract(self):
        if not self.permission.can_read():
            render_access_denied()
            return

        session = Session()

        try:
            contracts = session.query(Contract).all()

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
        if not self.permission.can_modify_contract():
            render_access_denied()
            return

        session = Session()
        try:
            contracts = session.query(Contract).all()

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

            statuses = get_statuses(session)

            current_status = (
                session.query(Status)
                .filter(Status.id == contract_object.status_id)
                .first()
            )
            if not current_status:
                return

            # Only commercial collaborator can modify their own customers
            if not (self.department == MANAGEMENT or contract_object.customer.commercial_id != self.authenticated_collaborator.id):  # type: ignore
                render_access_denied()
                return

            contract_updated = ask_contract_modification(
                contract_object,
                current_status,
                statuses
            )
            if not contract_updated:
                return

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
