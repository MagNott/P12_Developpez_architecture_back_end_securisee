from app.views.menu_view import render_main_menu
from app.utils.constants import SIGNIN, SIGNUP, LOGOUT


def action_main_menu():
    while True:
        action = render_main_menu()

        if action == SIGNIN:
            from app.controllers.auth_controller import signin
            signin()
        elif action == SIGNUP:
            from app.controllers.auth_controller import signup
            signup()
        elif action == LOGOUT:
            from app.controllers.auth_controller import logout
            logout()
            break
