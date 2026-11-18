# Pydantic schemas for creating, editing, and displaying restaurant reviews.
# They also validate ratings so they stay between 1 and 5.


from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


# Information a user submits when writing a new review.
class ReviewCreate(BaseModel):
    restaurant_id: int
    rating: int = Field(ge=1, le=5)
    comment: str | None = None


# Optional fields a user can change on an existing review.
class ReviewUpdate(BaseModel):
    rating: int | None = Field(default=None, ge=1, le=5)
    comment: str | None = None


# Review information returned to the frontend.
class ReviewResponse(BaseModel):
    review_id: int
    user_id: int
    restaurant_id: int
    rating: int
    comment: str | None
    created_at: datetime | None = None

# Allow Pydantic to build API responses from SQLAlchemy model objects.
    model_config = ConfigDict(from_attributes=True)


# Summary of a restaurant’s average rating and review count.
class RestaurantRatingResponse(BaseModel):
    restaurant_id: int
    average_rating: float | None
    total_reviews: int
