# Pydantic schemas for saving restaurants and returning saved records.


from pydantic import BaseModel, ConfigDict
from datetime import datetime


# Only the restaurant ID is needed to save a restaurant.
class SavedRestaurantCreate(BaseModel):
    restaurant_id: int


# Saved record returned after saving or listing favourites.
class SavedRestaurantResponse(BaseModel):
    saved_id: int
    user_id: int
    restaurant_id: int
    created_at: datetime | None = None

# Allow Pydantic to build API responses from SQLAlchemy model objects.
    model_config = ConfigDict(from_attributes=True)
