
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from routes.auth import require_customer
from services.recommendation import recommend
from services.swipe_limit import remaining
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

@router.get('/recommended')
def recommended(db: Session = Depends(get_db), user: User = Depends(require_customer)):
    return [dict(RestaurantResponse.model_validate(r).model_dump(), review_count=n, sponsored=p, score=round(score, 4)) for r,n,p,score in recommend(db, user.user_id, remaining(db, user.user_id))]


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
