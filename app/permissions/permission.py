from app.utils.session_utils import (
    get_authenticated_department,
    is_authenticated,
)
from app.utils.constants import MANAGEMENT, SALES, SUPPORT


class Permission:
    def __init__(self):
        self.authenticated_collaborator = is_authenticated()
        department_object = (
            get_authenticated_department()
            if self.authenticated_collaborator
            else None
        )
        self.department = department_object.name if department_object else None

    def is_collaborator_authenticated(self) -> bool:
        return self.authenticated_collaborator is not False

    def can_read(self):
        # All authenticated collaborators can read any data
        # (customers, contracts, events, etc.)
        return self.is_collaborator_authenticated()

    def can_create_contract(self):
        return bool(
            self.is_collaborator_authenticated()
            and self.department == MANAGEMENT
        )

    def can_modify_contract(self):
        return self.is_collaborator_authenticated() and self.department in [
            MANAGEMENT,
            SALES,
        ]

    def can_modify_collaborator(self):
        return bool(
            self.is_collaborator_authenticated()
            and self.department == MANAGEMENT
        )

    def can_create_collaborator(self):
        return bool(
            self.is_collaborator_authenticated()
            and self.department == MANAGEMENT
        )

    def can_delete_collaborator(self):
        return bool(
            self.is_collaborator_authenticated()
            and self.department == MANAGEMENT
        )

    def can_view_events_without_support_collaborator(self):
        return bool(
            self.is_collaborator_authenticated()
            and self.department == MANAGEMENT
        )

    def can_assign_collaborator_to_event(self):
        return bool(
            self.is_collaborator_authenticated()
            and self.department == MANAGEMENT
        )

    def can_create_event(self):
        return bool(
            self.is_collaborator_authenticated()
            and self.department == SALES
        )

    def can_modify_event(self):
        return bool(
            self.is_collaborator_authenticated()
            and self.department == SUPPORT
        )

    def can_display_my_events(self):
        return bool(
            self.is_collaborator_authenticated()
            and self.department == SUPPORT
        )

    def can_create_customer(self) -> bool:
        return bool(self.is_collaborator_authenticated()
                    and self.department == SALES)

    def can_modify_customer(self):
        return bool(self.is_collaborator_authenticated()
                    and self.department == SALES)

    def can_assign_support_collaborator_to_event(self):
        return bool(
            self.is_collaborator_authenticated()
            and self.department == MANAGEMENT
        )

    def can_filter_contracts_by_status(self):
        return bool(self.is_collaborator_authenticated()
                    and self.department == SALES)

    def can_filter_contracts_not_fully_paid(self):
        return bool(self.is_collaborator_authenticated()
                    and self.department == SALES)
