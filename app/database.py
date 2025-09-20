from psycopg2 import connect
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session, sessionmaker

engine = create_engine('postgresql://admin:12345@localhost:5433/db0')
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


