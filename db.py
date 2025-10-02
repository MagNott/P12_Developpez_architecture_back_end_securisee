from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg2://p12_user:mdpp12@localhost:5432/p12_db"

engine = create_engine(DATABASE_URL)
engine.connect()
print("Connexion à la base de données réussie.")