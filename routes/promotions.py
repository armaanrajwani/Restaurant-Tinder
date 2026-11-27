import os
import uuid
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.extensions import Promotion
from routes.auth import require_owner
from routes.owners import owned_restaurant

router = APIRouter(prefix='/promotions', tags=['Promotions'])

@router.post('/test-purchase/{restaurant_id}', status_code=201)
def test_purchase(restaurant_id: int, db: Session = Depends(get_db), user: User = Depends(require_owner)):
    # Explicit demo mode only. Never represents a real payment.
    if os.getenv('ENABLE_TEST_PROMOTIONS') != 'true':
        raise HTTPException(403, 'Test promotions disabled')
    owned_restaurant(db, user.user_id, restaurant_id)
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    promotion = Promotion(restaurant_id=restaurant_id, owner_id=user.user_id, payment_reference='test-'+uuid.uuid4().hex, starts_at=now, ends_at=now+timedelta(days=7))
    db.add(promotion)
    db.commit()
    db.refresh(promotion)
    return {'promotion_id': promotion.promotion_id, 'test_payment': True, 'ends_at_utc': promotion.ends_at}
