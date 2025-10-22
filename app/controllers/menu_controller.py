from app.views.menu_view import (
    render_sales_menu,
    render_management_menu,
    render_main_menu,
    render_support_menu,
)
from app.views.menu_view import render_access_denied
from app.utils.constants import (ASSIGN_SUPPORT_COLLABORATOR_TO_EVENT,
                                 MODIFY_EVENT,
                                 SALES,
                                 CREATE_CONTRACT,
                                 READ_CUSTOMER,
                                 READ_CONTRACT,
                                 READ_EVENT,
                                 CREATE_CUSTOMER,
                                 CREATE_EVENT,
                                 DELETE_COLLABORATOR,
                                 DISPLAY_MY_EVENTS,
                                 EVENT_WITHOUT_SUPPORT_COLLABORATOR,
                                 MANAGEMENT,
                                 LOGOUT,
                                 VIEW_CONTRACTS,
                                 MODIFY_COLLABORATOR,
                                 MODIFY_CONTRACT,
                                 MODIFY_CUSTOMER,
                                 VIEW_EVENTS,
                                 SIGNIN, SIGNUP, SUPPORT,
                                 UPDATE_MY_EVENTS, VIEW_CUSTOMERS)
from app.utils.session_utils import get_authenticated_department
from app.controllers.collaborator_controller import signin, signup, logout
from app.controllers.contract_controller import ContractController
from app.controllers.customer_controller import CustomerController
from app.controllers.collaborator_controller import (
    modify_collaborator,
    delete_collaborator,
)
from app.controllers.event_controller import EventController
from app.permissions.permission import Permission


def action_main_menu():
    while True:
        action = render_main_menu()

        if action == SIGNIN:
            signin()
        elif action == SIGNUP:
            signup()
        elif action == LOGOUT:
            logout()
            break


def department_menu():
    department_object = get_authenticated_department()
    if not department_object:
        return render_access_denied()

    department = str(department_object.name)

    if department == MANAGEMENT:
        action_management_menu()

    elif department == SUPPORT:
        action_support_menu()

    elif department == SALES:
        action_sales_menu()


def action_sales_menu():
    while True:
        action = render_sales_menu()
        if action == CREATE_CUSTOMER:
            customer_controller = CustomerController()
            customer_controller.create_customer()
        elif action == VIEW_CUSTOMERS:
            customer_controller = CustomerController()
            customer_controller.view_customers()
        elif action == READ_CUSTOMER:
            customer_controller = CustomerController()
            customer_controller.read_customer()
        elif action == MODIFY_CUSTOMER:
            customer_controller = CustomerController()
            customer_controller.modify_customer()
        elif action == VIEW_CONTRACTS:
            contract_controller = ContractController()
            contract_controller.view_contracts()
        elif action == READ_CONTRACT:
            contract_controller = ContractController()
            contract_controller.read_contract()
        elif action == MODIFY_CONTRACT:
            contract_controller = ContractController()
            contract_controller.modify_contract()
        elif action == VIEW_EVENTS:
            event_controller = EventController()
            event_controller.view_events()
        elif action == CREATE_EVENT:
            event_controller = EventController()
            event_controller.create_event()
        elif action == READ_EVENT:
            event_controller = EventController()
            event_controller.read_event()
        elif action == LOGOUT:
            logout()
            break


def action_management_menu():
    while True:
        action = render_management_menu()

        if action == CREATE_CONTRACT:
            contract_controller = ContractController()
            contract_controller.create_contract()
        elif action == VIEW_CONTRACTS:
            contract_controller = ContractController()
            contract_controller.view_contracts()
        elif action == READ_CONTRACT:
            contract_controller = ContractController()
            contract_controller.read_contract()
        elif action == MODIFY_CONTRACT:
            contract_controller = ContractController()
            contract_controller.modify_contract()
        elif action == VIEW_EVENTS:
            event_controller = EventController()
            event_controller.view_events()
        elif action == READ_EVENT:
            event_controller = EventController()
            event_controller.read_event()
        elif action == ASSIGN_SUPPORT_COLLABORATOR_TO_EVENT:
            event_controller = EventController()
            event_controller.assign_support_collaborator_to_event()
        elif action == VIEW_CUSTOMERS:
            customer_controller = CustomerController()
            customer_controller.view_customers()
        elif (
            action == MODIFY_COLLABORATOR
        ):
            modify_collaborator()
        elif (
            action == DELETE_COLLABORATOR
        ):
            delete_collaborator()
        elif action == LOGOUT:
            logout()
            break


def action_support_menu():
    while True:
        action = render_support_menu()

        if action == DISPLAY_MY_EVENTS:
            event_controller = EventController()
            event_controller.display_my_events()
        elif action == VIEW_CONTRACTS:
            contract_controller = ContractController()
            contract_controller.view_contracts()
        elif action == READ_CONTRACT:
            contract_controller = ContractController()
            contract_controller.read_contract()
        elif action == VIEW_CUSTOMERS:
            customer_controller = CustomerController()
            customer_controller.view_customers()
        elif action == VIEW_EVENTS:
            event_controller = EventController()
            event_controller.view_events()
        elif action == READ_EVENT:
            event_controller = EventController()
            event_controller.read_event()
        elif action == MODIFY_EVENT:
            event_controller = EventController()
            event_controller.modify_event()
        elif action == LOGOUT:
            from app.controllers.collaborator_controller import logout

            logout()
            break
