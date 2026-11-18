# Pydantic schemas for account registration, login, and API responses.
# These help ensure private password data is not returned in user profiles.


from pydantic import BaseModel, ConfigDict, EmailStr, Field


# Registration details supplied when a user creates an account.
class UserCreate(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8)


# Credentials submitted when logging in.
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Public account details returned to the client (no password hash).
class UserResponse(BaseModel):
    user_id: int
    username: str
    email: EmailStr

# Allow Pydantic to build API responses from SQLAlchemy model objects.
    model_config = ConfigDict(from_attributes=True)


# The access token returned after a successful login.
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
