import os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(__file__).resolve().parent / ".env")

# SQLAlchemy lets Python communicate with the MySQL database.
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base

# Connection settings: which MySQL server and database to use.
# SECURITY NOTE: The original file hardcodes a database password.
# Move credentials to .env before sharing this code or committing it to Git.
DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password=os.environ["MYSQL_PASSWORD"],
    host="localhost",
    port=3306,
    database="dishr_test"
)

# Create the shared connection engine for talking to MySQL.
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# Factory for creating a separate database session for each request.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class inherited by database models such as User and Review.
Base = declarative_base()


# Give a route a database session, then close it when the request finishes.
def get_db():
    # Open a new session.
    db = SessionLocal()

    try:
        # Let FastAPI use this session inside the requested route.
        yield db
    finally:
        # Always close the session, even if the route raises an error.
        db.close()
