CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    password TEXT
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    topic TEXT,
    content TEXT,
    user_id INTEGER REFERENCES users,
    visible BOOLEAN
);

CREATE TABLE replies (
    id SERIAL PRIMARY KEY,
    content TEXT,
    message_id INTEGER REFERENCES messages,
    user_id INTEGER REFERENCES users
);

CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    topic TEXT
    user_id INTEGER REFERENCES users,
    visible BOOLEAN
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

CREATE TABLE chats (
    id SERIAL PRIMARY KEY,
    user1_id INTEGER REFERENCES users,
    user2_id INTEGER REFERENCES users,
    content TEXT
);
