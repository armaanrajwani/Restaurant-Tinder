
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, text, UniqueConstraint
from database import Base

# Records a user's choice for a restaurant (like/dislike/haven't been).
class RestaurantSwipe(Base):
    # Maps this class to the restaurant_swipes table.
    __tablename__ = "restaurant_swipes"

    # Unique ID for a swipe record.
    swipe_id = Column(Integer, primary_key=True, autoincrement=True)

    # The user who made this choice.
    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )

    # The restaurant this choice applies to.
    restaurant_id = Column(
        Integer,
        ForeignKey("restaurants.restaurant_id"),
        nullable=False
    )

    # Stores the choice; API validation limits the allowed values.
    swipe_type = Column(
        String(20),
        nullable=False
    )

    # MySQL sets the timestamp when a swipe is first saved.
    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )

    # Allows only one swipe record per user/restaurant pair.
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "restaurant_id",
            name="unique_user_restaurant"
        ),
    )
