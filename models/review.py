
from sqlalchemy import Column, Integer, SmallInteger, Text, ForeignKey, TIMESTAMP, text
from database import Base


# Represents a rating and optional written review of a restaurant.
class Review(Base):
    # Maps this Python class to the existing reviews table.
    __tablename__ = "reviews"
    # Database-generated unique ID for each review.
    review_id = Column(Integer, primary_key=True, autoincrement=True)

    # The user who wrote the review; must exist in users.
    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )

    # The restaurant being reviewed; must exist in restaurants.
    restaurant_id = Column(
        Integer,
        ForeignKey("restaurants.restaurant_id"),
        nullable=False
    )

    # Numeric rating; the API schema and MySQL constraint enforce 1–5.
    rating = Column(SmallInteger, nullable=False)
    # Optional written feedback.
    comment = Column(Text, nullable=True)

    # MySQL supplies the creation time when the review is inserted.
    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=True
    )
