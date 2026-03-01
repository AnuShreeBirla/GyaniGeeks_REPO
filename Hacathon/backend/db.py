"""
SQLite schema for AI-Powered Personalized Learning Intelligence System.
Schema: User, Topic, Subject, Quiz, QuizAttempt, Reminder, Rating.
"""
import sqlite3
import os
import json

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'learning.db')

def get_conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_conn()
    c = conn.cursor()

    # Users: name, email, college, stream, streak, xp, enrolled_courses (JSON), mastery_map (JSON), password_hash, theme
    c.execute("""
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        college TEXT,
        stream TEXT,
        streak INTEGER DEFAULT 0,
        xp INTEGER DEFAULT 0,
        enrolled_courses TEXT DEFAULT '[]',
        mastery_map TEXT DEFAULT '{}',
        password_hash TEXT,
        theme TEXT DEFAULT 'light',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Subject (e.g. Data Structures, Calculus)
    c.execute("""
    CREATE TABLE IF NOT EXISTS subject (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        estimated_weeks INTEGER DEFAULT 4
    )
    """)

    # Topic: name, subject_id, difficulty, prerequisites (JSON), estimated_time_mins
    c.execute("""
    CREATE TABLE IF NOT EXISTS topic (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        subject_id INTEGER NOT NULL,
        difficulty TEXT DEFAULT 'medium',
        prerequisites TEXT DEFAULT '[]',
        estimated_time_mins INTEGER DEFAULT 45,
        week_number INTEGER DEFAULT 1,
        FOREIGN KEY (subject_id) REFERENCES subject(id)
    )
    """)

    # Quiz: topic_id, questions (JSON)
    c.execute("""
    CREATE TABLE IF NOT EXISTS quiz (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic_id INTEGER NOT NULL,
        questions TEXT NOT NULL,
        FOREIGN KEY (topic_id) REFERENCES topic(id)
    )
    """)

    # Quiz attempt: user_id, quiz_id/topic_id, score, time_seconds, confidence, created_at
    c.execute("""
    CREATE TABLE IF NOT EXISTS quiz_attempt (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        topic_id INTEGER NOT NULL,
        score REAL NOT NULL,
        time_seconds INTEGER,
        confidence INTEGER,
        reattempt_count INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES user(id),
        FOREIGN KEY (topic_id) REFERENCES topic(id)
    )
    """)

    # Reminder: user_id, daily_study_time (HH:MM), notify_browser BOOL, notify_email BOOL
    c.execute("""
    CREATE TABLE IF NOT EXISTS reminder (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL UNIQUE,
        daily_study_time TEXT,
        notify_browser INTEGER DEFAULT 1,
        notify_email INTEGER DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES user(id)
    )
    """)

    # Rating: user_id, stars 1-5, created_at
    c.execute("""
    CREATE TABLE IF NOT EXISTS rating (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        stars INTEGER NOT NULL CHECK(stars >= 1 AND stars <= 5),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES user(id)
    )
    """)

    # Download (resource): user_id, resource_name, topic_id, created_at
    c.execute("""
    CREATE TABLE IF NOT EXISTS download (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        resource_name TEXT NOT NULL,
        topic_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES user(id)
    )
    """)

    conn.commit()
    conn.close()

def seed_data():
    """Insert default user, subjects, topics, quizzes if empty."""
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM user")
    if c.fetchone()[0] > 0:
        conn.close()
        return
    c.execute("""
    INSERT INTO user (id, name, email, college, stream, streak, xp, enrolled_courses, mastery_map)
    VALUES (1, 'Avinash', 'avinash@example.com', 'Engineering College', 'CSE', 7, 1250,
            '["Data Structures","Calculus"]', '{"1":55,"2":72,"3":48,"4":65}')
    """)
    c.execute("INSERT INTO subject (id, name, description, estimated_weeks) VALUES (1, 'Data Structures', 'Arrays, Lists, Trees, Graphs', 4)")
    c.execute("INSERT INTO subject (id, name, description, estimated_weeks) VALUES (2, 'Calculus', 'Limits, Derivatives, Integration', 3)")
    c.execute("INSERT INTO topic (id, name, subject_id, week_number, estimated_time_mins) VALUES (1, 'Arrays', 1, 1, 45)")
    c.execute("INSERT INTO topic (id, name, subject_id, week_number, estimated_time_mins) VALUES (2, 'Linked List', 1, 2, 50)")
    c.execute("INSERT INTO topic (id, name, subject_id, week_number, estimated_time_mins) VALUES (3, 'Trees', 1, 3, 60)")
    c.execute("INSERT INTO topic (id, name, subject_id, week_number, estimated_time_mins) VALUES (4, 'Graphs', 1, 4, 55)")
    c.execute("INSERT INTO topic (id, name, subject_id, week_number, estimated_time_mins) VALUES (5, 'Limits', 2, 1, 40)")
    c.execute("INSERT INTO topic (id, name, subject_id, week_number, estimated_time_mins) VALUES (6, 'Derivatives', 2, 2, 50)")
    c.execute("INSERT INTO topic (id, name, subject_id, week_number, estimated_time_mins) VALUES (7, 'Integration', 2, 3, 55)")
    q1 = json.dumps([
        {"q": "What is the time complexity of array access?", "options": ["O(1)", "O(n)", "O(log n)"], "correct": 0},
        {"q": "Which is a dynamic array?", "options": ["C array", "Python list", "Both"], "correct": 1},
        {"q": "Array elements are stored:", "options": ["Contiguously", "Randomly", "In a tree"], "correct": 0},
        {"q": "Size of static array is:", "options": ["Fixed", "Dynamic", "Unknown"], "correct": 0},
        {"q": "Index of first element in 0-based array?", "options": ["1", "0", "-1"], "correct": 1},
        {"q": "Best for random access?", "options": ["Linked List", "Array", "Stack"], "correct": 1},
        {"q": "Worst case insert at end in dynamic array?", "options": ["O(1)", "O(n)", "O(log n)"], "correct": 1},
        {"q": "Traversal of array of n elements?", "options": ["O(1)", "O(n)", "O(n^2)"], "correct": 1},
        {"q": "Array can store?", "options": ["Same type", "Mixed types", "Only numbers"], "correct": 0},
        {"q": "Memory for array is?", "options": ["Contiguous", "Scattered", "Stack only"], "correct": 0},
    ])
    for tid in [1, 2, 3, 4]:
        c.execute("INSERT OR IGNORE INTO quiz (topic_id, questions) VALUES (?, ?)", (tid, q1))
    q2 = json.dumps([
        {"q": "Derivative of x^2?", "options": ["x", "2x", "x^2"], "correct": 1},
        {"q": "Integral of 1/x?", "options": ["ln|x|", "x^2", "1/x^2"], "correct": 0},
        {"q": "Limit of sin(x)/x as x->0?", "options": ["0", "1", "undefined"], "correct": 1},
        {"q": "d/dx(e^x)=?", "options": ["e^x", "xe^(x-1)", "0"], "correct": 0},
        {"q": "∫0 dx = ?", "options": ["0", "x", "C"], "correct": 2},
        {"q": "Chain rule: d/dx f(g(x)) = ?", "options": ["f' g'", "f'(g(x)) g'(x)", "f g"], "correct": 1},
        {"q": "Limit of (1+1/n)^n as n→∞?", "options": ["1", "e", "0"], "correct": 1},
        {"q": "Derivative of constant?", "options": ["0", "1", "constant"], "correct": 0},
        {"q": "∫x dx = ?", "options": ["x^2", "x^2/2 + C", "2x"], "correct": 1},
        {"q": "L'Hospital applies when limit is?", "options": ["0/0 or ∞/∞", "0", "1"], "correct": 0},
    ])
    for tid in [5, 6, 7]:
        c.execute("INSERT OR IGNORE INTO quiz (topic_id, questions) VALUES (?, ?)", (tid, q2))
    conn.commit()
    conn.close()

init_db()
seed_data()
