
from sqlalchemy import (Column, Integer, ForeignKey, TIMESTAMP, UniqueConstraint, text)
from database import Base


# Records which restaurants each user has bookmarked.
class SavedRestaurant(Base):
    # Maps to the saved_restaurants table.
    __tablename__ = "saved_restaurants"

    # Unique ID for this saved-restaurant entry.
    saved_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    # Identifies the user who saved the restaurant.
    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )

    # Identifies the restaurant they saved.
    restaurant_id = Column(
        Integer,
        ForeignKey("restaurants.restaurant_id"),
        nullable=False
    )

    # Automatically records when the entry was created.
    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )

    # Prevents the same user from saving the same restaurant twice.
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "restaurant_id",
            name="unique_saved_restaurant"
        ),
    )
