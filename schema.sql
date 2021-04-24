CREATE TABLE cards (id SERIAL PRIMARY KEY, nimi TEXT, elementti TEXT, kuvaus TEXT, harvinaisuus INTEGER);
CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT, actions INTEGER, coins INTEGER, isadmin BOOLEAN);
