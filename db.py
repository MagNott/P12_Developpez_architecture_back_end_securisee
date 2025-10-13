from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql+psycopg2://p12_user:mdpp12@localhost:5432/p12_db"

engine = create_engine(DATABASE_URL)
engine.connect()

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

BaseModel = declarative_base()
print("Connexion à la base de données réussie.")
