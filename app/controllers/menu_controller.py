from app.views.menu_view import (
    render_sales_menu,
    render_management_menu,
    render_main_menu,
    render_support_menu,
)
from app.views.menu_view import render_access_denied
from app.utils.constants import (ASSIGN_COLLABORATOR_TO_EVENT,
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
                                 MODIFY_COLLABORATOR,
                                 MODIFY_CONTRACT,
                                 MODIFY_CUSTOMER,
                                 SIGNIN, SIGNUP, SUPPORT,
                                 UPDATE_MY_EVENTS)
from app.utils.session_utils import get_authenticated_department
from app.controllers.collaborator_controller import signin, signup, logout
from app.controllers.contract_controller import (
    create_contract,
    modify_contract,
    read_contract
)
from app.controllers.customer_controller import (
    create_customer,
    modify_customer,
    read_customer
)
from app.controllers.collaborator_controller import (
    modify_collaborator,
    delete_collaborator,
)
from app.controllers.event_controller import (
    create_event,
    event_without_support_collaborator,
    assign_collaborator_to_event,
    read_event
)
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
    permission = Permission()

    while True:
        action = render_sales_menu()
        if action == CREATE_CUSTOMER and permission.can_create_customer():
            create_customer()
        elif action == MODIFY_CUSTOMER and permission.can_modify_customer():
            modify_customer()
        elif action == CREATE_EVENT and permission.can_create_event():
            create_event()
        elif action == READ_EVENT and permission.can_read():
            read_event()
        elif action == READ_CUSTOMER and permission.can_read():
            read_customer()
        elif action == READ_CONTRACT and permission.can_read():
            read_contract()
        elif action == LOGOUT:
            logout()
            break


def action_management_menu():
    permission = Permission()
    while True:
        action = render_management_menu()

        if action == CREATE_CONTRACT and permission.can_create_contract():
            create_contract()
        elif action == MODIFY_CONTRACT and permission.can_modify_contract():
            modify_contract()
        elif (
            action == MODIFY_COLLABORATOR
            and permission.can_modify_collaborator()
        ):
            modify_collaborator()
        elif (
            action == DELETE_COLLABORATOR
            and permission.can_delete_collaborator()
        ):
            delete_collaborator()
        elif (
            action == EVENT_WITHOUT_SUPPORT_COLLABORATOR
            and permission.can_view_events_without_support_collaborator()
        ):
            event_without_support_collaborator()
        elif (
            action == ASSIGN_COLLABORATOR_TO_EVENT
            and permission.can_assign_collaborator_to_event()
        ):
            assign_collaborator_to_event()
        elif action == LOGOUT:
            logout()
            break


def action_support_menu():
    permission = Permission()
    while True:
        action = render_support_menu()

        if action == DISPLAY_MY_EVENTS and permission.can_display_my_events():
            from app.controllers.event_controller import display_my_events
            display_my_events()

        elif action == UPDATE_MY_EVENTS and permission.can_update_my_events():
            from app.controllers.event_controller import update_my_events

            update_my_events()
        elif action == LOGOUT:
            from app.controllers.collaborator_controller import logout

            logout()
            break
