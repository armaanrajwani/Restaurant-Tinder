# Pydantic schemas for restaurant information sent back to the frontend.
# Unlike SQLAlchemy models, schemas describe API data, not database tables.


from pydantic import BaseModel, ConfigDict


# Describes the restaurant fields returned by the API.
class RestaurantResponse(BaseModel):

    restaurant_id: int
    name: str

    cuisine: str | None = None
    price_range: str | None = None
    location: str | None = None
    description: str | None = None
    image_url: str | None = None

# Allow Pydantic to build API responses from SQLAlchemy model objects.
    model_config = ConfigDict(from_attributes=True)
