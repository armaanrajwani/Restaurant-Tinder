from datetime import datetime
from zoneinfo import ZoneInfo
from fastapi import HTTPException
from sqlalchemy.dialects.mysql import insert
from models.extensions import DailySwipeUsage

LIMIT = 10

def today():
    return datetime.now(ZoneInfo('America/Halifax')).date()

def consume_swipe(db, user_id):
    # Atomic upsert locks the daily counter even for simultaneous requests.
    day = today()
    stmt = insert(DailySwipeUsage).values(user_id=user_id, swipe_date=day, used=0)
    db.execute(stmt.on_duplicate_key_update(used=DailySwipeUsage.used))
    row = db.query(DailySwipeUsage).filter_by(user_id=user_id, swipe_date=day).with_for_update().one()
    if row.used >= LIMIT:
        db.rollback()
        raise HTTPException(429, 'Daily swipe limit reached')
    row.used += 1

def remaining(db, user_id):
    row = db.get(DailySwipeUsage, (user_id, today()))
    return LIMIT - (row.used if row else 0)
