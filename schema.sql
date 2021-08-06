CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    password TEXT
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    topic TEXT,
    content TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE replies (
    id SERIAL PRIMARY KEY,
    contet TEXT,
    message_id INTEGER REFERENCES messages,
    usre_id INTEGER REFERENCES users
);

CREATE TABLE qustions (
    id SERIAL PRIMARY KEY,
    topic TEXT
);

CREATE TABLE choices (
    id SERIAL PRIMARY KEY,
    question_id INTEGER REFERENCES questions,
    choice TEXT
);

CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    choice_id INTEGER REFERENCES choices,
    user_id INTEGER REFERENCES users
);
