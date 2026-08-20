CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    court_id INTEGER NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('confirmed', 'cancelled', 'pending')),
    price INTEGER NOT NULL CHECK (price >= 0)
);

INSERT OR REPLACE INTO bookings (id, user_id, court_id, status, price)
VALUES
    (101, 5, 1, 'confirmed', 100),
    (102, 7, 2, 'cancelled', 150),
    (103, 5, 2, 'confirmed', 200),
    (104, 8, 1, 'pending', 100);


CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

INSERT OR REPLACE INTO users (id, name, email)
VALUES
    (5, 'Dani', 'dani@example.com'),
    (7, 'Alex', 'alex@example.com'),
    (8, 'John', 'john@example.com');

CREATE TABLE IF NOT EXISTS courts (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

INSERT OR REPLACE INTO courts (id, name)
VALUES
    (1, 'Court A'),
    (2, 'Court B');
