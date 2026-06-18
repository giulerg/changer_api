CREATE SCHEMA IF NOT EXISTS currency;

CREATE TABLE IF NOT EXISTS currency.raw_data (
    id SERIAL PRIMARY KEY,
    data JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status VARCHAR(20) NOT NULL DEFAULT 'NEW'
);


CREATE TABLE IF NOT EXISTS currency.transformed_data (
    id SERIAL PRIMARY KEY,
    main_currency VARCHAR(3) NOT NULL,
    currency  VARCHAR(3) NOT NULL,
    rate NUMERIC(20, 10) NOT NULL,
    date TIMESTAMPTZ NOT NULL 
);