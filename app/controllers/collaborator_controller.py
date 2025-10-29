from app.utils.security_utils import hash_anonymize
from app.views.collaborator_view import (
    get_signup_info,
    show_cannot_delete_self,
    show_signin_success,
    show_signin_error,
    show_signup_success,
    show_signup_error,
    show_error_commiting_to_db,
    render_choice_collaborator,
    show_delete_error,
    show_delete_success,
)
from app.models.collaborator import Collaborator
from app.utils.password_utils import hash_password
from app.utils.database_utils import commit_to_db
from app.utils.collaborator_utils import find_collaborator_by_login
from app.utils.password_utils import verify_password
from app.views.collaborator_input_view import (
    ask_confirm_delete,
    ask_login,
    ask_password,
    ask_collaborator_modification,
)
from app.utils.session_utils import generate_token, save_token
from app.permissions.permission import Permission
from app.views.menu_view import render_access_denied
from db import Session
import sentry_sdk


class CollaboratorController:
    def __init__(self):
        self.permission = Permission()
        self.authenticated_collaborator: Collaborator = self.permission.authenticated_collaborator  # noqa: E501

    def signup(self):
        session = Session()

        try:
            user_info = get_signup_info(
                session,
                self.authenticated_collaborator
            )
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
                id_collaborator_anonimized_created = hash_anonymize(
                        str(collaborator.id)
                    )
                sentry_sdk.capture_message(
                    f"New collaborator created: "
                    f"{id_collaborator_anonimized_created} "
                    f"by himself/herself."
                )
                sentry_sdk.flush()
                show_signup_success()
            else:
                show_signup_error()
        finally:
            session.close()
            Session.remove()

    def signin(self):
        session = Session()

        try:
            user_login = ask_login()
            collaborator_found = find_collaborator_by_login(
                user_login,
                session
            )

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

    def logout(self):
        print("Log out function called")

    def create_collaborator(self):
        if not self.permission.can_create_collaborator():
            render_access_denied()
            return

        session = Session()

        try:
            user_info = get_signup_info(
                session,
                self.authenticated_collaborator
            )
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
                id_collaborator_anonimized_created = hash_anonymize(
                        str(collaborator.id)
                    )
                id_collaborator_anonimized = hash_anonymize(
                        str(self.authenticated_collaborator.id)
                    )
                sentry_sdk.capture_message(
                    f"New collaborator created: "
                    f"{id_collaborator_anonimized_created} "
                    f"by {id_collaborator_anonimized}."
                )
                sentry_sdk.flush()
                show_signup_success()
            else:
                show_signup_error()
        finally:
            session.close()
            Session.remove()

    def modify_collaborator(self):
        if not self.permission.can_modify_collaborator():
            render_access_denied()
            return

        session = Session()
        try:
            collaborators = session.query(Collaborator).all()
            collaborator_choice = render_choice_collaborator(
                collaborators,
                self.authenticated_collaborator
            )
            if not collaborator_choice:
                return

            collaborator_object = (
                session.query(Collaborator)
                .filter(
                    Collaborator.id == int(collaborator_choice.split(":")[0])
                )
                .first())
            if not collaborator_object:
                return

            collaborator_updated = ask_collaborator_modification(
                session,
                collaborator_object
            )
            if not collaborator_updated:
                return

            if "password" in collaborator_updated:
                hashed_password = hash_password(collaborator_updated["password"])  # noqa: E501
                collaborator_updated["password"] = hashed_password

            for key, value in collaborator_updated.items():
                setattr(collaborator_object, key, value)

            if commit_to_db(session, collaborator_object):
                id_collaborator_anonimized_modified = hash_anonymize(
                        str(collaborator_object.id)
                    )
                id_collaborator_anonimized = hash_anonymize(
                        str(self.authenticated_collaborator.id)
                    )
                sentry_sdk.capture_message(
                    f"Collaborator modified: "
                    f"{id_collaborator_anonimized_modified}"
                    f" by {id_collaborator_anonimized}."
                )
                show_signup_success()
            else:
                show_signup_error()

        finally:
            session.close()
            Session.remove()

    def delete_collaborator(self):
        if not self.permission.can_delete_collaborator():
            render_access_denied()
            return

        session = Session()
        try:
            collaborators = session.query(Collaborator).all()
            collaborator_choice = render_choice_collaborator(
                collaborators,
                self.authenticated_collaborator
            )
            if not collaborator_choice:
                return

            collaborator_object = (
                session.query(Collaborator)
                .filter(
                    Collaborator.id == int(collaborator_choice.split(":")[0])
                )
                .first())
            if not collaborator_object:
                return

            if collaborator_object.id == self.authenticated_collaborator.id:  # type: ignore  # noqa: E501
                show_cannot_delete_self()
                return

            if not collaborator_object:
                return

            if ask_confirm_delete(collaborator_object):
                show_delete_success()
            else:
                show_delete_error()

            session.delete(collaborator_object)
            session.commit()
            return True
        except Exception as e:
            # Even if no explicit transaction seems to have started,
            # rollback prevents issues if something was implicitly flushed.
            session.rollback()
            show_error_commiting_to_db(e)
            sentry_sdk.capture_exception(e)
            return False
        finally:
            session.close()
            Session.remove()
