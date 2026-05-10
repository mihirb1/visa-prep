PRAGMA foreign_keys = ON; -- enforces foreign key constraints during this file
                          -- execution (for insert statements defined)


CREATE TABLE IF NOT EXISTS merchants ( --only recreates table if it DNE
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    category TEXT NOT NULL,
    risk_level REAL NOT NULL
) STRICT;
-- enforces types using STRICT


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
INSERT INTO merchants(name, category, risk_level)
VALUES ('Nike', 'Athletic', 0.05), ('Adidas', 'Athletic', 0.05), ('Hollister', 'Clothing', 0.10),
('Shein', 'E-commerce', 0.40), ('Alibaba', 'E-commerce', 0.50);


INSERT INTO transactions(amount, merchant_id, country, rate, status)
VALUES (20.5, 2, 'United States', 1.0, 'Validated'), (6.70, 1, 'China', 2.78, 'Validated'),
(4.20, 3, 'Bangladesh', 0.48, 'Validated'), (3.14, 5, 'Iran', 3.74, 'Blocked');

