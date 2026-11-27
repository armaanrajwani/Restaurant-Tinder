USE dishr_test;
CREATE TABLE IF NOT EXISTS daily_swipe_usage (
 user_id INT NOT NULL, swipe_date DATE NOT NULL, used INT NOT NULL DEFAULT 0,
 PRIMARY KEY (user_id, swipe_date), FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
 CHECK (used BETWEEN 0 AND 10)
);
CREATE TABLE IF NOT EXISTS restaurant_promotions (
 promotion_id INT AUTO_INCREMENT PRIMARY KEY,
 restaurant_id INT NOT NULL, owner_id INT NOT NULL,
 payment_reference VARCHAR(255) NOT NULL UNIQUE,
 starts_at DATETIME NOT NULL, ends_at DATETIME NOT NULL,
 FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id) ON DELETE CASCADE,
 FOREIGN KEY (owner_id) REFERENCES restaurant_owners(user_id) ON DELETE CASCADE,
 CHECK (ends_at > starts_at), INDEX (restaurant_id, ends_at)
);
-- Existing non-owner accounts become customers.
INSERT IGNORE INTO customers (user_id)
SELECT u.user_id FROM users u LEFT JOIN restaurant_owners o ON o.user_id=u.user_id WHERE o.user_id IS NULL;
