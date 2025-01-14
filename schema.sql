CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    final_grade TEXT DEFAULT NULL 
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
    user_id INTEGER NOT NULL,
    competency_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    date_taken TEXT NOT NULL,
    assessment_type TEXT,
    feedback TEXT DEFAULT NULL, 
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (competency_id) REFERENCES competencies(id)
);
