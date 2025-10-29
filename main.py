import sentry_sdk
import os


dsn_env = os.getenv("SENTRY_DSN")
if not dsn_env:
    raise ValueError("SENTRY_DSN environment variable is not set.")

sentry_sdk.init(
    dsn=dsn_env,
    send_default_pii=True,
    enable_logs=True,
)

from app.controllers.menu_controller import action_main_menu  # noqa: E402
from app.permissions.permission import Permission  # noqa: E402


if __name__ == "__main__":
    if Permission().is_collaborator_authenticated():
        from app.controllers.menu_controller import department_menu
        department_menu()
    else:
        action_main_menu()
