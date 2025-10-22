from app.validators.event_validator import (
    is_end_date_after_start,
    is_valid_attendees,
    is_valid_date,
    is_valid_location,
    is_valid_notes,

)


def test_valid_location():
    assert is_valid_location("Paris") is True
    assert is_valid_location("") is False
    assert is_valid_location(" " * 5) is False
    assert is_valid_location("A" * 151) is False


def test_valid_attendees():
    assert is_valid_attendees("10") is True
    assert is_valid_attendees("0") is False
    assert is_valid_attendees("-5") is False
    assert is_valid_attendees("abc") is False


def test_invalid_attendees():
    assert is_valid_attendees("ten") is False
    assert is_valid_attendees("") is False
    assert is_valid_attendees(" ") is False


def test_valid_date_format():
    assert is_valid_date("2023-05-20") is True
    assert is_valid_date("20-05-2023") is False
    assert is_valid_date("2023/05/20") is False
    assert is_valid_date("not a date") is False


def test_end_date_after_start():
    assert is_end_date_after_start("2023-05-20", "2023-05-21") is True
    assert is_end_date_after_start("2023-05-20", "2023-05-20") is True
    assert is_end_date_after_start("2023-05-21", "2023-05-20") is False
    assert is_end_date_after_start("invalid-date", "2023-05-20") is False
    assert is_end_date_after_start("2023-05-20", "invalid-date") is False


def test_valid_notes():
    assert is_valid_notes("This is a valid note.") is True
    assert is_valid_notes("") is False
    assert is_valid_notes(" " * 10) is False
    long_note = "a" * 501
    assert is_valid_notes(long_note) is False
