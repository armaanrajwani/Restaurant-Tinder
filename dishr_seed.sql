-- Dishr MySQL 8.0+ Complete Schema & 40-Restaurant Halifax Seed
-- Aligned 100% with SQLAlchemy models and Pydantic schemas

DROP DATABASE IF EXISTS dishr_test;
CREATE DATABASE dishr_test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE dishr_test;

-- 1. USERS (Matches models/user.py & routes/auth.py)
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. ROLE & PREFERENCE TABLES (Relational completeness)
CREATE TABLE customers (
    user_id INT PRIMARY KEY,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE restaurant_owners (
    user_id INT PRIMARY KEY,
    business_name VARCHAR(150),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE user_preferences (
    preference_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    cuisine_preference VARCHAR(100),
    price_min INT,
    price_max INT,
    location_radius_km INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    CHECK (price_min IS NULL OR price_min BETWEEN 1 AND 4),
    CHECK (price_max IS NULL OR price_max BETWEEN 1 AND 4)
);

-- 3. RESTAURANTS (Matches models/restaurant.py & schemas/restaurant.py)
CREATE TABLE restaurants (
    restaurant_id INT AUTO_INCREMENT PRIMARY KEY,
    owner_id INT NULL,
    name VARCHAR(150) NOT NULL,
    cuisine VARCHAR(100) NOT NULL,
    price_range VARCHAR(4) NOT NULL,
    location VARCHAR(255) NOT NULL,
    description TEXT,
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES restaurant_owners(user_id) ON DELETE SET NULL,
    CHECK (price_range IN ('$', '$$', '$$$', '$$$$'))
);

-- 4. RESTAURANT SWIPES (Matches models/swipe.py & schemas/swipe.py)
CREATE TABLE restaurant_swipes (
    swipe_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    restaurant_id INT NOT NULL,
    swipe_type VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_user_restaurant UNIQUE (user_id, restaurant_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id) ON DELETE CASCADE,
    CHECK (swipe_type IN ('liked', 'disliked', 'havent_been'))
);

-- 5. SAVED RESTAURANTS (Matches models/saved.py & schemas/saved.py)
CREATE TABLE saved_restaurants (
    saved_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    restaurant_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_saved_restaurant UNIQUE (user_id, restaurant_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id) ON DELETE CASCADE
);

-- 6. REVIEWS (Matches models/review.py & schemas/review.py)
CREATE TABLE reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    restaurant_id INT NOT NULL,
    rating TINYINT NOT NULL,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id) ON DELETE CASCADE,
    CHECK (rating BETWEEN 1 AND 5)
);

-- ============================================================================
-- SEED DATA: 40 REAL HALIFAX RESTAURANTS
-- ============================================================================
INSERT INTO restaurants (restaurant_id, owner_id, name, cuisine, price_range, location, description, image_url) VALUES
(46, NULL, 'The Brooklyn Warehouse', 'Canadian', '$$$', 'Windsor Street, Halifax, NS', 'Seasonal local bistro fare.', 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800'),
(47, NULL, 'The Armview Restaurant & Lounge', 'Canadian', '$$', 'Chebucto Road, Halifax, NS', 'Diner classics and comfort food.', 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800'),
(48, NULL, 'The Coastal Cafe', 'Canadian', '$$', 'Robie Street, Halifax, NS', 'Breakfast and brunch dishes.', 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800'),
(49, NULL, 'Robie Street Station', 'Canadian', '$$', 'Robie Street, Halifax, NS', 'Breakfast and casual meals.', 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800'),
(50, NULL, 'The Ardmore Tea Room', 'Canadian', '$', 'Quinpool Road, Halifax, NS', 'Traditional diner breakfast.', 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800'),
(51, NULL, 'The Westcliff Restaurant', 'Canadian', '$', 'Oxford Street, Halifax, NS', 'Classic diner meals.', 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800'),
(52, NULL, 'The Cheeky Neighbour Diner', 'Canadian', '$$', 'Quinpool Road, Halifax, NS', 'Brunch and diner classics.', 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800'),
(53, NULL, 'The Osney Cafe & Social', 'Canadian', '$$', 'Charles Street, Halifax, NS', 'Cafe meals and brunch.', 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800'),
(54, NULL, 'The Summit Cafe', 'Canadian', '$', 'Lower Water Street, Halifax, NS', 'Breakfast and lunch fare.', 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800'),
(55, NULL, 'The Brown Hound Public House', 'Pub', '$$', 'Halifax, NS', 'Pub comfort food.', 'https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800'),
(56, NULL, 'The Henry House', 'Pub', '$$', 'Barrington Street, Halifax, NS', 'Traditional pub dishes.', 'https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800'),
(57, NULL, 'The Old Triangle Irish Alehouse', 'Pub', '$$', 'Prince Street, Halifax, NS', 'Irish pub fare.', 'https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800'),
(58, NULL, 'The Maxwell''s Plum', 'Pub', '$$', 'Grafton Street, Halifax, NS', 'Casual pub meals.', 'https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800'),
(59, NULL, 'Your Father''s Moustache', 'Pub', '$$', 'Spring Garden Road, Halifax, NS', 'Pub classics and burgers.', 'https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800'),
(60, NULL, 'The Split Crow Pub', 'Pub', '$$', 'Granville Street, Halifax, NS', 'Traditional tavern fare.', 'https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800'),
(61, NULL, 'The Lower Deck', 'Pub', '$$', 'Upper Water Street, Halifax, NS', 'Maritime pub food.', 'https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800'),
(62, NULL, 'The Auction House', 'Pub', '$$', 'Argyle Street, Halifax, NS', 'Gastropub comfort dishes.', 'https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800'),
(63, NULL, 'The Foggy Goggle', 'Pub', '$$', 'Gottingen Street, Halifax, NS', 'Casual pub dishes.', 'https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800'),
(64, NULL, 'The Lion''s Head Tavern', 'Pub', '$$', 'Robie Street, Halifax, NS', 'Neighborhood tavern fare.', 'https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800'),
(65, NULL, 'The Midtown Tavern', 'Pub', '$$', 'Halifax, NS', 'Traditional tavern meals.', 'https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800'),
(66, NULL, 'McKelvie''s', 'Seafood', '$$$', 'Lower Water Street, Halifax, NS', 'Atlantic seafood dishes.', 'https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800'),
(67, NULL, 'Salty''s', 'Seafood', '$$$', 'Upper Water Street, Halifax, NS', 'Waterfront seafood meals.', 'https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800'),
(68, NULL, 'The Waterfront Warehouse', 'Seafood', '$$$', 'Lower Water Street, Halifax, NS', 'Lobster and seafood dishes.', 'https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800'),
(69, NULL, 'The Bluenose II Restaurant', 'Seafood', '$$', 'Hollis Street, Halifax, NS', 'Seafood and diner classics.', 'https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800'),
(70, NULL, 'Shuck Seafood + Raw Bar', 'Seafood', '$$$', 'Salter Street, Halifax, NS', 'Oysters and seafood.', 'https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800'),
(71, NULL, 'The Sea Smoke Restaurant & Bar', 'Seafood', '$$$', 'Lower Water Street, Halifax, NS', 'Seafood and sushi-inspired dishes.', 'https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800'),
(72, NULL, 'Sushi Nami Royale', 'Japanese', '$$', 'Halifax, NS', 'Sushi and Japanese dishes.', 'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=800'),
(73, NULL, 'Wasabi House', 'Japanese', '$$', 'Quinpool Road, Halifax, NS', 'Sushi rolls and sashimi.', 'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=800'),
(74, NULL, 'Sushi Jet', 'Japanese', '$$', 'Halifax, NS', 'Sushi and Japanese meals.', 'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=800'),
(75, NULL, 'Tako Sushi & Ramen', 'Japanese', '$$', 'Parkland Drive, Halifax, NS', 'Ramen and sushi.', 'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=800'),
(76, NULL, 'Doraku', 'Japanese', '$$', 'Dartmouth, NS', 'Sushi and Japanese dishes.', 'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=800'),
(77, NULL, 'Ko-Doraku', 'Japanese', '$$', 'Dresden Row, Halifax, NS', 'Japanese rice bowls and sushi.', 'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=800'),
(78, NULL, 'Sushi Shige', 'Japanese', '$$', 'Almon Street, Halifax, NS', 'Traditional sushi and sashimi.', 'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=800'),
(79, NULL, 'Fujiyama Restaurant', 'Japanese', '$$', 'Halifax, NS', 'Japanese sushi and cooked dishes.', 'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=800'),
(80, NULL, 'Kitsune Food Co.', 'Japanese', '$$', 'Halifax, NS', 'Japanese-inspired casual dishes.', 'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=800'),
(81, NULL, 'Kofuku Japanese and Thai', 'Japanese', '$$', 'Robie Street, Halifax, NS', 'Japanese and Thai dishes.', 'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=800'),
(82, NULL, 'Mizu All You Can Eat', 'Japanese', '$$', 'Halifax, NS', 'Sushi and Asian dishes.', 'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=800'),
(83, NULL, 'Mappila Cuisine', 'Indian', '$$', 'Halifax, NS', 'South Indian regional dishes.', 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=800'),
(84, NULL, 'Chopsticks Restaurant', 'Chinese', '$$', 'Halifax, NS', 'Chinese comfort dishes.', 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=800'),
(85, NULL, 'Spice Hub', 'Indian', '$$', 'Dartmouth, NS', 'Indian curries and rice dishes.', 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=800'),
(86, NULL, 'Adda Indian Eatery', 'Indian', '$$', 'Halifax, NS', 'Indian street food and curries.', 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=800'),
(87, NULL, 'Curry Village', 'Indian', '$$', 'Dresden Row, Halifax, NS', 'Indian curries and breads.', 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=800'),
(88, NULL, 'A Taste of India', 'Indian', '$', 'Scotia Square, Halifax, NS', 'Indian quick-service meals.', 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=800'),
(89, NULL, 'Biryani House', 'Indian', '$$', 'Halifax, NS', 'Biryani and Indian dishes.', 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=800'),
(90, NULL, 'Naan n Curry', 'Indian', '$$', 'Halifax, NS', 'Curries and flatbreads.', 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=800'),
(91, NULL, 'Tandoori Flame', 'Indian', '$$', 'Halifax, NS', 'Indian grilled dishes and curries.', 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=800'),
(92, NULL, 'Piatto Pizzeria + Enoteca', 'Italian', '$$', 'Hollis Street, Halifax, NS', 'Neapolitan-style pizza.', 'https://images.unsplash.com/photo-1551183053-bf91a1d81141?w=800'),
(93, NULL, 'Tomavinos Ristorante', 'Italian', '$$', 'South Street, Halifax, NS', 'Italian pizza and pasta.', 'https://images.unsplash.com/photo-1551183053-bf91a1d81141?w=800'),
(94, NULL, 'Mother''s Pizza', 'Pizza', '$$', 'Agricola Street, Halifax, NS', 'Artisan pizza.', 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800'),
(95, NULL, 'Yeah Yeahs Pizza', 'Pizza', '$$', 'Halifax, NS', 'New York-style pizza.', 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800'),
(96, NULL, 'Randy''s Pizza', 'Pizza', '$', 'Halifax, NS', 'Pizza and donairs.', 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800'),
(97, NULL, 'Jessy''s Pizza', 'Pizza', '$', 'Halifax, NS', 'Pizza and casual takeout.', 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800'),
(98, NULL, 'Alexandra''s Pizza', 'Pizza', '$', 'Halifax, NS', 'Pizza and donairs.', 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800'),
(99, NULL, 'Freeman''s Little New York', 'Pizza', '$$', 'Halifax, NS', 'Pizza and casual meals.', 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800'),
(100, NULL, 'Rinaldo''s Italian American Specialties', 'Italian', '$$', 'Windsor Street, Halifax, NS', 'Italian-American sandwiches and pizza.', 'https://images.unsplash.com/photo-1551183053-bf91a1d81141?w=800');