from app.views.collaborator_view import (
    get_signup_info,
    show_signin_success,
    show_signin_error,
    show_signup_success,
    show_signup_error,
)
from app.models.collaborator import Collaborator
from app.utils.password_utils import hash_password
from app.utils.database_utils import commit_to_db
from app.utils.collaborator_utils import find_collaborator_by_login
from app.utils.password_utils import verify_password
from app.views.collaborator_input_view import ask_login, ask_password
from app.utils.session_utils import generate_token, save_token
from app.permissions.permission import Permission
from db import Session


def signup():
    session = Session()

    try:
        user_info = get_signup_info()
        hashed_password = hash_password(user_info["password"])

        collaborator = Collaborator(
            first_name=user_info["first_name"],
            last_name=user_info["last_name"],
            mail=user_info["email"],
            phone_number=user_info["phone_number"],
            login=user_info["login"],
            password=hashed_password,
            department_id=user_info["department_id"],
        )

        if commit_to_db(session, collaborator):
            show_signup_success()
        else:
            show_signup_error()
    finally:
        session.close()
        Session.remove()


def signin():
    session = Session()

    try:
        user_login = ask_login()
        collaborator_found = find_collaborator_by_login(user_login)

        user_password_clear = ask_password()

        if collaborator_found and verify_password(
            user_password_clear, str(collaborator_found.password)
        ):
            token = generate_token(collaborator_found)
            save_token(token)
            show_signin_success(collaborator_found)

            from app.controllers.menu_controller import department_menu
            # to avoid circular import
            department_menu()
        else:
            show_signin_error()

    finally:
        session.close()
        Session.remove()


def logout():
    print("Log out function called")

# did signup do that ?
# def create_collaborator():
#     print("[Collaborator Controller] create_collaborator() called")


def modify_collaborator():
    print("[Collaborator Controller] modify_collaborator() called")


def delete_collaborator():
    permission = Permission()
    if permission.can_delete_collaborator():
        print("[Collaborator Controller] delete_collaborator() called")
