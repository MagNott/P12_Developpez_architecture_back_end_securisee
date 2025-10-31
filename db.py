from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
import os

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environnement variable is not set.")

engine = create_engine(DATABASE_URL)
engine.connect()

SessionFactory = sessionmaker(bind=engine)

# Creation of a scoped session (isolated by context)
Session = scoped_session(SessionFactory)


BaseModel = declarative_base()
print("Connexion à la base de données réussie.")
