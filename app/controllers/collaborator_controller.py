from app.views.collaborator_view import (
    get_signup_info,
    show_signup_success,
    show_signup_error
)
from app.models.collaborator import Collaborator
from app.utils.password_utils import hash_password
from app.utils.database_utils import commit_to_db


# EST CE QU'IL FAUT GERER UN TEST D'INTEGRATION ICI ? OUI
def signup():
    user_info = get_signup_info()
    hashed_password = hash_password(user_info["password"])

    collaborator = Collaborator(
        first_name=user_info["first_name"],
        last_name=user_info["last_name"],
        mail=user_info["email"],
        phone_number=user_info["phone_number"],
        login=user_info["login"],
        password=hashed_password,
        department_id=user_info["department_id"]
    )

    if commit_to_db(collaborator):
        show_signup_success()
    else:
        show_signup_error()


def signin():
    print("Sign in function called")


def logout():
    print("Log out function called")
