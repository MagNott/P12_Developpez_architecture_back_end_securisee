from app.models.collaborator import Collaborator
from app.models.contract import Contract
from app.permissions.permission import Permission
from app.utils.contract_utils import get_contracts
from app.views.event_input_view import ask_event_modification
from app.views.menu_view import render_access_denied
from db import Session
from app.models.event import Event
from app.views.event_view import (
    render_view_all_events,
    get_event_info,
    show_created_event_success,
    show_created_event_error,
    render_choice_event,
    render_view_event_details,
    show_modified_event_success,
    show_modified_event_error,
    show_events_without_support_collaborator,
    render_choice_support_collaborator,
    show_assigned_event_success,
    show_assigned_event_error,
    render_view_my_events,
    show_no_signed_contracts_available,
)
from app.utils.database_utils import commit_to_db
from app.utils.collaborator_utils import get_collaborators_by_department


class EventController:
    def __init__(self):
        self.permission = Permission()
        self.authenticated_collaborator: Collaborator = self.permission.authenticated_collaborator  # noqa

    def view_events(self):
        if not self.permission.can_read():
            render_access_denied()
            return

        session = Session()

        try:
            events = session.query(Event).all()
            render_view_all_events(events, self.authenticated_collaborator)
        finally:
            session.close()
            Session.remove()

    def create_event(self):
        if not self.permission.can_create_event():
            render_access_denied()
            return

        session = Session()

        try:
            contracts: list[Contract] = get_contracts(session)
            # filter by status 'signed' and by self.authenticated_collaborator
            filtered_contracts = [
                contract for contract in contracts
                if contract.status.name == 'Signed'
                and contract.customer.commercial_id
                == self.authenticated_collaborator.id
            ]
            if not filtered_contracts:
                show_no_signed_contracts_available()
                return

            event_info = get_event_info(
                session, filtered_contracts,
                self.authenticated_collaborator
            )
            event = Event(
                location=event_info["location"],
                attendees=event_info["attendees"],
                notes=event_info["notes"],
                start_date=event_info["start_date"],
                end_date=event_info["end_date"],
                contract_id=event_info["contract_id"],
                collaborator_id=None,
            )
            if commit_to_db(session, event):
                show_created_event_success()

            else:
                show_created_event_error()
        finally:
            session.close()
            Session.remove()

    def read_event(self):
        if not self.permission.can_read():
            render_access_denied()
            return

        session = Session()

        try:
            events = session.query(Event).all()
            event_choice = render_choice_event(
                events,
                self.authenticated_collaborator
            )
            if not event_choice:
                return

            event_object = (
                session.query(Event)
                .filter(Event.id == int(event_choice.split(":")[0]))
                .first()
            )
            if not event_object:
                return
            render_view_event_details(
                event_object,
                self.authenticated_collaborator
            )
        finally:
            session.close()
            Session.remove()

    def modify_event(self):
        if not self.permission.can_modify_event():
            render_access_denied()
            return

        session = Session()
        try:
            events = (
                session.query(Event)
                .filter(
                    Event.collaborator_id == self.authenticated_collaborator.id
                )
                .all()
            )
            # a support collaborator can only modify their own events

            event_choice = render_choice_event(
                events,
                self.authenticated_collaborator
            )
            if not event_choice:
                return

            event_object = (
                session.query(Event)
                .filter(Event.id == int(event_choice.split(":")[0]))
                .first()
            )
            if not event_object:
                return
            if not event_object.collaborator_id == self.authenticated_collaborator.id:  # type: ignore  # noqa: E501
                render_access_denied()
                return

            event_updated = ask_event_modification(event_object)
            if not event_updated:
                return

            # Apply updates to the event object
            for key, value in event_updated.items():
                setattr(event_object, key, value)

            if commit_to_db(session, event_object):
                show_modified_event_success()
            else:
                show_modified_event_error()

        finally:
            session.close()
            Session.remove()

    def assign_support_collaborator_to_event(self):
        if not self.permission.can_assign_support_collaborator_to_event():
            render_access_denied()
            return

        session = Session()
        try:
            events_without_support = (
                session.query(Event).filter(
                    Event.collaborator_id.is_(None)
                ).all()
            )
            if not events_without_support:
                show_events_without_support_collaborator(
                    events_without_support
                )
                return
            event_choice = render_choice_event(
                events_without_support,
                self.authenticated_collaborator
            )
            if not event_choice:
                return

            event_object = (
                session.query(Event)
                .filter(Event.id == int(event_choice.split(":")[0]))
                .first()
            )
            if not event_object:
                return

            collaborators = get_collaborators_by_department(session)
            support_collaborators = [
                collaborator
                for collaborator in collaborators
                if collaborator["departement"] == "Support"
            ]
            collaborator_choice = render_choice_support_collaborator(
                support_collaborators,
                self.authenticated_collaborator
            )
            if not collaborator_choice:
                return
            collaborator_id = int(collaborator_choice.split(":")[0])
            event_object.collaborator_id = int(collaborator_id)  # type: ignore

            if commit_to_db(session, event_object):
                show_assigned_event_success()
            else:
                show_assigned_event_error()

        finally:
            session.close()
            Session.remove()

    def display_my_events(self):
        if not self.permission.can_display_my_events():
            render_access_denied()
            return

        session = Session()

        try:
            events = (
                session.query(Event)
                .filter(Event.collaborator_id == self.authenticated_collaborator.id)  # noqa: E501
                .all()
            )
            render_view_my_events(events, self.authenticated_collaborator)
        finally:
            session.close()
            Session.remove()
