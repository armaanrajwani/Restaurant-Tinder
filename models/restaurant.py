
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from database import Base


# Represents one restaurant stored in the MySQL restaurants table.
class Restaurant(Base):
    # SQLAlchemy uses this exact table name when querying MySQL.
    __tablename__ = "restaurants"
    # Unique identifier for each restaurant.
    restaurant_id = Column(Integer, primary_key=True)

    # Optional link to the restaurant owner in the restaurant_owners table.
    owner_id = Column(
        Integer,
        ForeignKey("restaurant_owners.user_id"),
        nullable=True
    )

    # Restaurant name is required; the remaining descriptive fields are optional.
    name = Column(String(150), nullable=False)
    # Type of food served (for example, Italian or Japanese).
    cuisine = Column(String(100))
    # Short price category used for filtering restaurants.
    price_range = Column(String(4))
    # Restaurant address or location description.
    location = Column(String(255))
    # Longer description of the restaurant.
    description = Column(Text)
    # Link to an image displayed by the frontend.
    image_url = Column(String(500))
