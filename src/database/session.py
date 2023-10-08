from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
from src.database.db_config import DB_CONFIG

engine = create_engine(DB_CONFIG.DB_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    db = SessionLocal()
    db.current_user_id = None
    try:
        yield db
    finally:
        db.close()
