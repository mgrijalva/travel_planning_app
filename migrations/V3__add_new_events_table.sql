CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    trip_id INT REFERENCES trips(id) ON DELETE CASCADE,
    event_name TEXT NOT NULL,
    event_time TIMESTAMP,
    address TEXT NOT NULL
);