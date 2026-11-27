
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import get_db
from models.user import User
from models.restaurant import Restaurant
from models.saved import SavedRestaurant
from schemas.saved import (
    SavedRestaurantCreate,
    SavedRestaurantResponse
)
from routes.auth import require_customer


# Groups related API endpoints under one URL prefix.
router = APIRouter(
    prefix="/saved",
    tags=["Saved Restaurants"]
)


# Save a restaurant
@router.post(
    "/",
    response_model=SavedRestaurantResponse,
    status_code=status.HTTP_201_CREATED
)
# Adds a restaurant to the signed-in user’s saved list, avoiding duplicates.
def save_restaurant(
    data: SavedRestaurantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_customer)
):
    restaurant = db.get(Restaurant, data.restaurant_id)

    if restaurant is None:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    existing = (
        db.query(SavedRestaurant)
        .filter(
            SavedRestaurant.user_id == current_user.user_id,
            SavedRestaurant.restaurant_id == data.restaurant_id
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Restaurant already saved"
        )

    saved = SavedRestaurant(
        user_id=current_user.user_id,
        restaurant_id=data.restaurant_id
    )

    db.add(saved)

    try:
        # Save the change to MySQL.
        db.commit()
        # Read back the saved record, including its generated ID.
        db.refresh(saved)
    except IntegrityError:
        # Undo pending changes after a database error.
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Restaurant could not be saved"
        )

    return saved


# View saved restaurants
@router.get(
    "/me",
    response_model=list[SavedRestaurantResponse]
)
# Lists restaurants saved by the current user.
def get_saved_restaurants(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_customer)
):
    saved = (
        db.query(SavedRestaurant)
        .filter(
            SavedRestaurant.user_id == current_user.user_id
        )
        .order_by(SavedRestaurant.saved_id.desc())
        .all()
    )

    return saved


# Remove a saved restaurant
@router.delete("/{restaurant_id}")
# Removes a restaurant from the current user’s saved list.
def remove_saved_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_customer)
):
    saved = (
        db.query(SavedRestaurant)
        .filter(
            SavedRestaurant.user_id == current_user.user_id,
            SavedRestaurant.restaurant_id == restaurant_id
        )
        .first()
    )

    if saved is None:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not saved"
        )

    db.delete(saved)
    # Save the change to MySQL.
    db.commit()

    return {"message": "Restaurant removed from saved list"}
