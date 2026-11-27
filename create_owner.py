"""Trusted local provisioning tool. Never expose this script as an API endpoint."""
import secrets
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from database import SessionLocal
from models.user import User
from models.extensions import RestaurantOwner
from models.restaurant import Restaurant
from schemas.user import UserCreate
from services.auth_service import hash_password
from pydantic import ValidationError


def main():
    try:
        restaurant_id = int(input('Existing restaurant ID: '))
        username = input('Owner name: ').strip()
        email = input('Owner email: ').strip()
        business_name = input('Business name: ').strip()
        if not 1 <= len(business_name) <= 150:
            raise ValueError('Business name must contain 1–150 characters.')
        password = secrets.token_urlsafe(24)
        data = UserCreate(username=username, email=email, password=password)
        if len(str(data.email)) > 255:
            raise ValueError('Email is too long.')
        with SessionLocal() as db:
            with db.begin():
                # Lock the existing restaurant to prevent simultaneous assignments.
                restaurant = db.execute(select(Restaurant).where(
                    Restaurant.restaurant_id == restaurant_id
                ).with_for_update()).scalar_one_or_none()
                if restaurant is None:
                    raise ValueError('Restaurant does not exist.')
                if restaurant.owner_id is not None:
                    raise ValueError('Restaurant already has an owner.')
                if db.query(User).filter_by(email=str(data.email)).first():
                    raise ValueError('Email already registered. Use a separate owner email.')
                print(f'Assign ownership of {restaurant.name} (ID {restaurant_id})?')
                if input('Type VERIFIED to confirm external verification: ') != 'VERIFIED':
                    print('Cancelled; no changes made.')
                    return
                user = User(username=data.username, email=str(data.email),
                            password_hash=hash_password(password))
                db.add(user)
                db.flush()
                db.add(RestaurantOwner(user_id=user.user_id, business_name=business_name))
                db.flush()
                restaurant.owner_id = user.user_id
                owner_id = user.user_id
            # Only disclose credentials after the transaction commits.
            print(f'Owner created: {owner_id}; restaurant: {restaurant_id}')
            print(f'Login email: {data.email}')
            print(f'Generated password: {password}')
            print('Deliver securely; do not commit or log this password.')
    except (ValueError, ValidationError) as exc:
        print('Account not created: invalid input or assignment. ' + (str(exc) if not isinstance(exc, ValidationError) else 'Check name and email.'))
        return 1
    except IntegrityError:
        print('Account not created: database constraint conflict.')
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
