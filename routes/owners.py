from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.extensions import RestaurantOwner
from models.restaurant import Restaurant
from schemas.owner import RestaurantUpdate
from schemas.user import UserLogin, TokenResponse
from schemas.restaurant import RestaurantResponse
from services.auth_service import verify_password, create_access_token
from routes.auth import require_owner

router = APIRouter(prefix='/owners', tags=['Restaurant owners'])

@router.post('/login', response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=str(data.email)).first()
    if not user or not db.get(RestaurantOwner, user.user_id) or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, 'Invalid owner credentials')
    return TokenResponse(access_token=create_access_token(user.user_id))

def owned_restaurant(db, user_id, restaurant_id):
    restaurant = db.get(Restaurant, restaurant_id)
    if not restaurant or restaurant.owner_id != user_id:
        raise HTTPException(404, 'Owned restaurant not found')
    return restaurant

@router.get('/restaurants', response_model=list[RestaurantResponse])
def list_owned(db: Session = Depends(get_db), user: User = Depends(require_owner)):
    return db.query(Restaurant).filter_by(owner_id=user.user_id).all()

@router.patch('/restaurants/{restaurant_id}', response_model=RestaurantResponse)
def update(restaurant_id: int, data: RestaurantUpdate, db: Session = Depends(get_db), user: User = Depends(require_owner)):
    restaurant = owned_restaurant(db, user.user_id, restaurant_id)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(restaurant, key, value)
    db.commit()
    db.refresh(restaurant)
    return restaurant
