from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from database import Base

class RestaurantOwner(Base):
    __tablename__ = 'restaurant_owners'
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    business_name = Column(String(150))

class Customer(Base):
    __tablename__ = 'customers'
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)

class DailySwipeUsage(Base):
    __tablename__ = 'daily_swipe_usage'
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    swipe_date = Column(Date, primary_key=True)
    used = Column(Integer, nullable=False, default=0)

class Promotion(Base):
    __tablename__ = 'restaurant_promotions'
    promotion_id = Column(Integer, primary_key=True, autoincrement=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.restaurant_id'), nullable=False)
    owner_id = Column(Integer, ForeignKey('restaurant_owners.user_id'), nullable=False)
    payment_reference = Column(String(255), unique=True, nullable=False)
    starts_at = Column(DateTime, nullable=False)
    ends_at = Column(DateTime, nullable=False)
