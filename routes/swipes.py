
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import get_db
from models.user import User
from models.restaurant import Restaurant
from models.swipe import RestaurantSwipe
from schemas.swipe import SwipeCreate, SwipeResponse
from routes.auth import require_customer
from services.swipe_limit import consume_swipe, remaining, today

# Groups related API endpoints under one URL prefix.
router = APIRouter(
    prefix="/swipes",
    tags=["Swipes"]
)


@router.post("/", response_model=SwipeResponse)
# Records a like, dislike, or haven’t-been choice; updates an existing choice.
def create_swipe(
    swipe: SwipeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_customer)
):
    restaurant = db.get(Restaurant, swipe.restaurant_id)

    if restaurant is None:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    consume_swipe(db, current_user.user_id)

    # A user can have only one swipe choice per restaurant.
    existing_swipe = (
        db.query(RestaurantSwipe)
        .filter(
            RestaurantSwipe.user_id == current_user.user_id,
            RestaurantSwipe.restaurant_id == swipe.restaurant_id
        )
        .first()
    )

    if existing_swipe:
        existing_swipe.swipe_type = swipe.swipe_type
        result = existing_swipe
    else:
        result = RestaurantSwipe(
            user_id=current_user.user_id,
            restaurant_id=swipe.restaurant_id,
            swipe_type=swipe.swipe_type
        )
        db.add(result)

    try:
        # Save the change to MySQL.
        db.commit()
        # Read back the saved record, including its generated ID.
        db.refresh(result)
    except IntegrityError:
        # Undo pending changes after a database error.
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Could not save swipe"
        )

    return result


@router.get("/me", response_model=list[SwipeResponse])
# Lists the current user’s recorded restaurant choices.
def get_my_swipes(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_customer)
):
    return (
        db.query(RestaurantSwipe)
        .filter(
            RestaurantSwipe.user_id == current_user.user_id
        )
        .order_by(RestaurantSwipe.swipe_id.desc())
        .all()
    )


@router.delete("/{restaurant_id}")
# Removes the current user’s choice for a specified restaurant.
def delete_swipe(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_customer)
):
    swipe = (
        db.query(RestaurantSwipe)
        .filter(
            RestaurantSwipe.user_id == current_user.user_id,
            RestaurantSwipe.restaurant_id == restaurant_id
        )
        .first()
    )

    if swipe is None:
        raise HTTPException(
            status_code=404,
            detail="Swipe not found"
        )

    db.delete(swipe)
    # Save the change to MySQL.
    db.commit()

    return {"message": "Swipe deleted successfully"}


@router.get('/remaining')
def get_remaining(db: Session = Depends(get_db), current_user: User = Depends(require_customer)):
    left = remaining(db, current_user.user_id)
    return {'limit': 10, 'used': 10-left, 'remaining': left, 'date': today()}
