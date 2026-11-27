from collections import defaultdict
from datetime import datetime, timezone
from sqlalchemy import func
from models.restaurant import Restaurant
from models.review import Review
from models.swipe import RestaurantSwipe
from models.extensions import Promotion

def recommend(db, user_id, limit):
    # Count reviews separately to avoid multiplying rows through joins.
    counts = dict(db.query(Review.restaurant_id, func.count(Review.review_id)).group_by(Review.restaurant_id).all())
    maximum = max(counts.values(), default=1)
    history = db.query(RestaurantSwipe, Restaurant.cuisine).join(Restaurant, Restaurant.restaurant_id == RestaurantSwipe.restaurant_id).filter(RestaurantSwipe.user_id == user_id).all()
    seen = {s.restaurant_id for s, _ in history}
    preferences = defaultdict(lambda: [0, 0])
    for swipe, cuisine in history:
        if swipe.swipe_type in ('liked', 'disliked'):
            pair = preferences[(cuisine or '').strip().casefold()]
            pair[0] += int(swipe.swipe_type == 'liked')
            pair[1] += 1
    weight = min(.7, max(0, (len(history)-10)*.7/20))
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    promoted = {r[0] for r in db.query(Promotion.restaurant_id).filter(Promotion.starts_at <= now, Promotion.ends_at > now).all()}
    results = []
    for restaurant in db.query(Restaurant).all():
        rid = restaurant.restaurant_id
        if rid in seen:
            continue
        likes, total = preferences[(restaurant.cuisine or '').strip().casefold()]
        preference = (likes+1)/(total+2)
        score = (1-weight)*counts.get(rid, 0)/maximum + weight*preference + .25*(rid in promoted)
        results.append((restaurant, counts.get(rid, 0), rid in promoted, score))
    results.sort(key=lambda r: (-r[3], -r[1], r[0].restaurant_id))
    return results[:limit]
