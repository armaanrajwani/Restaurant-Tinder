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
-- Waterfront & Downtown Fine Dining / Seafood
(1, NULL, 'The Bicycle Thief', 'Italian', '$$$', '1475 Lower Water Street, Halifax, NS', 'Vibrant waterfront Italian dining featuring handmade pasta, fresh Atlantic seafood, and an extensive wine list.', 'https://images.unsplash.com/photo-1551183053-bf91a1d81141?w=800'),
(2, NULL, 'The Five Fishermen', 'Seafood', '$$$', '1740 Argyle Street, Halifax, NS', 'Iconic downtown seafood restaurant set in a historic 19th-century building, famous for fresh lobster, scallops, and mussel bar.', 'https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800'),
(3, NULL, 'The Press Gang', 'Seafood', '$$$$', '5218 Prince Street, Halifax, NS', 'Intimate historic stone-walled oyster bar and fine dining venue offering upscale Atlantic seafood and craft cocktails.', 'https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800'),
(4, NULL, 'Ristorante a Mano', 'Italian', '$$', '1477 Lower Water Street, Halifax, NS', 'Bustling Bishop''s Landing trattoria serving wood-fired Neapolitan pizza, classic pastas, and tiramisu.', 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=800'),
(5, NULL, 'Drift', 'Canadian', '$$$', '1709 Lower Water Street, Halifax, NS', 'Modern Nova Scotian cuisine celebrating local ingredients with elevated coastal comfort dishes at Queen''s Marque.', 'https://images.unsplash.com/photo-1544148103-0773bf10d330?w=800'),
(6, NULL, 'Bar Sofia', 'Latin American', '$$$', '1709 Lower Water Street, Halifax, NS', 'Lively waterfront spot offering colorful Latin American share plates, empanadas, ceviche, and agave cocktails.', 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=800'),
(7, NULL, 'Café Lunette', 'French', '$$$', '1741 Lower Water Street, Halifax, NS', 'Parisian-inspired bistro on the Halifax waterfront serving steak frites, fresh oysters, and French pastries.', 'https://images.unsplash.com/photo-1550966871-3ed3cdb5ed0c?w=800'),
(8, NULL, 'Highwayman', 'Spanish', '$$$', '1673 Barrington Street, Halifax, NS', 'Intimate downtown tapas bar known for Spanish small plates, pintxos, and inventive cocktails.', 'https://images.unsplash.com/photo-1515443961218-a51367888e4b?w=800'),
(9, NULL, 'The Canteen on Portland', 'Canadian', '$$', '22 Portland Street, Dartmouth, NS', 'Beloved neighborhood bistro just across the ferry serving seasonal coastal fare and famous crobster rolls.', 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800'),
(10, NULL, '2 Doors Down', 'Canadian', '$$', '1533 Barrington Street, Halifax, NS', 'Modern downtown eatery offering elevated comfort food, gourmet burgers, and local Nova Scotia craft beers.', 'https://images.unsplash.com/photo-1550547660-d9450f859349?w=800'),
(11, NULL, 'Pickford & Black', 'Seafood', '$$', '1869 Upper Water Street, Halifax, NS', 'Harbourfront oyster bar and casual seafood kitchen serving fish tacos, lobster rolls, and local draughts.', 'https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?w=800'),
(12, NULL, 'Lot Six', 'Seafood', '$$$', '1685 Argyle Street, Halifax, NS', 'Trendy glass-atrium oyster bar and restaurant on Argyle Street known for cocktails and contemporary Atlantic plates.', 'https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=800'),

-- North End, Agricola & Hydrostone Favorites
(13, NULL, 'Bar Kismet', 'Seafood', '$$$', '2733 Agricola Street, Halifax, NS', 'Acclaimed North End neighborhood gem specializing in fresh local seafood, handmade pasta, and world-class cocktails.', 'https://images.unsplash.com/photo-1551218808-94e220e084d2?w=800'),
(14, NULL, 'Salvatore''s Pizzaiolo Trattoria', 'Pizza', '$$', '5541 Young Street, Halifax, NS', 'Hydrostone institution famous for New York-style thin-crust pizzas, hero sandwiches, and homemade meatballs.', 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800'),
(15, NULL, 'Agricola Street Brasserie', 'French', '$$$', '2540 Agricola Street, Halifax, NS', 'Chic industrial-style brasserie serving wood-fired mains, charcuterie, and weekend brunch in the North End.', 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800'),
(16, NULL, 'Edna', 'Canadian', '$$$', '2053 Gottingen Street, Halifax, NS', 'Cozy, high-energy Gottingen Street favorite known for seasonal small plates, fresh oysters, and lively weekend brunch.', 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800'),
(17, NULL, 'Studio East Food+Drink', 'Asian Fusion', '$$', '6021 Cunard Street, Halifax, NS', 'Creative Asian-fusion gastropub serving steamed bao buns, Korean fried chicken, and bold noodle bowls.', 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=800'),
(18, NULL, 'Rinaldi''s Italian Kitchen', 'Italian', '$$', '2310 Gottingen Street, Halifax, NS', 'Casual North End Italian kitchen offering hearty pasta bowls, paninis, and classic comfort dishes.', 'https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?w=800'),
(19, NULL, 'Field Guide', 'Canadian', '$$$', '2076 Gottingen Street, Halifax, NS', 'Intimate North End kitchen and cocktail bar focusing on seasonal local produce and inventive small plates.', 'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=800'),
(20, NULL, 'The Narrows Public House', 'Pub', '$$', '2720 Gottingen Street, Halifax, NS', 'Restored heritage house pub serving nostalgic Maritime comfort recipes, local beers, and house-cured meats.', 'https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=800'),

-- Indian & South Asian
(21, NULL, 'Tawa Grill', 'Indian', '$$', '1569 Hollis Street, Halifax, NS', 'Downtown Indian restaurant serving authentic tandoori specialties, rich curries, and fresh garlic naan.', 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=800'),
(22, NULL, 'Rasa Flavours of India', 'Indian', '$$', '1546 Birmingham Street, Halifax, NS', 'Modern Indian dining near Spring Garden offering regional curries, biryani, and vibrant street-food starters.', 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=800'),
(23, NULL, 'Mirchi Tandoor', 'Indian', '$$', '5245 Blowers Street, Halifax, NS', 'Popular downtown spot for clay-oven kebabs, butter chicken, vindaloo, and vegetarian thalis.', 'https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=800'),
(24, NULL, 'Anardana Indian Restaurant & Bar', 'Indian', '$$', '5530 Young Street, Halifax, NS', 'Contemporary North End Indian restaurant & lounge featuring craft cocktails and elevated North Indian classics.', 'https://images.unsplash.com/photo-1517244683847-7456b63c5969?w=800'),
(25, NULL, 'Dhaba Express', 'Indian', '$$', '8 Oland Crescent, Halifax, NS', 'Casual Bayers Lake favorite serving homestyle Punjabi curries, dosas, and generous portions.', 'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=800'),
(26, NULL, 'Red Chillies Flavours of India', 'Indian', '$$', '1496 Lower Water Street, Halifax, NS', 'Waterfront Indian kitchen known for aromatic biryanis, lamb rogan josh, and freshly baked tandoori breads.', 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=800'),

-- Japanese, Korean & Thai
(27, NULL, 'Dharma Sushi', 'Japanese', '$$', '1576 Argyle Street, Halifax, NS', 'Cozy downtown sushi bar offering creative maki rolls, fresh sashimi, and Japanese comfort dishes.', 'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=800'),
(28, NULL, 'Buta Ramen', 'Japanese', '$$', '5190 Morris Street, Halifax, NS', 'Dedicated ramen shop simmering rich tonkotsu, miso, and spicy broth bowls with house-made toppings.', 'https://images.unsplash.com/photo-1557872943-16a5ac26437e?w=800'),
(29, NULL, 'Bi-One Korean Restaurant', 'Korean', '$$', '1542 South Park Street, Halifax, NS', 'Casual South End spot for sizzling bibimbap, bulgogi, japchae, and spicy tofu stews.', 'https://images.unsplash.com/photo-1590301157890-4810ed352733?w=800'),
(30, NULL, 'Cha Baa Thai Restaurant', 'Thai', '$$', '1546 Queen Street, Halifax, NS', 'Long-standing favorite for authentic Pad Thai, green curry, tom yum soup, and mango sticky rice.', 'https://images.unsplash.com/photo-1559314809-0d155014e29e?w=800'),
(31, NULL, 'Kanpai Izakaya', 'Japanese', '$$', '1459 Dresden Row, Halifax, NS', 'Lively Japanese pub near Spring Garden serving yakitori skewers, takoyaki, ramen, and sake.', 'https://images.unsplash.com/photo-1580822184713-fc5400e7fe10?w=800'),

-- Mexican, Middle Eastern & Mediterranean
(32, NULL, 'Antojo Tacos + Tequila', 'Mexican', '$$', '1667 Argyle Street, Halifax, NS', 'High-energy Argyle Street cantina serving street-style tacos, loaded nachos, guacamole, and margaritas.', 'https://images.unsplash.com/photo-1551504734-5ee1c4a1479b?w=800'),
(33, NULL, 'El Chino Snack Bar', 'Mexican', '$$', '2398 Robie Street, Halifax, NS', 'Quirky neighborhood spot blending Mexican street tacos and snacks with Asian-inspired flavors.', 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=800'),
(34, NULL, 'Mezza Lebanese Kitchen', 'Middle Eastern', '$', '5431 Spring Garden Road, Halifax, NS', 'Fast-casual Halifax staple for chicken shawarma wraps, falafel bowls, hummus, and garlic sauce.', 'https://images.unsplash.com/photo-1529006557810-274b9b2fc783?w=800'),
(35, NULL, 'Tareks Cafe', 'Middle Eastern', '$', '3045 Robie Street, Halifax, NS', 'Beloved family-run North End cafe known for generous shawarma plates, fresh pita, and lentil soup.', 'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=800'),

-- Pubs, Burgers & Halifax Classics
(36, NULL, 'Durty Nelly''s Irish Pub', 'Pub', '$$', '1645 Argyle Street, Halifax, NS', 'Authentic Irish pub built in Ireland and shipped to Halifax, serving fish & chips, shepherd''s pie, and live music.', 'https://images.unsplash.com/photo-1572116469696-31de0f17cc34?w=800'),
(37, NULL, 'The Stubborn Goat Gastropub', 'Pub', '$$', '1579 Grafton Street, Halifax, NS', 'Downtown gastropub featuring wood-fired pizzas, local craft taps, and a bustling Argyle/Grafton patio.', 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800'),
(38, NULL, 'Darrell''s Restaurant', 'Burgers', '$', '5576 Fenwick Street, Halifax, NS', 'Iconic South End diner famous across Halifax for its legendary Peanut Butter Burger and pita wraps.', 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=800'),
(39, NULL, 'King of Donair', 'Canadian', '$', '6420 Quinpool Road, Halifax, NS', 'Home of Halifax''s official food—spiced beef donairs sliced off the spit with tomatoes, onions, and sweet donair sauce.', 'https://images.unsplash.com/photo-1626700051175-6818013e1d4f?w=800'),
(40, NULL, 'The Wooden Monkey', 'Canadian', '$$', '1707 Grafton Street, Halifax, NS', 'Downtown favorite focused on organic, locally sourced Maritime dishes, wood-fired pizzas, and vegan/gluten-free options.', 'https://images.unsplash.com/photo-1498837167922-ddd27525d352?w=800');