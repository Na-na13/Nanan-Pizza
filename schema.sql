CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR (10) UNIQUE NOT NULL,
    password VARCHAR (10) NOT NULL
);
