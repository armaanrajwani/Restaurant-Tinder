
import jwt

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import get_db
from models.user import User
from models.extensions import Customer, RestaurantOwner
from schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
    TokenResponse
)
from services.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
    JWT_SECRET,
    JWT_ALGORITHM
)


# Groups related API endpoints under one URL prefix.
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# Reads the Bearer token sent in the Authorization header.
bearer_scheme = HTTPBearer()


# REGISTER A USER
@router.post("/register", response_model=UserResponse, status_code=201)
# Registers a new account, checking email uniqueness and securely hashing the password.
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.email == str(user_data.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    new_user = User(
        username=user_data.username,
        email=str(user_data.email),
        password_hash=hash_password(user_data.password)
    )

    db.add(new_user)

    try:
        # Save the change to MySQL.
        db.flush()
        db.add(Customer(user_id=new_user.user_id))
        db.commit()
    except IntegrityError:
        # Undo pending changes after a database error.
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Could not register user"
        )

    # Read back the saved record, including its generated ID.
    db.refresh(new_user)

    return new_user


# LOGIN
@router.post("/login", response_model=TokenResponse)
# Checks email/password and issues a signed access token for later requests.
def login_user(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == str(login_data.email)
    ).first()

    if not user or not verify_password(
        login_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(user.user_id)

    return TokenResponse(access_token=token)


# GET CURRENT USER
@router.get("/me", response_model=UserResponse)
# Validates the bearer token and loads the user making the request.
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(
            credentials.credentials,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM]
        )

        user_id = int(payload["sub"])

    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    user = db.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user


def require_customer(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not db.get(Customer, current_user.user_id):
        raise HTTPException(403, 'Customer account required')
    return current_user

def require_owner(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not db.get(RestaurantOwner, current_user.user_id):
        raise HTTPException(403, 'Restaurant owner account required')
    return current_user
