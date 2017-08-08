DROP TABLE IF EXISTS chores;
CREATE TABLE chores(
    id integer PRIMARY KEY AUTOINCREMENT,
    title text NOT NULL,
    owner text NOT NULL,
    status integer NOT NULL
);