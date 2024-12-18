CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('user', 'manager', 'super-admin')),
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    active BOOLEAN DEFAULT 1,
    date_created TEXT DEFAULT CURRENT_TIMESTAMP,
    hire_date TEXT
);

CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    grade INTEGER NOT NULL,
    date_created TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS competencies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS assessments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    competency_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY(competency_id) REFERENCES competencies(id)
);

CREATE TABLE IF NOT EXISTS assessment_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    assessment_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    date_taken TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(assessment_id) REFERENCES assessments(id)
);
