from app.utils.status_utils import get_statuses


def test_get_status_utils_success(
        db_session,
):

    statuses = get_statuses(db_session)

    assert len(statuses) == 3
    # 3 status in db signed, unsigned and pending
    assert statuses[0]['name'] == "Pending"
    assert statuses[1]['name'] == "Signed"
    assert statuses[2]['name'] == "Unsigned"
