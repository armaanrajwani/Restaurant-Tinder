
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.restaurant import Restaurant
from schemas.restaurant import RestaurantResponse


# Groups related API endpoints under one URL prefix.
router = APIRouter(
    prefix="/restaurants",
    tags=["Restaurants"]
)


# --------------------------------------------------
# GET ALL RESTAURANTS
# --------------------------------------------------

@router.get("/", response_model=list[RestaurantResponse])
# Lists restaurants, optionally narrowing results by cuisine and price range.
def get_restaurants(
    cuisine: str | None = None,
    price_range: str | None = None,
    db: Session = Depends(get_db)
):

    # Start with all restaurants; filters below narrow the results.
    query = db.query(Restaurant)

    if cuisine:
        query = query.filter(
            Restaurant.cuisine == cuisine
        )

    if price_range:
        query = query.filter(
            Restaurant.price_range == price_range
        )

    restaurants = query.all()

    return restaurants


# --------------------------------------------------
# GET RESTAURANT BY ID
# --------------------------------------------------

@router.get("/{restaurant_id}", response_model=RestaurantResponse)
# Looks up one restaurant by its unique ID or returns 404 if missing.
def get_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db)
):

    restaurant = db.query(Restaurant).filter(
        Restaurant.restaurant_id == restaurant_id
    ).first()

    if restaurant is None:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    return restaurant
