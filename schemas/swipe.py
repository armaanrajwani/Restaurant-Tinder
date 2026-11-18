# Pydantic schemas for recording and displaying restaurant swipe choices.


from pydantic import BaseModel, ConfigDict
from typing import Literal
from datetime import datetime

# Restrict swipe types to the three choices Dishr supports.
SwipeType = Literal["liked", "disliked", "havent_been"]

# A new swipe request: which restaurant and what choice.
class SwipeCreate(BaseModel):
    restaurant_id: int
    swipe_type: SwipeType

# The swipe record returned by the API.
class SwipeResponse(BaseModel):
    swipe_id: int
    user_id: int
    restaurant_id: int
    swipe_type: SwipeType
    created_at: datetime | None = None

# Allow Pydantic to build API responses from SQLAlchemy model objects.
    model_config = ConfigDict(from_attributes=True)
