import sentry_sdk
from sqlalchemy.orm import DeclarativeBase


def commit_to_db(session, model_instance: DeclarativeBase) -> bool:
    """
    Add and commit an instance to the database

    Returns:
        True if the commit was successful, False otherwise
    """
    try:
        session.add(model_instance)
        session.commit()
        return True
    except Exception as e:
        # Even if no explicit transaction seems to have started,
        # rollback prevents issues if something was implicitly flushed.
        session.rollback()
        print(f"Error committing to database: {e}")
        sentry_sdk.capture_exception(e)
        return False
