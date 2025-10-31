from datetime import datetime


def is_valid_location(location) -> bool:
    return bool(location.strip()) and len(location) <= 150


def is_valid_attendees(attendees) -> bool:
    attendees = attendees.strip()
    return attendees.isdigit() and int(attendees) > 0


def is_valid_notes(notes) -> bool:
    return bool(notes.strip()) and len(notes) <= 500


def is_valid_start_date(date_str) -> bool:
    try:
        object_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        now = datetime.now().date()
        if object_date < now:
            return False
        return True
    except ValueError:
        return False


def is_valid_date(date_str) -> bool:
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def is_end_date_after_start(start_str, end_str) -> bool:
    try:
        start = datetime.strptime(start_str, "%Y-%m-%d")
        end = datetime.strptime(end_str, "%Y-%m-%d")
        return end >= start
    except ValueError:
        return False
