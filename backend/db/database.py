from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DB_PATH", "sqlite:///./aria.db")
# If it doesn't start with sqlite:///, we assume it's just a path and prepend it.
if not DB_PATH.startswith("sqlite:///"):
    DB_PATH = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DB_PATH, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
