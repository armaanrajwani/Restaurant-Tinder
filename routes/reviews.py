
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from models.user import User
from models.restaurant import Restaurant
from models.review import Review
from schemas.review import (
    ReviewCreate,
    ReviewUpdate,
    ReviewResponse,
    RestaurantRatingResponse
)
from routes.auth import require_customer


# Groups related API endpoints under one URL prefix.
router = APIRouter(
    prefix="/reviews",
    tags=["Reviews and Ratings"]
)


# Create a review
@router.post(
    "/",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED
)
# Checks that the restaurant exists, then saves a review for the signed-in user.
def create_review(
    data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_customer)
):
    restaurant = db.get(Restaurant, data.restaurant_id)

    if restaurant is None:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    review = Review(
        user_id=current_user.user_id,
        restaurant_id=data.restaurant_id,
        rating=data.rating,
        comment=data.comment
    )

    db.add(review)
    # Save the change to MySQL.
    db.commit()
    # Read back the saved record, including its generated ID.
    db.refresh(review)

    return review


# View reviews written by current user
@router.get("/me", response_model=list[ReviewResponse])
# Returns only the reviews written by the current user.
def get_my_reviews(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_customer)
):
    return (
        db.query(Review)
        .filter(Review.user_id == current_user.user_id)
        .order_by(Review.review_id.desc())
        .all()
    )


# View reviews for a restaurant
@router.get(
    "/restaurant/{restaurant_id}",
    response_model=list[ReviewResponse]
)
# Returns reviews belonging to a specified restaurant.
def get_restaurant_reviews(
    restaurant_id: int,
    db: Session = Depends(get_db)
):
    restaurant = db.get(Restaurant, restaurant_id)

    if restaurant is None:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    return (
        db.query(Review)
        .filter(Review.restaurant_id == restaurant_id)
        .order_by(Review.review_id.desc())
        .all()
    )


# Get average rating for a restaurant
@router.get(
    "/restaurant/{restaurant_id}/rating",
    response_model=RestaurantRatingResponse
)
# Calculates the average star rating and number of reviews for one restaurant.
def get_restaurant_rating(
    restaurant_id: int,
    db: Session = Depends(get_db)
):
    restaurant = db.get(Restaurant, restaurant_id)

    if restaurant is None:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    # Ask MySQL to calculate the average rating and review count.
    average, count = (
        db.query(
            func.avg(Review.rating),
            func.count(Review.review_id)
        )
        .filter(Review.restaurant_id == restaurant_id)
        .one()
    )

    return {
        "restaurant_id": restaurant_id,
        "average_rating": round(float(average), 2) if average is not None else None,
        "total_reviews": count
    }


# Update your own review
@router.put("/{review_id}", response_model=ReviewResponse)
# Changes an existing review only if it belongs to the signed-in user.
def update_review(
    review_id: int,
    data: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_customer)
):
    review = db.get(Review, review_id)

    if review is None:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    if review.user_id != current_user.user_id:
        raise HTTPException(
            status_code=403,
            detail="You can only edit your own reviews"
        )

    # Only change fields explicitly supplied in the update request.
    updates = data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(review, field, value)

    # Save the change to MySQL.
    db.commit()
    # Read back the saved record, including its generated ID.
    db.refresh(review)

    return review


# Delete your own review
@router.delete("/{review_id}")
# Deletes an existing review only if it belongs to the signed-in user.
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_customer)
):
    review = db.get(Review, review_id)

    if review is None:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    if review.user_id != current_user.user_id:
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own reviews"
        )

    db.delete(review)
    # Save the change to MySQL.
    db.commit()

    return {"message": "Review deleted successfully"}
