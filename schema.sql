PRAGMA foreign_keys = ON; -- enforces foreign key constraints during this file
                          -- execution (for insert statements defined)

CREATE TABLE IF NOT EXISTS merchants ( --only recreates table if it DNE
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    category TEXT NOT NULL,
    risk_level REAL NOT NULL,
    balance REAL DEFAULT 0.0
) STRICT;
-- enforces types using STRICT

CREATE INDEX IF NOT EXISTS idx_merchant_category ON merchants(category);

CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    amount REAL NOT NULL,
    merchant_id INTEGER NOT NULL,
    country TEXT DEFAULT "USA",
    rate REAL DEFAULT 1.0000,
    status TEXT NOT NULL,
    FOREIGN KEY (merchant_id) REFERENCES merchants(id) ON DELETE RESTRICT
) STRICT;

-- Sample data
INSERT INTO merchants (name, category, risk_level) VALUES 
('Apple Store', 'Tech', 0.02),
('McDonalds', 'Food', 0.05),
('Louis Vuitton', 'Luxury', 0.15),
('BettingWorld', 'Gambling', 0.85),
('Local Coffee', 'Food', 0.10);

INSERT INTO transactions (amount, merchant_id, country, rate, status) VALUES 
(1200.00, 1, 'USA', 1.0, 'Validated'),      -- Big Tech Purchase
(15.50, 2, 'USA', 1.0, 'Validated'),        -- Fast Food
(3500.00, 3, 'France', 0.92, 'Pending'),    -- High Value Luxury
(50.00, 4, 'Cyprus', 0.85, 'Blocked'),      -- High Risk Gambling
(4.25, 5, 'USA', 1.0, 'Validated'),         -- Small Coffee
(250.00, 4, 'China', 7.24, 'Validated'),     -- E-commerce International
(89.99, 1, 'Vietnam', 25000.0, 'Validated'); -- Athletic Apparel

