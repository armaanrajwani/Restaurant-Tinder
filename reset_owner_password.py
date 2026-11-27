from getpass import getpass
from database import SessionLocal
from models.user import User
from models.extensions import RestaurantOwner
from services.auth_service import hash_password

email = input("Owner email: ").strip()
password = getpass("New password: ")

with SessionLocal() as db:
    user = db.query(User).filter_by(email=email).first()

    if not user:
        print("User does not exist.")

    elif not db.get(RestaurantOwner, user.user_id):
        print("User is not a restaurant owner.")

    elif len(password) < 12:
        print("Password must be at least 12 characters.")

    else:
        user.password_hash = hash_password(password)
        db.commit()
        print("Password successfully updated.")