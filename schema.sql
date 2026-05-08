CREATE TABLE transactions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    amount DECIMAL(15, 2) NOT NULL,
    merchant VARCHAR(255) NOT NULL,
    country VARCHAR(50) DEFAULT "USA",
    rate DECIMAL(5, 4) DEFAULT 1.0000, 
    status VARCHAR(20) NOT NULL
);

INSERT INTO transactions(amount, merchant, status)
VALUES(10.0, "Nike", 'Validated');

INSERT INTO transactions(amount, merchant, country, rate, status)
VALUES(25.5, "Adidas", "Germany", 1.08, 'Validated');

INSERT INTO transactions(amount, merchant, country, rate, status)
VALUES(13.3, "Toyota", "Iran", 2.86, 'Blocked');