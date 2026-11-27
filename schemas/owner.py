from pydantic import BaseModel, Field, ConfigDict
from typing import Literal

class RestaurantUpdate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    name: str = Field(default=None, min_length=1, max_length=150)
    cuisine: str = Field(default=None, min_length=1, max_length=100)
    price_range: Literal['$', '$$', '$$$', '$$$$'] = None
    location: str = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    image_url: str | None = Field(default=None, max_length=500)
