-- Customers
CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY,
    first_order_date TIMESTAMP,
    country TEXT
);

-- Orders
CREATE TABLE orders (
    order_id TEXT PRIMARY KEY,
    order_date TIMESTAMP,
    order_amount REAL,
	customer_id TEXT,
    country TEXT
);

-- Order items
CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id TEXT,
    product_id TEXT,
    product_name TEXT,
    quantity INTEGER,
    unit_price REAL,
    line_amount REAL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
