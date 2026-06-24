from dotenv import load_dotenv
load_dotenv()

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. The engine — the actual connection to PostgreSQL
engine = create_engine(os.getenv("DATABASE_URL"))

# 2. SessionLocal — a factory that creates database sessions
# A "session" is like a transaction: you open it, do stuff, commit or rollback
SessionLocal = sessionmaker(bind=engine)

# 3. Base — the class all your models will inherit from
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
