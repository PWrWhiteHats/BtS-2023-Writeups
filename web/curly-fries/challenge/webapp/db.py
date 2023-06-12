import os
import sqlite3
from hashlib import sha256


def get_db():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, "database.db")
    conn = sqlite3.connect(db_path, check_same_thread=False)
    return conn


def create_db():
    db = get_db()
    db.cursor().executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        );
        CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT
        );
        INSERT INTO Tasks (description) VALUES ('Order a new batch of fries');
        INSERT INTO Tasks (description) VALUES ('Experiment with new curly fries prototype');
        INSERT INTO Tasks (description) VALUES ('flag{fake_flag_for_testing}');
        INSERT INTO Tasks (description) VALUES ('Settle the beef with McDonalds');
        """
    )
    db.commit()
    db.close()


def register_user(username, password):
    db = get_db()
    hashed_password = sha256(password.encode("utf-8")).hexdigest()
    try:
        db.cursor().execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password),
        )
        db.commit()
        db.close()
        return True
    except sqlite3.IntegrityError:
        return False


def get_user(username, password):
    db = get_db()
    hashed_password = sha256(password.encode("utf-8")).hexdigest()
    result = db.cursor().execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, hashed_password),
    )
    user = result.fetchone()
    db.close()
    return True if user is not None else False


def get_tasks():
    db = get_db()
    return db.cursor().execute("SELECT * FROM Tasks").fetchall()
