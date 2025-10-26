from app.utils.department_utils import get_departments


def test_get_departments_success(
        db_session,
):

    departments = get_departments(db_session)

    assert len(departments) == 3
    # There is 3 departments management, sales, support
    assert departments[0]["name"] == "Management"
    assert departments[1]["name"] == "Support"
    assert departments[2]["name"] == "Sales"
