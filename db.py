from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

# if os.getenv("ENV_TEST") == "true":
#     DATABASE_URL = "sqlite:///:memory:"
# else:
DATABASE_URL = "postgresql+psycopg2://p12_user:mdpp12@localhost:5432/p12_db"

engine = create_engine(DATABASE_URL)
engine.connect()

SessionFactory = sessionmaker(bind=engine)

# Creation of a scoped session (isolated by context)
Session = scoped_session(SessionFactory)


BaseModel = declarative_base()
print("Connexion à la base de données réussie.")
