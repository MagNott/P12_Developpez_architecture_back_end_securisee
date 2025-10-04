# initialize the database and create tables

from db import engine, Base
from app.models.user import User  # noqa: F401
from app.models.customer import Customer  # noqa: F401
from app.models.collaborator import Collaborator  # noqa: F401
from app.models.contract import Contract  # noqa: F401
from app.models.event import Event  # noqa: F401
from app.models.department import Department  # noqa: F401
from app.models.status import Status  # noqa: F401
from sqlalchemy.schema import CreateTable

Base.metadata.create_all(bind=engine)
print("Tables créées avec succès.")

for table in Base.metadata.tables.values():
    print(CreateTable(table).compile(engine))
