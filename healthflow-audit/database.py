from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Remplace avec tes infos : user:password@localhost:port/dbname
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:qwerty@localhost:5433/healthflow_ms"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Fonction utilitaire pour avoir une session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
