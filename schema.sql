CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR (10) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role INTEGER NOT NULL DEFAULT 2
);

CREATE TABLE products (
    prod_id SERIAL PRIMARY KEY,
    category TEXT NOT NULL,
    name TEXT UNIQUE NOT NULL, 
    ingredients TEXT [], 
    price NUMERIC (4,2) NOT NULL
);

CREATE TABLE extras (
    extra_id SERIAL PRIMARY KEY,
    name VARCHAR (30) UNIQUE NOT NULL,
    price NUMERIC (4,2) NOT NULL
);  

CREATE TABLE sizes (
    size_id SERIAL PRIMARY KEY,
    size_name TEXT NOT NULL,
    price NUMERIC (4,2) NOT NULL
);

CREATE TABLE orderlist (
    order_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    product_id INTEGER REFERENCES products,
    size INTEGER REFERENCES sizes, 
    extras TEXT [],
    price NUMERIC (4,2),
    VISIBLE BOOLEAN
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY, 
    username VARCHAR (20), 
    order_list TEXT, 
    order_time TIMESTAMP NOT NULL
);

INSERT INTO products (category, name, price, ingredients) VALUES ('pizza', 'Mozzarella', 11.00, '{"tomaatti","mozzarella","pesto","tuore basilika"}');

