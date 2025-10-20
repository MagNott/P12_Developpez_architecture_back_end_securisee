from app.controllers.menu_controller import action_main_menu
from app.permissions.permission import Permission


if __name__ == "__main__":
    if Permission().is_collaborator_authenticated():
        from app.controllers.menu_controller import department_menu
        department_menu()
    else:
        action_main_menu()
