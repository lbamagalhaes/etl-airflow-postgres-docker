CREATE TABLE IF NOT EXISTS my_table (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  age INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS stock_data (
    Symbol VARCHAR,
    Time TIMESTAMP,
    Price NUMERIC,
    Currency VARCHAR,
    Time_Location VARCHAR
);