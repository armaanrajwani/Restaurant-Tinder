
import os
# Tools for calculating when a login token expires.
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from pathlib import Path
# Library used to securely hash and verify passwords.
from pwdlib import PasswordHash

# Read private settings (including the JWT secret) from the project .env file.
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# Use the library-recommended password hashing method.
password_hasher = PasswordHash.recommended()

# Secret key used to sign tokens so they cannot be altered undetected.
JWT_SECRET = os.environ["JWT_SECRET"]
# Algorithm used to sign and verify JWT login tokens.
JWT_ALGORITHM = "HS256"
# Tokens stop being valid after this many minutes.
TOKEN_EXPIRATION_MINUTES = 60


# Convert a plain-text password into a secure hash before saving it.
def hash_password(password: str) -> str:
    return password_hasher.hash(password)


# Compare a login password with the stored hash without storing plain text.
def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return password_hasher.verify(
        plain_password,
        hashed_password
    )


# Make a signed login token that identifies a user for a limited time.
def create_access_token(user_id: int) -> str:
    # Calculate the expiry time in UTC.
    expiration = datetime.now(timezone.utc) + timedelta(
        minutes=TOKEN_EXPIRATION_MINUTES
    )

    # The token contains the user ID (subject) and expiry time.
    payload = {
        "sub": str(user_id),
        "exp": expiration
    }

    # Sign the token with the secret key and return it to the login route.
    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )
