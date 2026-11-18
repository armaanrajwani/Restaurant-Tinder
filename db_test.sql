-- Dishr MySQL 8.0+ test database
-- Real Halifax restaurant names/addresses; descriptions and price bands are illustrative test data.
-- Safe to rerun: recreates only the dishr_test database.
CREATE DATABASE IF NOT EXISTS dishr_test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE dishr_test;

CREATE TABLE IF NOT EXISTS users (
 user_id INT AUTO_INCREMENT PRIMARY KEY,
 name VARCHAR(100) NOT NULL,
 email VARCHAR(255) NOT NULL UNIQUE,
 password_hash VARCHAR(255) NOT NULL,
 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS customers (
 user_id INT PRIMARY KEY,
 FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS restaurant_owners (
 user_id INT PRIMARY KEY,
 business_name VARCHAR(150),
 FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS user_preferences (
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
CREATE TABLE IF NOT EXISTS restaurants (
 restaurant_id INT AUTO_INCREMENT PRIMARY KEY,
 owner_id INT NULL,
 name VARCHAR(150) NOT NULL,
 cuisine VARCHAR(100) NOT NULL,
 price_range VARCHAR(10) NOT NULL,
 location VARCHAR(255) NOT NULL,
 description TEXT,
 image_url VARCHAR(255),
 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY (owner_id) REFERENCES restaurant_owners(user_id) ON DELETE SET NULL,
 CHECK (price_range IN ('$','$$','$$$','$$$$'))
);
CREATE TABLE IF NOT EXISTS swipes (
 swipe_id INT AUTO_INCREMENT PRIMARY KEY,
 user_id INT NOT NULL,
 restaurant_id INT NOT NULL,
 swipe_type ENUM('like','dislike','havent_been') NOT NULL,
 swiped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 UNIQUE KEY uq_swipe_user_restaurant (user_id, restaurant_id),
 FOREIGN KEY (user_id) REFERENCES customers(user_id) ON DELETE CASCADE,
 FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS saves (
 save_id INT AUTO_INCREMENT PRIMARY KEY,
 user_id INT NOT NULL,
 restaurant_id INT NOT NULL,
 saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 UNIQUE KEY uq_save_user_restaurant (user_id, restaurant_id),
 FOREIGN KEY (user_id) REFERENCES customers(user_id) ON DELETE CASCADE,
 FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS reviews (
 review_id INT AUTO_INCREMENT PRIMARY KEY,
 user_id INT NOT NULL,
 restaurant_id INT NOT NULL,
 rating TINYINT NOT NULL,
 comment TEXT,
 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY (user_id) REFERENCES customers(user_id) ON DELETE CASCADE,
 FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id) ON DELETE CASCADE,
 CHECK (rating BETWEEN 1 AND 5)
);

-- owner_id is NULL because real-world ownership accounts have not been created.
-- image_url is NULL until images with usable permissions are supplied.
INSERT INTO restaurants (restaurant_id, owner_id, name, cuisine, price_range, location, description, image_url) VALUES
(1,NULL,'The Bicycle Thief','Italian','$$$','1475 Lower Water Street, Halifax, NS, Canada','Waterfront Italian-inspired dining with pasta and seafood.',NULL),
(2,NULL,'The Five Fishermen','Seafood','$$$','1740 Argyle Street, Halifax, NS, Canada','Seafood-focused restaurant in a historic downtown setting.',NULL),
(3,NULL,'The Press Gang','Seafood','$$$$','5218 Prince Street, Halifax, NS, Canada','Historic downtown restaurant known for oysters and seafood.',NULL),
(4,NULL,'Ristorante a Mano','Italian','$$','1477 Lower Water Street, Halifax, NS, Canada','Italian waterfront restaurant serving pasta and pizza.',NULL),
(5,NULL,'Bar Kismet','Seafood','$$$','2733 Agricola Street, Halifax, NS, Canada','North End seafood, small plates and cocktails.',NULL),
(6,NULL,'Salvatore''s Pizzaiolo Trattoria','Pizza','$$','5541 Young Street, Halifax, NS, Canada','North End pizzeria known for pizza and sandwiches.',NULL),
(7,NULL,'Antojo Tacos + Tequila','Mexican','$$','1667 Argyle Street, Halifax, NS, Canada','Mexican-inspired tacos and casual downtown dining.',NULL),
(8,NULL,'Agricola Street Brasserie','French','$$$','2540 Agricola Street, Halifax, NS, Canada','Brasserie-style dining on Agricola Street.',NULL),
(9,NULL,'Durty Nelly''s Irish Pub','Pub','$$','1645 Argyle Street, Halifax, NS, Canada','Irish-style pub serving hearty casual meals.',NULL),
(10,NULL,'Drift','Canadian','$$$','1709 Lower Water Street, Halifax, NS, Canada','Contemporary Canadian cuisine on the Halifax waterfront.',NULL)
ON DUPLICATE KEY UPDATE
 name=VALUES(name), cuisine=VALUES(cuisine), price_range=VALUES(price_range),
 location=VALUES(location), description=VALUES(description);

-- Sanity checks
SELECT COUNT(*) AS restaurant_count FROM restaurants;
SELECT restaurant_id, name, cuisine, price_range, location FROM restaurants ORDER BY restaurant_id;
