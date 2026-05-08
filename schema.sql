
CREATE TABLE merchants IF NOT EXISTS( --only recreates table if it DNE
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) UNIQUE NOT NULL,
    category VARCHAR(50) NOT NULL,
    risk_level DECIMAL(3, 2) NOT NULL
) STRICT; 
-- enforces types using STRICT

CREATE TABLE transactions IF NOT EXISTS (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    amount DECIMAL(15, 2) NOT NULL,
    merchant_id INTEGER NOT NULL,
    country VARCHAR(50) DEFAULT "USA",
    rate DECIMAL(5, 4) DEFAULT 1.0000, 
    status VARCHAR(20) NOT NULL,
    FOREIGN KEY (merchant_id) REFERENCES merchants(id) ON DELETE RESTRICT
) STRICT;

INSERT INTO merchants(name, category, risk_level)
VALUES ('Nike', 'Athletic', 0.05), ('Adidas', 'Athletic', 0.05), ('Hollister', 'Clothing', 0.10), 
('Shein', 'E-commerce', 0.40), ('Alibaba', 'E-commerce', 0.50);
