from app.models.collaborator import Collaborator
from app.models.customer import Customer
from app.permissions.permission import Permission
from app.views.menu_view import render_access_denied
import datetime
from db import Session
from app.views.customer_view import (
    get_customer_info,
    render_view_all_customers,
    show_created_customer_success,
    show_created_customer_error,
    render_choice_customer,
    render_read_customer,
    show_modified_customer_success,
    show_modified_customer_error)
from app.views.customer_input_view import (
    ask_customer_modification,
)
from app.utils.database_utils import commit_to_db


class CustomerController:
    def __init__(self):
        self.permission = Permission()
        self.authenticated_collaborator = self.permission.authenticated_collaborator

    def view_customers(self):
        if not self.permission.can_read():
            render_access_denied()
            return

        session = Session()

        try:
            customers = session.query(Customer).all()
            render_view_all_customers(customers)

        finally:
            session.close()
            Session.remove()

    def create_customer(self):
        if not self.permission.can_create_customer():
            render_access_denied()
            return

        session = Session()

        try:
            customer_info = get_customer_info()
            now = datetime.datetime.now()
            customer = Customer(
                first_name=customer_info["first_name"],
                last_name=customer_info["last_name"],
                mail=customer_info["email"],
                phone_number=customer_info["phone_number"],
                company_name=customer_info["company_name"],
                creation_date=now,
                last_update=now,
                commercial_id=self.authenticated_collaborator.id,
            )

            if commit_to_db(session, customer):
                show_created_customer_success()
            else:
                show_created_customer_error()

        finally:
            session.close()
            Session.remove()

    def read_customer(self):

        if not self.permission.can_read():
            render_access_denied()
            return

        session = Session()

        try:
            customers = session.query(Customer).all()

            customer_choice = render_choice_customer(customers)
            if not customer_choice:
                return

            customer_object = (
                session.query(Customer)
                .filter(Customer.id == int(customer_choice.split(":")[0]))
                .first()
            )
            render_read_customer(customer_object)

        finally:
            session.close()
            Session.remove()

    def modify_customer(self):
        if not self.permission.can_modify_customer():
            render_access_denied()
            return

        session = Session()
        try:
            customers = session.query(Customer).all()

            customer_choice = render_choice_customer(customers)
            if not customer_choice:
                return

            customer_object = (
                session.query(Customer)
                .filter(Customer.id == int(customer_choice.split(":")[0]))
                .first()
            )
            if not customer_object:
                return

            current_sales_collaborator = (
                session.query(Collaborator)
                .filter(Collaborator.id == customer_object.commercial_id)
                .first()
            )
            if not current_sales_collaborator:
                return

            current_sales_collaborator_name = f"{current_sales_collaborator.first_name} {current_sales_collaborator.last_name} (ID {current_sales_collaborator.id})"

            sales_collaborators = (
                session.query(Collaborator)
                .filter(Collaborator.department.has(name="Sales"))
                .all()
            )

            customer_updated = ask_customer_modification(
                customer_object,
                current_sales_collaborator_name,
                sales_collaborators
            )

            if not customer_updated:
                return

            for key, value in customer_updated.items():
                setattr(customer_object, key, value)
            customer_object.last_update = datetime.datetime.now().date()  # type: ignore

            if commit_to_db(session, customer_object):
                show_modified_customer_success()
            else:
                show_modified_customer_error()

        finally:
            session.close()
            Session.remove()
