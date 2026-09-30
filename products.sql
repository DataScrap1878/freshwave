DROP TABLE IF EXISTS products;

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL UNIQUE,
    category TEXT NOT NULL,
    unit_price REAL NOT NULL
);

INSERT INTO products (product_id, product_name, category, unit_price) VALUES
(101, 'Glace Vanille', 'ice_cream', 3.80),
(102, 'Glace Chocolat', 'ice_cream', 4.00),
(103, 'Glace Fraise', 'ice_cream', 3.90),
(104, 'Sorbet Mangue', 'sorbet', 4.20),
(105, 'Sorbet Citron', 'sorbet', 4.10),
(106, 'Thé glacé citron', 'cold_drink', 3.20),
(107, 'Limonade artisanale', 'cold_drink', 3.50),
(108, 'Smoothie fruits rouges', 'cold_drink', 4.50),
(109, 'Café espresso', 'hot_drink', 2.20),
(110, 'Chocolat chaud', 'hot_drink', 3.40);
