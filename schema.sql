CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR (10) UNIQUE NOT NULL,
    password VARCHAR (10) NOT NULL
);

CREATE TABLE pizza (
    pizza_id SERIAL PRIMARY KEY, 
    name TEXT UNIQUE NOT NULL, 
    ingredients TEXT [] NOT NULL, 
    price NUMERIC (4,2) NOT NULL
);

CREATE TABLE extras (
    extra_id SERIAL PRIMARY KEY,
    name VARCHAR (30) UNIQUE NOT NULL
    price NUMERIC (4,2) NOT NULL
);  

CREATE TABLE orderlist (
    order_id SERIAL PRIMARY KEY, 
    prod TEXT NOT NULL, 
    size INTEGER NOT NULL, 
    extras TEXT []
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY, 
    user VARCHAR (20), 
    order TEXT, 
    order_time TIMESTAMP NOT NULL
);

