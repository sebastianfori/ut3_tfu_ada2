from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from contextlib import contextmanager

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://app:app@localhost:5432/recipes")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

@contextmanager
def get_session():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
