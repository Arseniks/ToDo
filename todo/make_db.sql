CREATE TABLE Tasks (
    uuid uuid PRIMARY KEY,
    name text NOT NULL,
    date date NOT NULL,
    done bool NOT NULL,
    description text
);