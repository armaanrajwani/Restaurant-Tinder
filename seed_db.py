from sqlalchemy import text
from database import SessionLocal, engine
from models.user import User
from models.swipe import RestaurantSwipe
from models.saved import SavedRestaurant
from models.review import Review
from services.auth_service import hash_password


def run_seed():
    # 1. Execute the SQL schema and 40 restaurants
    with open("dishr_seed.sql", "r", encoding="utf-8") as f:
        sql_script = f.read()

    raw_conn = engine.raw_connection()
    try:
        cursor = raw_conn.cursor()
        for statement in sql_script.split(";"):
            stmt = statement.strip()
            if stmt:
                cursor.execute(stmt)
        raw_conn.commit()
        cursor.close()
    finally:
        raw_conn.close()

    # 2. Seed users with valid pwdlib Argon2 hashes + activity
    db = SessionLocal()
    try:
        hashed_pw = hash_password("Password123!")

        users = [
            User(user_id=1, username="Armaan Rajwani", email="armaan@dishr.ca", password_hash=hashed_pw),
            User(user_id=2, username="Sarah Jenkins", email="sarah.j@dishr.ca", password_hash=hashed_pw),
            User(user_id=3, username="Marcus Chen", email="marcus.c@dishr.ca", password_hash=hashed_pw),
        ]
        db.add_all(users)
        db.commit()

        # Populate customers & preferences
        db.execute(text("INSERT INTO customers (user_id) VALUES (1), (2), (3)"))
        db.execute(text("""
            INSERT INTO user_preferences (user_id, cuisine_preference, price_min, price_max, location_radius_km)
            VALUES (1, 'Indian', 1, 3, 10), (2, 'Seafood', 2, 4, 5), (3, 'Japanese', 1, 3, 15)
        """))

        # Seed swipes (using exact Pydantic literals: liked / disliked / havent_been)
        swipes = [
            RestaurantSwipe(user_id=1, restaurant_id=1, swipe_type="liked"),
            RestaurantSwipe(user_id=1, restaurant_id=21, swipe_type="liked"),
            RestaurantSwipe(user_id=1, restaurant_id=24, swipe_type="liked"),
            RestaurantSwipe(user_id=1, restaurant_id=32, swipe_type="liked"),
            RestaurantSwipe(user_id=1, restaurant_id=39, swipe_type="liked"),
            RestaurantSwipe(user_id=1, restaurant_id=3, swipe_type="havent_been"),
            RestaurantSwipe(user_id=1, restaurant_id=38, swipe_type="disliked"),
            RestaurantSwipe(user_id=2, restaurant_id=1, swipe_type="liked"),
            RestaurantSwipe(user_id=2, restaurant_id=2, swipe_type="liked"),
            RestaurantSwipe(user_id=2, restaurant_id=13, swipe_type="liked"),
            RestaurantSwipe(user_id=3, restaurant_id=27, swipe_type="liked"),
            RestaurantSwipe(user_id=3, restaurant_id=28, swipe_type="liked"),
        ]
        db.add_all(swipes)

        # Seed saved restaurants
        saves = [
            SavedRestaurant(user_id=1, restaurant_id=1),
            SavedRestaurant(user_id=1, restaurant_id=24),
            SavedRestaurant(user_id=1, restaurant_id=32),
            SavedRestaurant(user_id=2, restaurant_id=13),
            SavedRestaurant(user_id=3, restaurant_id=28),
        ]
        db.add_all(saves)

        # Seed reviews
        reviews = [
            Review(user_id=1, restaurant_id=1, rating=5, comment="Incredible pasta and waterfront views. Angry lobster spaghetti is a must."),
            Review(user_id=2, restaurant_id=1, rating=4, comment="Great atmosphere and service, definitely book a reservation in advance."),
            Review(user_id=1, restaurant_id=24, rating=5, comment="Best butter chicken and garlic naan in the North End. Cocktails are great too."),
            Review(user_id=1, restaurant_id=32, rating=4, comment="Fun vibe on Argyle Street and awesome birria tacos."),
            Review(user_id=2, restaurant_id=13, rating=5, comment="Hands down the best cocktails and fresh seafood plates in Halifax."),
            Review(user_id=3, restaurant_id=28, rating=5, comment="Rich broth and chewy noodles—perfect on a cold Halifax evening."),
        ]
        db.add_all(reviews)
        db.commit()

        print("Database built successfully: 40 Halifax restaurants, 3 users, 12 swipes, 5 saves, 6 reviews.")
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()