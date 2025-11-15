CREATE TABLE haha (
    id SERIAL PRIMARY KEY,
    trip_id INddddT REFERENCES trips(id) ON DELETE CASCADE,
    event_name TEXT NOT NULL,
    event_time TIMESTAMP,
    address TEXT NOT NULL
);