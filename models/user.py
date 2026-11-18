
from sqlalchemy import Column, Integer, String, DateTime
from database import Base

# Represents a registered Dishr user account.
class User(Base):
    # Connects this class to the users table in MySQL.
    __tablename__ = "users"

    # Unique ID assigned automatically when a user registers.
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    # Python calls this username, but the MySQL column is named "name".
    username = Column("name", String(100), nullable=False)
    # Email is required and must be unique across accounts.
    email = Column(String(255), unique=True, nullable=False)
    # Stores a hashed password, never the original plaintext password.
    password_hash = Column(String(255), nullable=False)
    # Date and time the account was created (if available).
    created_at = Column(DateTime, nullable=True)
